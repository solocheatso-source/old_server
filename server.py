# server.py - Главный WebSocket сервер для V2/Standoff
import asyncio
import websockets
import json
import logging
import signal
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from typing import Dict, Set
from rpc_handlers import RPCHandler, DateTimeEncoder
from database import Database

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('V2Server')

# Конфигурация сервера
import os
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 25505))
HTTP_PORT = int(os.environ.get("HTTP_PORT", PORT + 1))

# MongoDB конфигурация
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://mongo:odPQUCRuWAiCqADMYBQwRecDahZgVhUN@turntable.proxy.rlwy.net:25506")
MONGODB_DB = os.environ.get("MONGODB_DB", "v2_standoff")
MAX_MESSAGE_SIZE = 10 * 1024 * 1024  # 10MB
PING_INTERVAL = 30
PING_TIMEOUT = 10

class ClientManager:
    """Менеджер подключенных клиентов"""
    
    def __init__(self):
        self._clients: Dict[int, websockets.WebSocketServerProtocol] = {}
        self._client_info: Dict[int, dict] = {}
    
    def add(self, websocket: websockets.WebSocketServerProtocol) -> int:
        client_id = id(websocket)
        self._clients[client_id] = websocket
        self._client_info[client_id] = {
            'connected_at': datetime.now(),
            'address': websocket.remote_address,
            'requests': 0,
            'user_id': None  # Добавляем поле для хранения user_id
        }
        return client_id
    
    def remove(self, client_id: int):
        self._clients.pop(client_id, None)
        self._client_info.pop(client_id, None)
    
    def set_user_id(self, client_id: int, user_id: str):
        """Устанавливает user_id для клиента"""
        if client_id in self._client_info:
            self._client_info[client_id]['user_id'] = user_id
    
    def get_user_id(self, client_id: int) -> str:
        """Получает user_id для клиента"""
        return self._client_info.get(client_id, {}).get('user_id')
    
    def get(self, client_id: int):
        return self._clients.get(client_id)

    def get_client_ids_by_user_id(self, user_id: str):
        """Return all connected client_ids for a given user_id."""
        if not user_id:
            return []
        result = []
        for cid, info in self._client_info.items():
            if info.get("user_id") == user_id:
                result.append(cid)
        return result
    
    def increment_requests(self, client_id: int):
        if client_id in self._client_info:
            self._client_info[client_id]['requests'] += 1
    
    @property
    def count(self) -> int:
        return len(self._clients)
    
    @property
    def all_clients(self):
        return self._clients.items()

clients = ClientManager()
rpc = None  # Будет инициализирован в main() с базой данных
httpd: ThreadingHTTPServer | None = None

class HttpHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A003
        # Suppress default HTTP server logging.
        return

    def do_GET(self):  # noqa: N802
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/standoff/inventory/promocode":
                qs = parse_qs(parsed.query or "")
                user_id = (qs.get("id") or [""])[0]
                promo = (qs.get("promo") or [""])[0]
                result = "error"
                try:
                    result = rpc.activate_promocode(str(user_id), str(promo))
                except Exception as e:
                    logger.error(f"Promocode handler error: {e}")
                    result = "error"

                body = (result or "error").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            self.send_response(404)
            self.end_headers()
        except Exception as e:
            logger.error(f"HTTP error: {e}")
            try:
                self.send_response(500)
                self.end_headers()
            except Exception:
                pass

async def handle_ping(websocket, message: bytes) -> bool:
    """Обработка ping сообщений"""
    if len(message) == 1 and message[0] == 1:
        await websocket.send(bytes([1]))
        return True
    return False

async def handle_rpc_request(websocket, message: str, client_id: int) -> None:
    """Обработка RPC запроса"""
    try:
        request = json.loads(message)
    except json.JSONDecodeError as e:
        logger.warning(f"[{client_id}] Invalid JSON: {e}")
        return
    
    # Игнорируем тестовые сообщения
    if "type" in request and request["type"] == "connection_test":
        logger.info(f"[{client_id}] Connection test received, ignoring")
        return
    
    request_id = request.get("Id", "")
    service_name = request.get("ServiceName", "")
    method_name = request.get("MethodName", "")
    params = request.get("Params", [])
    
    # Если нет ServiceName, это не RPC запрос
    if not service_name:
        logger.warning(f"[{client_id}] Not an RPC request, ignoring: {message[:100]}")
        return
    
    logger.info(f"[{client_id}] ===== RPC REQUEST =====")
    logger.info(f"[{client_id}] Service: {service_name}")
    logger.info(f"[{client_id}] Method: {method_name}")
    logger.info(f"[{client_id}] Params: {params}")
    logger.info(f"[{client_id}] ======================")
    
    clients.increment_requests(client_id)
    
    try:
        result = rpc.handle(service_name, method_name, params, client_id)
        
        # Логируем результат
        if result.get("Exception"):
            logger.error(f"[{client_id}] RPC Exception: {result.get('Exception')}")
        else:
            return_value = result.get("Return", "")
            if len(str(return_value)) > 200:
                logger.info(f"[{client_id}] RPC Success: {str(return_value)[:200]}...")
            else:
                logger.info(f"[{client_id}] RPC Success: {return_value}")
        
        response = {
            "RpcResponse": {
                "Id": request_id,
                "Return": result.get("Return"),
                "Exception": result.get("Exception")
            },
            "EventResponse": None
        }
        
        await websocket.send(json.dumps(response, cls=DateTimeEncoder))

        # Send any queued async events (friends/lobby updates, etc.)
        try:
            pending = rpc.drain_pending_events()
        except Exception:
            pending = []
        for ev in pending or []:
            try:
                await send_event(ev.get("client_id"), ev.get("event_name"), ev.get("listener_name"), ev.get("params"))
            except Exception as e:
                logger.error(f"Failed to send queued event: {e}")
        
    except Exception as e:
        logger.error(f"[{client_id}] RPC Error: {e}")
        import traceback
        traceback.print_exc()
        
        error_response = {
            "RpcResponse": {
                "Id": request_id,
                "Return": None,
                "Exception": {
                    "Id": "ServerError",
                    "Code": 500,
                    "Message": str(e),
                    "Params": {}
                }
            },
            "EventResponse": None
        }
        await websocket.send(json.dumps(error_response, cls=DateTimeEncoder))

