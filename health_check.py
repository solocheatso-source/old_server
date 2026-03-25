#!/usr/bin/env python3
"""
Health check script for V2 Standoff Server
Проверяет доступность WebSocket, HTTP серверов и MongoDB
"""

import asyncio
import websockets
import json
import sys
import os
from urllib.request import urlopen
from urllib.error import URLError
from pymongo import MongoClient

def check_mongodb(uri=None):
    """Проверка MongoDB подключения"""
    try:
        if not uri:
            uri = os.environ.get("MONGODB_URI", "mongodb://mongo:odPQUCRuWAiCqADMYBQwRecDahZgVhUN@turntable.proxy.rlwy.net:25506")
        
        print(f"Checking MongoDB: {uri[:50]}...")
        
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Проверяем соединение
        
        # Проверяем доступ к базе данных
        db_name = os.environ.get("MONGODB_DB", "v2_standoff")
        db = client[db_name]
        
        # Простой тест записи/чтения
        test_collection = db.health_check
        test_doc = {"test": True, "timestamp": "now"}
        test_collection.insert_one(test_doc)
        test_collection.delete_one({"test": True})
        
        client.close()
        print("✓ MongoDB connection OK")
        return True
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

async def check_websocket(host="localhost", port=25505):
    """Проверка WebSocket сервера"""
    try:
        uri = f"ws://{host}:{port}"
        print(f"Checking WebSocket: {uri}")
        
        async with websockets.connect(uri) as websocket:
            # Отправляем ping
            await websocket.send(bytes([1]))
            response = await websocket.recv()
            
            if response == bytes([1]):
                print("✓ WebSocket ping/pong OK")
                return True
            else:
                print("✗ WebSocket ping/pong failed")
                return False
                
    except Exception as e:
        print(f"✗ WebSocket connection failed: {e}")
        return False

def check_http(host="localhost", port=25506):
    """Проверка HTTP сервера"""
    try:
        url = f"http://{host}:{port}/standoff/inventory/promocode?id=test&promo=test"
        print(f"Checking HTTP: {url}")
        
        with urlopen(url, timeout=5) as response:
            if response.status == 200:
                print("✓ HTTP server OK")
                return True
            else:
                print(f"✗ HTTP server returned status: {response.status}")
                return False
                
    except URLError as e:
        print(f"✗ HTTP connection failed: {e}")
        return False

async def main():
    """Основная функция проверки"""
    print("V2 Standoff Server Health Check")
    print("=" * 40)
    
    # Получаем порты из переменных окружения
    ws_port = int(os.environ.get("PORT", 25505))
    http_port = int(os.environ.get("HTTP_PORT", ws_port + 1))
    
    # Проверяем серверы
    mongo_ok = check_mongodb()
    ws_ok = await check_websocket(port=ws_port)
    http_ok = check_http(port=http_port)
    
    print("=" * 40)
    if mongo_ok and ws_ok and http_ok:
        print("✓ All services are healthy")
        sys.exit(0)
    else:
        print("✗ Some services are down")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())