async def handle_client(websocket: websockets.WebSocketServerProtocol):
    """Обработка подключения клиента"""
    client_id = clients.add(websocket)
    addr = websocket.remote_address
    logger.info(f"Client connected: {client_id} from {addr} (total: {clients.count})")
    
    try:
        async for message in websocket:
            # Ping/Pong
            if isinstance(message, bytes):
                if await handle_ping(websocket, message):
                    continue
            
            # RPC Request
            await handle_rpc_request(websocket, message, client_id)
                
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Client disconnected: {client_id}, code: {e.code}")
    except Exception as e:
        logger.error(f"Client error: {client_id}, {type(e).__name__}: {e}")
    finally:
        # Обрабатываем отключение пользователя
        rpc.disconnect_user(client_id)

        # Flush any queued async events generated during disconnect (friends/lobby cleanup).
        try:
            pending = rpc.drain_pending_events()
        except Exception:
            pending = []
        for ev in pending or []:
            try:
                await send_event(ev.get("client_id"), ev.get("event_name"), ev.get("listener_name"), ev.get("params"))
            except Exception as e:
                logger.error(f"Failed to send queued event (disconnect): {e}")

        clients.remove(client_id)
        logger.info(f"Client removed: {client_id} (total: {clients.count})")

async def send_event(client_id: int, event_name: str, listener_name: str, params: dict):
    """Отправка события клиенту"""
    websocket = clients.get(client_id)
    if websocket:
        event = {
            "RpcResponse": None,
            "EventResponse": {
                "EventName": event_name,
                "ListenerName": listener_name,
                # IMPORTANT: Params must be a JSON array for the Unity client event parser.
                "Params": params if isinstance(params, list) else [params]
            }
        }
        try:
            await websocket.send(json.dumps(event, cls=DateTimeEncoder))
        except Exception as e:
            logger.error(f"Failed to send event to {client_id}: {e}")

async def broadcast_event(event_name: str, listener_name: str, params: dict):
    """Отправка события всем клиентам"""
    for client_id, websocket in clients.all_clients:
        await send_event(client_id, event_name, listener_name, params)

def print_banner():
    """Вывод баннера сервера"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    V2 STANDOFF SERVER                        ║
║══════════════════════════════════════════════════════════════║
║  WebSocket: ws://{HOST}:{PORT}                               ║
║  HTTP:      http://{HOST}:{HTTP_PORT}                        ║
║  Started:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                          ║
║                                                              ║
║  Services:                                                   ║
║  • V2AuthRemoteService      - Authentication                 ║
║  • HandshakeRemoteService   - Handshake                      ║
║  • PlayerRemoteService      - Player management              ║
║  • PlayerStatsRemoteService - Statistics                     ║
║  • OtherStatsRemoteService  - Ranked statistics             ║
║  • InventoryRemoteService   - Inventory                      ║
║  • FriendsRemoteService     - Friends                        ║
║  • MatchmakingRemoteService - Matchmaking                    ║
║  • GameSettingsRemoteService- Game settings                  ║
║                                                              ║
║  Press Ctrl+C to stop                                        ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

async def main():
    print_banner()
    
    # Инициализация базы данных
    try:
        db = Database(MONGODB_URI, MONGODB_DB)
        logger.info(f"Database connected: {MONGODB_DB}")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        sys.exit(1)
    
    # Передаем базу данных в RPC handler
    global rpc
    rpc = RPCHandler(clients, db)

    # Start lightweight HTTP server for bonus/promocode endpoints expected by the Unity client.
    global httpd
    try:
        httpd = ThreadingHTTPServer((HOST, HTTP_PORT), HttpHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        logger.info(f"HTTP server listening on http://{HOST}:{HTTP_PORT}")
    except Exception as e:
        logger.error(f"Failed to start HTTP server: {e}")
    
    # Настройка сервера
    # Periodic cleanup for stale lobbies (no activity + no online members).
    def lobby_cleanup_worker():
        while True:
            try:
                rpc._maybe_cleanup_lobbies()  # noqa: SLF001
            except Exception as e:
                logger.error(f"Lobby cleanup error: {e}")
            time.sleep(60)

    try:
        cleanup_thread = threading.Thread(target=lobby_cleanup_worker, daemon=True)
        cleanup_thread.start()
    except Exception as e:
        logger.error(f"Failed to start lobby cleanup worker: {e}")

    server = await websockets.serve(
        handle_client,
        HOST,
        PORT,
        ping_interval=None,  # Используем свой ping
        ping_timeout=None,
        max_size=MAX_MESSAGE_SIZE,
        compression=None
    )
    
    logger.info(f"Server listening on ws://{HOST}:{PORT}")
    
    # Graceful shutdown
    stop = asyncio.Future()
    
    def signal_handler():
        logger.info("Shutdown signal received...")
        stop.set_result(None)
    
    if sys.platform != 'win32':
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, signal_handler)
        loop.add_signal_handler(signal.SIGINT, signal_handler)
    
    try:
        await stop
    except asyncio.CancelledError:
        pass
    finally:
        server.close()
        await server.wait_closed()
        try:
            if httpd:
                httpd.shutdown()
                httpd.server_close()
        except Exception:
            pass
        logger.info("Server stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
