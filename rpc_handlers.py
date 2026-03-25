import json
import uuid
import random
import os
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from database import Database
from real_items_collection import ITEMS_DATA
from bson import ObjectId

logger = logging.getLogger("V2Server")

class DateTimeEncoder(json.JSONEncoder):
    """Кастомный JSON encoder для datetime объектов"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class RPCHandler:
    def __init__(self, clients_manager=None, database=None):
        self.db = database or Database()
        self.current_sessions = {}
        self.clients_manager = clients_manager
        self._pending_events: List[Dict[str, Any]] = []

        # In-memory cache of item definitions (id -> definition dict).
        # Helps avoid Mongo queries for every inventory action.
        self._item_definitions_cache: Dict[int, Dict[str, Any]] = {}
        self._weapon_skins_by_collection: Dict[str, List[int]] = {}
        self._last_lobby_cleanup_at: Optional[datetime] = None
        
        # Инициализируем предметы в базе данных
        self._init_items()
        
        self.services = {
            # Аутентификация
            "V2AuthRemoteService": self.handle_auth_service,
            "TestAuthRemoteService": self.handle_test_auth_service,
            "GoogleAuthRemoteService": self.handle_google_auth_service,
            "FacebookAuthRemoteService": self.handle_facebook_auth_service,
            "GameCenterAuthRemoteService": self.handle_gamecenter_auth_service,
            
            # Основные сервисы
            "HandshakeRemoteService": self.handle_handshake_service,
            "PlayerRemoteService": self.handle_player_service,
            "PlayerStatsRemoteService": self.handle_player_stats_service,
            "OtherStatsRemoteService": self.handle_other_stats_service,
            "InventoryRemoteService": self.handle_inventory_service,
            "FriendsRemoteService": self.handle_friends_service,
            "MatchmakingRemoteService": self.handle_matchmaking_service,
            "GameSettingsRemoteService": self.handle_game_settings_service,
            "StorageRemoteService": self.handle_storage_service,
            
            # Дополнительные сервисы
            "BoltRemoteService": self.handle_bolt_service,
            "AvatarRemoteService": self.handle_avatar_service,
            "ClanRemoteService": self.handle_clan_service,
            "ChatRemoteService": self.handle_chat_service,
            "AdsRemoteService": self.handle_ads_service,
            "AnalyticsRemoteService": self.handle_analytics_service,
            "MarketplaceRemoteService": self.handle_marketplace_service,
            "GameServerRemoteService": self.handle_gameserver_service,
            
            # In-App Purchase сервисы
            "GoogleInAppRemoteService": self.handle_google_inapp_service,
            "AppStoreInAppRemoteService": self.handle_appstore_inapp_service,
            "AmazonInAppRemoteService": self.handle_amazon_inapp_service,
            
            # Ultramax сервисы
            "AdminRemoteService": self.handle_admin_service,
            "PromocodeRemoteService": self.handle_promocode_service,
            "RankRemoteService": self.handle_rank_service,
        }

    def drain_pending_events(self) -> List[Dict[str, Any]]:
        """Return and clear queued remote events to be sent by the websocket layer."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def _queue_event_to_client(self, client_id: int, listener_name: str, event_name: str, params: List[Any]) -> None:
        if client_id is None:
            return
        if not isinstance(params, list):
            params = [params]
        self._pending_events.append(
            {
                "client_id": int(client_id),
                "listener_name": str(listener_name),
                "event_name": str(event_name),
                "params": params,
            }
        )

    def _queue_event_to_user(self, user_id: str, listener_name: str, event_name: str, params: List[Any]) -> None:
        if not user_id or not self.clients_manager:
            return
        try:
            client_ids = self.clients_manager.get_client_ids_by_user_id(user_id)
        except Exception:
            client_ids = []
        for cid in client_ids or []:
            self._queue_event_to_client(cid, listener_name, event_name, params)

    def _get_user_online_status(self, user: Dict[str, Any]) -> str:
        status = user.get("PlayerStatus") if isinstance(user.get("PlayerStatus"), dict) else {}
        online = status.get("OnlineStatus") or status.get("onlineStatus") or "StateOffline"
        return str(online)

    def _online_status_to_int(self, online_status: str) -> int:
        # Must match Axlebolt.Bolt.Player.OnlineStatus enum order on the client.
        mapping = {
            "StateOffline": 0,
            "StateOnline": 1,
            "StateBusy": 2,
            "StateAway": 3,
            "StateSnooze": 4,
            "StateLookingToTrade": 5,
            "StateLookingToPlay": 6,
        }
        try:
            return int(mapping.get(str(online_status or "StateOffline"), 0))
        except Exception:
            return 0

    def _build_play_in_game(self, user: Dict[str, Any]) -> Dict[str, Any]:
        # Must be compatible with Axlebolt.Bolt.Player.PlayInGame JSON deserialization (no default ctor).
        # We only need version compatibility in lobby; PhotonGame can stay null.
        game_version = str(user.get("GameVersion") or user.get("game_version") or "")
        lobby_id = str(user.get("LobbyId") or user.get("lobby_id") or "")
        return {
            "GameCode": "standoff2",
            "GameVersion": game_version,
            "LobbyId": lobby_id,
        }

    def _build_player_status(self, user: Dict[str, Any]) -> Dict[str, Any]:
        online_status = self._get_user_online_status(user)
        return {
            "OnlineStatus": online_status,
            "PlayInGame": self._build_play_in_game(user),
        }

    def _build_friend_wrapper(self, friend_user: Dict[str, Any], relationship_status: int) -> Dict[str, Any]:
        if not isinstance(friend_user, dict):
            friend_user = {}
        online_status = self._get_user_online_status(friend_user)
        online_status_int = self._online_status_to_int(online_status)
        wrapper = {
            "RelationshipStatus": int(relationship_status or 0),
            "AuthId": str(friend_user.get("AuthId") or ""),
            "Id": str(friend_user.get("Id") or ""),
            "Uid": str(friend_user.get("Uid") or ""),
            "Name": str(friend_user.get("Name") or ""),
            "AvatarId": str(friend_user.get("AvatarId") or ""),
            "AvatarVideoId": str(friend_user.get("AvatarVideoId") or ""),
            "AvatarVideoAccess": bool(friend_user.get("AvatarVideoAccess", False)),
            "RegistrationDate": int(friend_user.get("RegistrationDate", 0) or 0),
            "TimeInGame": int(friend_user.get("TimeInGame", 0) or 0),
            "PlayerStatus": self._build_player_status(friend_user),
            "OnlineStatus": online_status_int,
        }
        return wrapper

    def _notify_friends_player_status_changed(self, user_id: str) -> None:
        """Push onPlayerStatusChanged events to all online friends."""
        if not user_id:
            return
        user = self.db.get_user(user_id)
        if not user:
            return
        status_payload = self._build_player_status(user)
        # RelationshipStatus.Friend = 3 (see Axlebolt.Bolt.Friends.RelationshipStatus)
        friend_ids = self.db.get_player_friends(user_id, [3])
        for fid in friend_ids or []:
            self._queue_event_to_user(fid, "FriendsRemoteEventListener", "onPlayerStatusChanged", [user_id, status_payload])

    def _maybe_cleanup_lobbies(self) -> None:
        """
        Remove stale lobbies from MongoDB.

        A lobby is considered stale if it wasn't updated for a while AND none of its members are online.
        This also clears LobbyId for affected users to avoid "stuck in lobby" states.
        """
        try:
            now = datetime.now()
        except Exception:
            return

        # Run at most once per minute.
        try:
            if self._last_lobby_cleanup_at and (now - self._last_lobby_cleanup_at).total_seconds() < 60:
                return
        except Exception:
            pass
        self._last_lobby_cleanup_at = now

        # Consider lobby stale after 15 minutes of no updates.
        stale_before = now - timedelta(minutes=15)

        try:
            stale_lobbies = list(
                self.db.db.lobbies.find(
                    {
                        "is_active": True,
                        "$or": [
                            {"updated_at": {"$lt": stale_before}},
                            {"updated_at": {"$exists": False}},
                        ],
                    }
                )
            )
        except Exception:
            stale_lobbies = []

        for lob in stale_lobbies or []:
            try:
                lobby_id = str(lob.get("_id") or "")
            except Exception:
                lobby_id = ""
            if not lobby_id:
                continue

            members = lob.get("members") if isinstance(lob.get("members"), list) else []
            members = [str(m) for m in members if str(m)]

            if not members:
                try:
                    self.db.delete_lobby(lobby_id)
                except Exception:
                    pass
                continue

            any_online = False
            if self.clients_manager:
                for mid in members:
                    try:
                        if self.clients_manager.get_client_ids_by_user_id(mid):
                            any_online = True
                            break
                    except Exception:
                        continue

            if any_online:
                # Keep the lobby alive while any member is connected.
                try:
                    self.db.update_lobby(lobby_id, {})
                except Exception:
                    pass
                continue

            # No online members: delete lobby and clear LobbyId for members.
            try:
                self.db.delete_lobby(lobby_id)
            except Exception:
                pass
            for mid in members:
                self._set_user_lobby_id(mid, "")

    # ===== LOBBY HELPERS =====

    def _set_user_lobby_id(self, user_id: str, lobby_id: Optional[str]) -> None:
        try:
            self.db.update_user(user_id, {"LobbyId": lobby_id or ""})
        except Exception:
            pass

    def _get_user_lobby_id(self, user_id: str) -> str:
        user = self.db.get_user(user_id) or {}
        lobby_id = user.get("LobbyId") or user.get("lobby_id") or ""
        return str(lobby_id) if lobby_id else ""

    def _get_lobby_by_member(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc = self.db.db.lobbies.find_one({"is_active": True, "members": user_id})
            if not doc:
                return None
            doc["_id"] = str(doc["_id"])
            return doc
        except Exception:
            return None

    def _get_current_lobby(self, user_id: str) -> Optional[Dict[str, Any]]:
        lobby_id = self._get_user_lobby_id(user_id)
        lobby = self.db.get_lobby(lobby_id) if lobby_id else None
        if lobby and isinstance(lobby.get("members"), list) and user_id in lobby.get("members"):
            return lobby
        # Fallback: search by membership.
        lobby = self._get_lobby_by_member(user_id)
        if lobby:
            self._set_user_lobby_id(user_id, lobby.get("_id"))
        return lobby

    def _leave_lobby_server_side(self, user_id: str) -> None:
        """Remove user from current lobby without an explicit client RPC (disconnect cleanup)."""
        if not user_id:
            return
        lobby = self._get_current_lobby(user_id)
        if not lobby:
            self._set_user_lobby_id(user_id, "")
            return

        lobby_id = str(lobby.get("_id") or "")
        if not lobby_id:
            self._set_user_lobby_id(user_id, "")
            return

        members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
        members = [str(m) for m in members if str(m)]

        if user_id in members:
            members.remove(user_id)

        owner_id = str(lobby.get("owner_id") or "")
        owner_changed = False
        new_owner_id = owner_id
        if owner_id == user_id and members:
            new_owner_id = members[0]
            owner_changed = True

        # Persist changes.
        self._set_user_lobby_id(user_id, "")
        if not members:
            try:
                self.db.delete_lobby(lobby_id)
            except Exception:
                pass
            return

        try:
            self.db.update_lobby(lobby_id, {"members": members, "owner_id": new_owner_id, "current_members": len(members)})
        except Exception:
            pass

        # Notify remaining members.
        for mid in members:
            self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onPlayerLeftLobby", [user_id])
        if owner_changed:
            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onLobbyOwnerChanged", [new_owner_id])

    def _lobby_type_to_name(self, lobby_type: int) -> str:
        # Must match BoltLobby.LobbyType enum names on the client.
        return {
            0: "Private",
            1: "FriendsOnly",
            2: "Public",
            3: "Invisible",
        }.get(int(lobby_type or 0), "Private")

    def _build_bolt_photon_game(self, region: str, room_id: str, app_version: str) -> Dict[str, Any]:
        return {
            "Region": str(region or ""),
            "RoomId": str(room_id or ""),
            "AppVersion": str(app_version or ""),
            "CustomProperties": {},
        }

    def _build_lobby_wrapper(self, lobby: Dict[str, Any], viewer_user_id: str) -> Dict[str, Any]:
        lobby_id = str(lobby.get("_id") or lobby.get("Id") or "")
        name = str(lobby.get("name") or lobby.get("Name") or "Lobby")
        lobby_type = int(lobby.get("type", 0) or 0)
        max_members = int(lobby.get("max_members", lobby.get("maxMembers", 10)) or 10)
        joinable = bool(lobby.get("joinable", True))
        owner_id = str(lobby.get("owner_id") or lobby.get("LobbyOwnerId") or "")
        data = lobby.get("data") if isinstance(lobby.get("data"), dict) else {}
        members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
        invites = lobby.get("invites") if isinstance(lobby.get("invites"), list) else []

        member_wrappers: List[Dict[str, Any]] = []
        for mid in members:
            mid = str(mid)
            u = self.db.get_user(mid)
            if not u:
                continue
            rel = self.db.get_friend_status(viewer_user_id, mid)
            member_wrappers.append(self._build_friend_wrapper(u, rel))

        invite_wrappers: List[Dict[str, Any]] = []
        for inv in invites:
            invited_id = ""
            if isinstance(inv, dict):
                invited_id = str(inv.get("player_id") or "")
            else:
                invited_id = str(inv or "")
            if not invited_id:
                continue
            u = self.db.get_user(invited_id)
            if not u:
                continue
            rel = self.db.get_friend_status(viewer_user_id, invited_id)
            invite_wrappers.append(self._build_friend_wrapper(u, rel))

        photon_game = None
        pg = lobby.get("photon_game")
        if isinstance(pg, dict):
            photon_game = {
                "Region": str(pg.get("Region") or pg.get("region") or ""),
                "RoomId": str(pg.get("RoomId") or pg.get("roomId") or pg.get("room_id") or ""),
                "AppVersion": str(pg.get("AppVersion") or pg.get("appVersion") or ""),
                "CustomProperties": pg.get("CustomProperties") if isinstance(pg.get("CustomProperties"), dict) else {},
            }

        game_server = None
        gs = lobby.get("game_server")
        if isinstance(gs, dict):
            game_server = {
                "Id": str(gs.get("Id") or gs.get("id") or ""),
                "IP": str(gs.get("IP") or gs.get("ip") or ""),
                "Port": int(gs.get("Port") or gs.get("port") or 0),
            }

        return {
            "Id": lobby_id,
            "LobbyOwnerId": owner_id,
            "Name": name,
            "Type": lobby_type,
            "Joinable": joinable,
            "MaxMembers": max_members,
            "Data": {str(k): str(v) for k, v in (data or {}).items()},
            "LobbyMembers": member_wrappers,
            "LobbyInvites": invite_wrappers,
            "GameServer": game_server,
            "PhotonGame": photon_game,
        }
    
    def _init_items(self):
        """Инициализация предметов в базе данных"""
        try:
            normalized_items = self._normalize_item_definitions(ITEMS_DATA)
            self.db.init_item_definitions(normalized_items)

            # Refresh caches from the normalized definitions.
            self._item_definitions_cache = {}
            self._weapon_skins_by_collection = {}
            for item in normalized_items:
                if not isinstance(item, dict):
                    continue
                item_id = item.get("Id")
                if item_id is None:
                    continue
                try:
                    item_id_int = int(item_id)
                except Exception:
                    continue
                self._item_definitions_cache[item_id_int] = item

                if item.get("Type") == "weapon":
                    props = item.get("Properties") if isinstance(item.get("Properties"), dict) else {}
                    collection = props.get("collection")
                    if collection and collection != "None":
                        self._weapon_skins_by_collection.setdefault(str(collection), []).append(item_id_int)
        except Exception as e:
            logger.exception("Failed to init items: %s", e)

    def _normalize_item_definitions(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize/patch item definitions on the server:
        - All collection packs (boxes) cost 10000 gold (currency 102).
        - Boxes get a `contains` property listing ALL weapon skins of that collection.
        - All knives and gloves are Arcane; Nameless collection skins/knives are Nameless.

        Applied before inserting definitions into MongoDB.
        """
        normalized: List[Dict[str, Any]] = []
        weapon_skins_by_collection: Dict[str, List[int]] = {}

        # First pass: deep-copy and collect weapon skins by collection.
        for item in items or []:
            if not isinstance(item, dict):
                continue

            new_item = dict(item)
            new_item["BuyPrice"] = dict(item.get("BuyPrice") or {}) if isinstance(item.get("BuyPrice"), dict) else {}
            new_item["SellPrice"] = dict(item.get("SellPrice") or {}) if isinstance(item.get("SellPrice"), dict) else {}
            new_item["Properties"] = dict(item.get("Properties") or {}) if isinstance(item.get("Properties"), dict) else {}

            props = new_item["Properties"]
            collection = props.get("collection")
            if new_item.get("Type") == "weapon" and collection and collection != "None":
                try:
                    weapon_skins_by_collection.setdefault(str(collection), []).append(int(new_item.get("Id")))
                except Exception:
                    pass

            normalized.append(new_item)

        # Second pass: patch prices/contains/rarities.
        for item in normalized:
            props = item.get("Properties") or {}
            collection_raw = props.get("collection")
            collection = str(collection_raw) if collection_raw is not None else ""
            collection_lower = collection.lower()
            item_type = item.get("Type")
            item_id = item.get("Id")

            # Collection packs: make all boxes cost 10000 GOLD (102) and list their contents.
            is_box = item_type == "box"
            try:
                if isinstance(item_id, int) and 400 <= item_id <= 499:
                    is_box = True
            except Exception:
                pass

            if is_box:
                item["BuyPrice"] = {"102": 10000}
                item["SellPrice"] = {"102": 5000}
                if collection and collection != "None":
                    contained = weapon_skins_by_collection.get(collection, [])
                    props["contains"] = ",".join(str(x) for x in sorted(set(contained)))

            # Rarity rules via `Properties.value` used by the client.
            if item_type == "gloves":
                props["value"] = str(6)  # Arcane

            if item_type == "knife":
                props["value"] = str(7 if collection_lower == "nameless" else 6)

            if item_type == "weapon" and collection_lower == "nameless":
                props["value"] = str(7)  # Nameless

        return normalized

    def _get_or_create_player_inventory(self, user_id: str) -> Dict[str, Any]:
        inventory = self.db.get_player_inventory(user_id)
        if not inventory:
            inventory = {
                "PlayerInventory": {},
                "PlayerCurrencies": {
                    # CurrencyId.Coins = 101, CurrencyId.Gold = 102, CurrencyId.ForceCoin = 103
                    "101": 50000,
                    "102": 5000,
                    "103": 0
                }
            }
            self.db.create_player_inventory(user_id, inventory)

        if "PlayerInventory" not in inventory or not isinstance(inventory.get("PlayerInventory"), dict):
            inventory["PlayerInventory"] = {}
        if "PlayerCurrencies" not in inventory or not isinstance(inventory.get("PlayerCurrencies"), dict):
            inventory["PlayerCurrencies"] = {"101": 0, "102": 0, "103": 0}
        else:
            currencies = inventory["PlayerCurrencies"]
            if "101" not in currencies and 101 not in currencies:
                currencies["101"] = 0
            if "102" not in currencies and 102 not in currencies:
                currencies["102"] = 0
            if "103" not in currencies and 103 not in currencies:
                currencies["103"] = 0
            inventory["PlayerCurrencies"] = currencies

        # Normalize items structure to match what the Unity client expects.
        self._normalize_player_inventory_items(inventory)
        return inventory

    def _normalize_player_inventory_items(self, inventory: Dict[str, Any]) -> None:
        player_inventory = inventory.get("PlayerInventory")
        if not isinstance(player_inventory, dict):
            return

        changed = False
        for k, item in list(player_inventory.items()):
            if not isinstance(item, dict):
                continue

            # Ensure required fields exist.
            if "Id" not in item:
                try:
                    item["Id"] = int(k)
                except Exception:
                    item["Id"] = 0
                changed = True
            if "Definition" not in item or not isinstance(item.get("Definition"), dict):
                definition_id = item.get("ItemDefinitionId", 0)
                try:
                    definition_id = int(definition_id)
                except Exception:
                    definition_id = 0
                item["Definition"] = {"Id": definition_id}
                changed = True
            if "Quantity" not in item:
                item["Quantity"] = 1
                changed = True
            if "Flags" not in item:
                item["Flags"] = 0
                changed = True
            if "Date" not in item:
                item["Date"] = int(datetime.now().timestamp())
                changed = True
            if "EquippedCt" not in item:
                item["EquippedCt"] = False
                changed = True
            if "EquippedTr" not in item:
                item["EquippedTr"] = False
                changed = True

            # ItemProperties are frequently accessed by the client; never leave null.
            if "ItemProperties" not in item or not isinstance(item.get("ItemProperties"), dict):
                item["ItemProperties"] = {"Properties": {}, "ChangedProperties": {}}
                changed = True
            else:
                ip = item["ItemProperties"]
                if "Properties" not in ip or not isinstance(ip.get("Properties"), dict):
                    ip["Properties"] = {}
                    changed = True
                if "ChangedProperties" not in ip or not isinstance(ip.get("ChangedProperties"), dict):
                    ip["ChangedProperties"] = {}
                    changed = True
                item["ItemProperties"] = ip

            player_inventory[k] = item

        if changed:
            inventory["PlayerInventory"] = player_inventory

    def _save_player_inventory(self, user_id: str, inventory: Dict[str, Any]) -> None:
        # Keep mongo-friendly string keys.
        if isinstance(inventory.get("PlayerInventory"), dict):
            inventory["PlayerInventory"] = {str(k): v for k, v in inventory["PlayerInventory"].items()}
        if isinstance(inventory.get("PlayerCurrencies"), dict):
            inventory["PlayerCurrencies"] = {str(k): v for k, v in inventory["PlayerCurrencies"].items()}
        self.db.update_player_inventory(user_id, inventory)

    def _generate_inventory_item_id(self, player_inventory: Dict[str, Any]) -> int:
        existing_ids = set()
        for k in (player_inventory or {}).keys():
            try:
                existing_ids.add(int(k))
            except Exception:
                continue
        while True:
            new_id = random.randint(100000, 999999)
            if new_id not in existing_ids:
                return new_id

    def _add_inventory_item(self, inventory: Dict[str, Any], definition_id: int, quantity: int = 1) -> Dict[str, Any]:
        player_inventory = inventory.get("PlayerInventory", {})
        new_item_id = self._generate_inventory_item_id(player_inventory)
        item = {
            "Id": new_item_id,
            "Definition": {"Id": int(definition_id)},
            "Quantity": int(quantity),
            "Flags": 0,
            "Date": int(datetime.now().timestamp()),
            "EquippedCt": False,
            "EquippedTr": False,
            "ItemProperties": {"Properties": {}, "ChangedProperties": {}}
        }
        player_inventory[str(new_item_id)] = item
        inventory["PlayerInventory"] = player_inventory
        return item

    def _get_item_definition_id_from_inventory_item(self, item: Dict[str, Any]) -> int:
        if not isinstance(item, dict):
            return 0
        definition = item.get("Definition")
        if isinstance(definition, dict) and "Id" in definition:
            try:
                return int(definition.get("Id") or 0)
            except Exception:
                return 0
        if "ItemDefinitionId" in item:
            try:
                return int(item.get("ItemDefinitionId") or 0)
            except Exception:
                return 0
        return 0

    def _get_skin_value_from_definition(self, definition: Dict[str, Any]) -> int:
        props = definition.get("Properties") if isinstance(definition, dict) else None
        value_raw = props.get("value") if isinstance(props, dict) else None
        try:
            value_int = int(value_raw)
        except Exception:
            value_int = 1
        return max(1, min(7, value_int))

    def _get_sell_gold_amount(self, definition: Dict[str, Any]) -> int:
        # Must match client-side InventoryManager.GetItemCostGold(SkinValue).
        value_int = self._get_skin_value_from_definition(definition)
        return {
            1: 10,   # Common
            2: 20,   # Uncommon
            3: 30,   # Rare
            4: 40,   # Epic
            5: 50,   # Legendary
            6: 80,   # Arcane
            7: 130,  # Nameless
        }.get(value_int, 0)

    def _is_sell_supported_definition(self, definition: Dict[str, Any]) -> bool:
        if not isinstance(definition, dict):
            return False
        t = str(definition.get("Type") or "").lower()
        if t in ("case", "box", "gift", "badge", "frame"):
            return False
        props = definition.get("Properties") if isinstance(definition.get("Properties"), dict) else {}
        collection = str(props.get("collection") or "").lower()
        if collection in ("purple_kill", "new_chance"):
            return False
        return True

    def _parse_escaped_json_object(self, maybe_escaped: str) -> Any:
        if maybe_escaped is None:
            return None
        s = str(maybe_escaped)
        if not s:
            return None
        # The client sends JSON through Utils.EscapeJson (no surrounding quotes).
        try:
            unescaped = json.loads(f"\"{s}\"")
            return json.loads(unescaped)
        except Exception:
            try:
                return json.loads(s)
            except Exception:
                return None

    # ===== PROMOCODES =====

    def activate_promocode(self, user_id: str, promo_code: str) -> str:
        """
        Activate promocode for a user.

        Returns:
        - "notfound" / "limit" / "error" strings for UI, OR
        - JSON array string of inventory operations compatible with BoltInventoryService.ProcessPromocodeResult().
        """
        code = str(promo_code or "").strip().upper()
        if not code or not user_id:
            return "notfound"

        promo = self.db.get_promocode(code)
        if not promo:
            return "notfound"
        if promo.get("active") is False:
            return "notfound"

        expires_at = promo.get("expires_at") or promo.get("ExpiresAt")
        try:
            if isinstance(expires_at, datetime) and expires_at <= datetime.now():
                return "notfound"
        except Exception:
            pass

        try:
            max_uses = int(promo.get("max_uses") or promo.get("MaxUses") or 0)
            uses = int(promo.get("uses") or promo.get("Uses") or 0)
        except Exception:
            max_uses = 0
            uses = 0
        if max_uses and uses >= max_uses:
            return "limit"

        # Per-user limit (default 1).
        try:
            per_user_limit = int(promo.get("per_user_limit") or promo.get("PerUserLimit") or 1)
        except Exception:
            per_user_limit = 1
        per_user_limit = max(1, per_user_limit)

        # This server currently enforces only 1 redemption per user (per_user_limit > 1 can be added later).
        if self.db.has_promocode_redemption(code, user_id):
            return "limit"

        # Reserve redemption first (unique index prevents races).
        if not self.db.record_promocode_redemption(code, user_id):
            return "limit"

        try:
            rewards = promo.get("rewards") or promo.get("Rewards") or {}
            if not isinstance(rewards, dict):
                rewards = {}

            currencies = rewards.get("currencies") or rewards.get("Currencies") or {}
            items = rewards.get("items") or rewards.get("Items") or []
            items_many = rewards.get("items_many") or rewards.get("ItemsMany") or []

            operations: List[Dict[str, Any]] = []
            inventory = self._get_or_create_player_inventory(user_id)

            if isinstance(currencies, dict):
                for cid_raw, amt_raw in currencies.items():
                    try:
                        cid = int(cid_raw)
                        amt = int(amt_raw)
                    except Exception:
                        continue
                    if amt == 0:
                        continue
                    self._currency_add(inventory, cid, float(amt))
                    operations.append({"OperationType": "Currency", "OperationData": {str(cid): int(amt)}})

            def add_item(definition_id: int) -> None:
                new_item = self._add_inventory_item(inventory, int(definition_id), 1)
                try:
                    skin_id = int(new_item.get("Id") or 0)
                except Exception:
                    skin_id = 0
                operations.append({"OperationType": "Add", "OperationData": {"SkinId": skin_id, "Id": int(definition_id)}})

            if isinstance(items, list):
                for def_id_raw in items:
                    try:
                        def_id = int(def_id_raw)
                    except Exception:
                        continue
                    add_item(def_id)

            if isinstance(items_many, list):
                for entry in items_many:
                    if not isinstance(entry, dict):
                        continue
                    def_id_raw = entry.get("Id") or entry.get("DefinitionId") or entry.get("definition_id") or entry.get("id")
                    qty_raw = entry.get("Quantity") or entry.get("quantity") or 1
                    try:
                        def_id = int(def_id_raw)
                        qty = int(qty_raw)
                    except Exception:
                        continue
                    qty = max(1, min(100, qty))
                    for _ in range(qty):
                        add_item(def_id)

            # If a promocode is configured with no actual rewards, treat it as not found to avoid "success" on empty ops.
            if not operations:
                try:
                    self.db.db.promocode_redemptions.delete_one({"code": code, "user_id": user_id})
                except Exception:
                    pass
                return "notfound"

            self._save_player_inventory(user_id, inventory)
            self.db.increment_promocode_use(code)

            return json.dumps(operations, ensure_ascii=False)
        except Exception:
            # Rollback redemption reservation.
            try:
                self.db.db.promocode_redemptions.delete_one({"code": code, "user_id": user_id})
            except Exception:
                pass
            return "error"

    def _remove_inventory_item(self, inventory: Dict[str, Any], inventory_item_id: int, quantity: int = 1) -> bool:
        player_inventory = inventory.get("PlayerInventory", {})
        key = str(inventory_item_id)
        item = player_inventory.get(key)
        if not isinstance(item, dict):
            return False

        current_qty = int(item.get("Quantity", 1) or 1)
        remove_qty = int(quantity or 1)
        if current_qty > remove_qty:
            item["Quantity"] = current_qty - remove_qty
            player_inventory[key] = item
        else:
            player_inventory.pop(key, None)

        inventory["PlayerInventory"] = player_inventory
        return True

    def _currency_get(self, inventory: Dict[str, Any], currency_id: int) -> float:
        currencies = inventory.get("PlayerCurrencies", {})
        try:
            return float(currencies.get(str(currency_id), currencies.get(currency_id, 0)) or 0)
        except Exception:
            return 0.0

    def _currency_add(self, inventory: Dict[str, Any], currency_id: int, amount: float) -> None:
        currencies = inventory.get("PlayerCurrencies", {})
        current = self._currency_get(inventory, currency_id)
        currencies[str(currency_id)] = current + float(amount or 0)
        inventory["PlayerCurrencies"] = currencies

    def _currency_subtract(self, inventory: Dict[str, Any], currency_id: int, amount: float) -> bool:
        current = self._currency_get(inventory, currency_id)
        amount_f = float(amount or 0)
        if current < amount_f:
            return False
        self._currency_add(inventory, currency_id, -amount_f)
        return True

    def _weighted_choice(self, candidates: List[int]) -> int:
        if not candidates:
            raise ValueError("No candidates")
        weights: List[float] = []
        for definition_id in candidates:
            definition = self._item_definitions_cache.get(int(definition_id)) or {}
            props = definition.get("Properties") if isinstance(definition, dict) else None
            value_raw = props.get("value") if isinstance(props, dict) else None
            try:
                value_int = int(value_raw)
            except Exception:
                value_int = 1
            # Client roulette uses (7 - value)^2 which makes Nameless (7) weight 0.
            # Use (8 - value)^2 on the server so Nameless stays obtainable (very rare).
            clamped = max(0, min(7, value_int))
            w = max(1, (8 - clamped) ** 2)
            weights.append(w)
        return random.choices(candidates, weights=weights, k=1)[0]
    
    def get_current_user_id(self, client_id: int = None) -> str:
        """Получить ID текущего пользователя"""
        if client_id and self.clients_manager:
            user_id = self.clients_manager.get_user_id(client_id)
            if user_id:
                return user_id
        return "demo_user_123"
    
    def handle(self, service_name: str, method_name: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Главный обработчик RPC запросов"""
        try:
            self._maybe_cleanup_lobbies()
        except Exception:
            pass
        if service_name in self.services:
            return self.services[service_name](method_name, params, client_id)
        else:
            return {
                "Return": None,
                "Exception": {
                    "Id": "ServiceNotFound",
                    "Code": 404,
                    "Message": f"Service {service_name} not found",
                    "Params": {}
                }
            }
    
    # ===== АУТЕНТИФИКАЦИЯ =====
    
    # ===== STATS DEFAULTS / NORMALIZATION =====

    _DOTNET_INT_SPLIT_MOD = 2147483647

    _SUPPORTED_STATS_GAME_MODES = ("deathmatch", "defuse")

    # Must match `WeaponId.ToString().ToLower()` from the Unity client.
    _WEAPON_STAT_NAMES = (
        "hands",
        "handsknife",
        "g22",
        "usp",
        "p350",
        "tec9",
        "fiveseven",
        "berettas",
        "watergun",
        "fnfal",
        "deagle",
        "ump45",
        "mp7",
        "p90",
        "mp5",
        "mac10",
        "m4a1",
        "akr",
        "akr12",
        "m4",
        "m16",
        "famas",
        "awm",
        "m40",
        "m110",
        "sm1014",
        "fabm",
        "spas",
        "val",
        "knife",
        "knifebayonet",
        "knifekarambit",
        "jkommando",
        "knifebutterfly",
        "flipknife",
        "kunaiknife",
        "knifefang",
        "knifesting",
        "dildo",
        "grenadehe",
        "grenadesmoke",
        "grenadeflash",
        "bomb",
        "defusekit",
        "vest",
        "vestandhelmet",
        "bat",
        "grenadesnowball",
        "scorpionknife",
        "daggerknife",
        "knifekukri",
        "knifetanto",
        "knifestilet",
    )

    def _dotnet_utc_seconds(self) -> int:
        """Mimic Unity's `DateTimeOffset.UtcNow.Ticks / 10000000` (seconds since 0001-01-01)."""
        return int((datetime.utcnow() - datetime(1, 1, 1)).total_seconds())

    def _split_long_to_int_parts(self, value: int) -> List[int]:
        part1 = int(value % self._DOTNET_INT_SPLIT_MOD)
        part2 = int(value // self._DOTNET_INT_SPLIT_MOD)
        return [part1, part2]

    def _normalize_flat_str_dict(self, data: Any) -> Dict[str, str]:
        if not isinstance(data, dict):
            return {}
        normalized: Dict[str, str] = {}
        for k, v in data.items():
            if k is None or v is None:
                continue
            normalized[str(k)] = str(v)
        return normalized

    def _merge_defaults(self, current: Dict[str, str], defaults: Dict[str, str]) -> bool:
        changed = False
        for k, v in defaults.items():
            if k not in current:
                current[k] = v
                changed = True
        return changed

    def _get_default_player_stats(self) -> Dict[str, str]:
        stats: Dict[str, str] = {
            "level_xp": "0",
            "level_id": "0",
        }

        # Per-mode aggregate stats used by PlayerStatsExtension.
        for mode in self._SUPPORTED_STATS_GAME_MODES:
            stats[f"{mode}_kills"] = "0"
            stats[f"{mode}_deaths"] = "0"
            stats[f"{mode}_assists"] = "0"
            stats[f"{mode}_shots"] = "0"
            stats[f"{mode}_hits"] = "0"
            stats[f"{mode}_headshots"] = "0"
            stats[f"{mode}_damage"] = "0"
            stats[f"{mode}_games_played"] = "0"

        # Per-weapon stats used by PlayerStatsExtension.
        for mode in self._SUPPORTED_STATS_GAME_MODES:
            for weapon in self._WEAPON_STAT_NAMES:
                stats[f"gun_{mode}_{weapon}_kills"] = "0"
                stats[f"gun_{mode}_{weapon}_shots"] = "0"
                stats[f"gun_{mode}_{weapon}_hits"] = "0"
                stats[f"gun_{mode}_{weapon}_headshots"] = "0"
                stats[f"gun_{mode}_{weapon}_damage"] = "0"

        return stats

    def _get_default_other_stats(self) -> Dict[str, str]:
        # Ranked/matchmaking stats queried during startup.
        # NOTE: These MUST be strings because Unity parses JSON into Dictionary<string, string>.
        now_parts = self._split_long_to_int_parts(self._dotnet_utc_seconds())

        return {
            "ranked_rank": "0",
            "ranked_current_mmr": "1000",
            "ranked_target_mmr": "1000",
            "ranked_played_matches": "0",
            "ranked_calibration_status": "0",
            "ranked_calibration_match_count": "0",
            "ranked_calibration_won_match_count": "0",
            "ranked_won_matches": "0",
            "ranked_ban_code": "-1",
            "ranked_ban_duration": "0",
            "ranked_banned_match_no": "0",
            "ranked_last_activity_time1": str(now_parts[0]),
            "ranked_last_activity_time2": str(now_parts[1]),
            "ranked_last_match_status": "3",
            # Kept for backward compatibility / debugging.
            "ranked_season_id": "1",
        }

    def _make_external_user_id(self, provider: str, raw: Any) -> str:
        """
        Build a stable, short AuthId for external providers (Google/Facebook/GameCenter/etc).

        We intentionally hash the incoming token/code to:
        - avoid storing long tokens in DB keys
        - keep AuthId stable for the same credential
        """
        provider_s = str(provider or "").strip().lower() or "ext"
        raw_s = str(raw or "").strip()
        if not raw_s:
            return ""
        digest = hashlib.sha256(raw_s.encode("utf-8", errors="ignore")).hexdigest()[:32]
        return f"{provider_s}:{digest}"

    def _issue_ticket_for_user(
        self,
        user_id: str,
        version: Any = None,
        hash_val: Any = None,
        client_id: int = None,
        email: Optional[str] = None,
    ) -> Dict[str, Any]:
        user_id = str(user_id or "").strip()
        if not user_id:
            return {
                "Return": None,
                "Exception": {"Id": "AuthFailed", "Code": 401, "Message": "Invalid credentials", "Params": {}},
            }

        # Maintenance mode (SettingsMain.maintenance_mode = true).
        settings_main = self.db.get_settings_main() or {}
        maintenance_enabled = bool(settings_main.get("maintenance_mode") or settings_main.get("MaintenanceMode"))
        tester_accounts = settings_main.get("tester_accounts") or settings_main.get("TesterAccounts") or []
        if not isinstance(tester_accounts, list) or len(tester_accounts) == 0:
            # Fallback to local game_settings.json if DB doesn't provide a whitelist.
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                candidates = [
                    os.path.join(base_dir, "game_settings.json"),
                    os.path.join(base_dir, "..", "game_settings.json"),
                    "game_settings.json",
                ]
                settings_path = next((p for p in candidates if os.path.exists(p)), None)
                if settings_path:
                    with open(settings_path, "r", encoding="utf-8") as f:
                        file_settings = json.load(f) or {}
                    file_testers = file_settings.get("tester_accounts") or []
                    if isinstance(file_testers, list):
                        tester_accounts = file_testers
            except Exception:
                tester_accounts = []

        if maintenance_enabled and user_id not in tester_accounts:
            return {
                "Return": None,
                "Exception": {
                    "Id": "MaintenanceMode",
                    "Code": 503,
                    "Message": "Server is under maintenance",
                    "Params": {},
                },
            }

        # Ban check.
        ban = self.db.get_active_ban(user_id)
        if ban:
            expires_at = ban.get("expires_at")
            message = ban.get("reason") or "You are banned"
            params_out: Dict[str, str] = {}
            if expires_at is not None:
                try:
                    params_out["expires_at"] = expires_at.isoformat() if hasattr(expires_at, "isoformat") else str(expires_at)
                except Exception:
                    params_out["expires_at"] = str(expires_at)
            return {
                "Return": None,
                "Exception": {"Id": "Banned", "Code": 403, "Message": message, "Params": params_out},
            }

        user = self.db.get_user(user_id)
        if not user:
            uid_length = random.choice([8, 9])
            uid = "".join([str(random.randint(0, 9)) for _ in range(uid_length)])

            user_email = str(email or "").strip() or f"{user_id}@v2.local"
            user_data = {
                "Id": str(uuid.uuid4()),
                "Uid": uid,
                "AuthId": user_id,
                "Email": user_email,
                "Name": "Player",
                "AvatarId": "",
                "AvatarVideoId": "",
                "AvatarVideoAccess": False,
                "GameVersion": str(version) if version is not None else "",
                "GameHash": str(hash_val) if hash_val is not None else "",
                "TimeInGame": 0,
                "RegistrationDate": int(datetime.now().timestamp()),
                "PlayerStatus": {"OnlineStatus": "StateOnline", "PlayInGame": None},
            }

            self.db.create_user(user_id, user_data)
            user = user_data
        else:
            self.db.update_user(
                user_id,
                {
                    "GameVersion": str(version) if version is not None else user.get("GameVersion", ""),
                    "GameHash": str(hash_val) if hash_val is not None else user.get("GameHash", ""),
                    "PlayerStatus": {"OnlineStatus": "StateOnline", "PlayInGame": None},
                },
            )

        ticket = str(uuid.uuid4())
        self.db.create_session(ticket, user_id)
        self.current_sessions[ticket] = user_id

        if client_id and self.clients_manager:
            self.clients_manager.set_user_id(client_id, user_id)

        # Notify online friends about status change.
        self._notify_friends_player_status_changed(user_id)

        return {"Return": ticket, "Exception": None}

    def handle_auth_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка V2 аутентификации"""
        if method == "auth":
            login = str(params[0]) if params else ""
            password = str(params[1]) if len(params) > 1 else ""
            version = params[2] if len(params) > 2 else ""
            hash_val = params[3] if len(params) > 3 else ""

            if not login or not password:
                return {
                    "Return": None,
                    "Exception": {"Id": "AuthFailed", "Code": 401, "Message": "Invalid credentials", "Params": {}},
                }

            user_id = str(login)
            return self._issue_ticket_for_user(user_id, version, hash_val, client_id)
        
        return {
            "Return": None,
            "Exception": {
                "Id": "MethodNotImplemented",
                "Code": 404,
                "Message": f"V2AuthRemoteService.{method} is not implemented",
                "Params": {}
            }
        }
    
    def handle_test_auth_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Auth service used in Unity editor / test builds."""
        if method == "auth":
            auth_id = str(params[0]) if params else ""
            email = str(params[1]) if len(params) > 1 else ""
            version = params[2] if len(params) > 2 else ""
            hash_val = params[3] if len(params) > 3 else ""

            user_id = str(auth_id or "").strip()
            if not user_id:
                return {
                    "Return": None,
                    "Exception": {"Id": "AuthFailed", "Code": 401, "Message": "Invalid credentials", "Params": {}},
                }

            # Keep AuthId stable and namespaced to avoid collisions with V2 credentials.
            user_id = self._make_external_user_id("test", user_id) or user_id
            return self._issue_ticket_for_user(user_id, version, hash_val, client_id, email=email)

        return {
            "Return": None,
            "Exception": {
                "Id": "MethodNotImplemented",
                "Code": 404,
                "Message": f"TestAuthRemoteService.{method} is not implemented",
                "Params": {},
            },
        }

    def handle_google_auth_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка Google аутентификации"""
        if method == "auth":
            token = params[0] if params else ""
            version = params[1] if len(params) > 1 else ""
            hash_val = params[2] if len(params) > 2 else ""
            user_id = self._make_external_user_id("google", token)
            return self._issue_ticket_for_user(user_id, version, hash_val, client_id)

        if method in ("protoAuth", "encryptedAuth"):
            auth = params[0] if params else {}
            verification = params[1] if len(params) > 1 else {}

            auth_code = ""
            version = ""
            if isinstance(auth, dict):
                auth_code = auth.get("AuthCode") or auth.get("authCode") or ""
                version = auth.get("GameVersion") or auth.get("gameVersion") or ""

            hash_val = ""
            if isinstance(verification, dict):
                hash_val = verification.get("Hash") or verification.get("hash") or ""

            user_id = self._make_external_user_id("google", auth_code)
            return self._issue_ticket_for_user(user_id, version, hash_val, client_id)

        return {
            "Return": None,
            "Exception": {
                "Id": "MethodNotImplemented",
                "Code": 404,
                "Message": f"GoogleAuthRemoteService.{method} is not implemented",
                "Params": {},
            },
        }
    
    def handle_facebook_auth_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка Facebook аутентификации"""
        if method == "auth":
            # Signature: (gameId, gameVersion, platform, token)
            _game_id = params[0] if params else ""
            version = params[1] if len(params) > 1 else ""
            _platform = params[2] if len(params) > 2 else 0
            token = params[3] if len(params) > 3 else ""
            _ = (_game_id, _platform)
            user_id = self._make_external_user_id("facebook", token)
            return self._issue_ticket_for_user(user_id, version, "", client_id)

        if method in ("protoAuth", "encryptedAuth"):
            auth = params[0] if params else {}
            verification = params[1] if len(params) > 1 else {}

            token = ""
            version = ""
            if isinstance(auth, dict):
                token = auth.get("Token") or auth.get("token") or ""
                version = auth.get("GameVersion") or auth.get("gameVersion") or ""

            hash_val = ""
            if isinstance(verification, dict):
                hash_val = verification.get("Hash") or verification.get("hash") or ""

            user_id = self._make_external_user_id("facebook", token)
            return self._issue_ticket_for_user(user_id, version, hash_val, client_id)

        return {
            "Return": None,
            "Exception": {
                "Id": "MethodNotImplemented",
                "Code": 404,
                "Message": f"FacebookAuthRemoteService.{method} is not implemented",
                "Params": {},
            },
        }
    
    def handle_gamecenter_auth_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка GameCenter аутентификации"""
        if method == "auth":
            return {"Return": str(uuid.uuid4()), "Exception": None}
        return {"Return": None, "Exception": None}
    
    # ===== HANDSHAKE =====
    
    def handle_handshake_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка handshake"""
        if method == "handshake":
            return {"Return": "OK", "Exception": None}
        
        elif method == "secureHandshake":
            return {"Return": "OK", "Exception": None}
        
        elif method == "logout":
            user_id = self.get_current_user_id(client_id)
            if user_id:
                self.db.update_user(user_id, {
                    "PlayerStatus": {
                        "OnlineStatus": "StateOffline",
                        "PlayInGame": None
                    }
                })
            return {"Return": "OK", "Exception": None}
        
        return {"Return": None, "Exception": None}
    
    # ===== PLAYER SERVICE =====
    
    def handle_player_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка игрока"""
        user_id = self.get_current_user_id(client_id)
        
        if method == "getPlayer":
            user = self.db.get_user(user_id)
            if user:
                user_copy = user.copy()
                user_copy.pop('created_at', None)
                user_copy.pop('updated_at', None)
                return {"Return": json.dumps(user_copy, cls=DateTimeEncoder), "Exception": None}
            else:
                return {"Return": None, "Exception": {"Id": "UserNotFound", "Code": 404, "Message": "User not found"}}
        
        elif method == "setPlayerName":
            new_name = params[0] if params else "Player"
            self.db.update_user(user_id, {"Name": new_name})
            return {"Return": "OK", "Exception": None}
        
        elif method == "setPlayerAvatar":
            avatar_id = str(uuid.uuid4())
            self.db.update_user(user_id, {"AvatarId": avatar_id})
            return {"Return": avatar_id, "Exception": None}
        
        elif method == "setPlayerAvatarVideoId":
            video_id = params[0] if params else ""
            self.db.update_user(user_id, {"AvatarVideoId": video_id})
            return {"Return": "OK", "Exception": None}
        
        elif method == "setPlayerFirebaseToken":
            token = params[0] if params else ""
            self.db.update_user(user_id, {"FirebaseToken": token})
            return {"Return": "OK", "Exception": None}
        
        elif method == "setOnlineStatus":
            self.db.update_user(user_id, {"PlayerStatus": {"OnlineStatus": "StateOnline", "PlayInGame": None}})
            return {"Return": "OK", "Exception": None}
        
        elif method == "setAwayStatus":
            self.db.update_user(user_id, {"PlayerStatus": {"OnlineStatus": "StateAway", "PlayInGame": None}})
            return {"Return": "OK", "Exception": None}
        
        return {"Return": None, "Exception": None}
    
    # ===== PLAYER STATS SERVICE =====
    
    def handle_player_stats_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка статистики игрока"""
        user_id = self.get_current_user_id(client_id)
        
        if method == "getStats":
            stats = self._normalize_flat_str_dict(self.db.get_player_stats(user_id))
            defaults = self._get_default_player_stats()

            if not stats:
                stats = defaults
                self.db.create_player_stats(user_id, dict(stats))
            else:
                changed = self._merge_defaults(stats, defaults)
                if changed:
                    self.db.update_player_stats(user_id, dict(stats))

            return {"Return": json.dumps(stats, cls=DateTimeEncoder), "Exception": None}

        if method in ("storeStats", "updateStats"):
            new_stats = self._normalize_flat_str_dict(params[0] if params else {})
            current_stats = self._normalize_flat_str_dict(self.db.get_player_stats(user_id))
            defaults = self._get_default_player_stats()

            # Ensure base keys exist so client-side IncrementStat/GetIntStat won't throw later.
            self._merge_defaults(current_stats, defaults)

            if new_stats:
                current_stats.update(new_stats)

            self.db.update_player_stats(user_id, dict(current_stats))
            return {"Return": "OK", "Exception": None}

        if method == "resetAllStats":
            stats = self._get_default_player_stats()
            self.db.update_player_stats(user_id, dict(stats))
            return {"Return": "OK", "Exception": None}
        
        return {"Return": None, "Exception": None}
    
    # ===== OTHER STATS SERVICE =====
    
    def handle_other_stats_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка дополнительной статистики"""
        user_id = self.get_current_user_id(client_id)
        
        if method == "getStats":
            other_stats = self._normalize_flat_str_dict(self.db.get_other_stats(user_id))
            defaults = self._get_default_other_stats()

            # Backward compatibility: older server stored a single unix timestamp in `ranked_last_activity_time`.
            legacy_changed = False
            if (
                ("ranked_last_activity_time1" not in other_stats or "ranked_last_activity_time2" not in other_stats)
                and "ranked_last_activity_time" in other_stats
            ):
                try:
                    unix_ts = int(other_stats["ranked_last_activity_time"])
                    if 0 < unix_ts < 10_000_000_000:
                        dt = datetime.utcfromtimestamp(unix_ts)
                        dotnet_seconds = int((dt - datetime(1, 1, 1)).total_seconds())
                        p1, p2 = self._split_long_to_int_parts(dotnet_seconds)

                        if "ranked_last_activity_time1" not in other_stats:
                            other_stats["ranked_last_activity_time1"] = str(p1)
                            legacy_changed = True
                        if "ranked_last_activity_time2" not in other_stats:
                            other_stats["ranked_last_activity_time2"] = str(p2)
                            legacy_changed = True
                except Exception:
                    pass

            if not other_stats:
                other_stats = defaults
                self.db.create_other_stats(user_id, dict(other_stats))
            else:
                changed = self._merge_defaults(other_stats, defaults) or legacy_changed
                if changed:
                    self.db.update_other_stats(user_id, dict(other_stats))

            return {"Return": json.dumps(other_stats, cls=DateTimeEncoder), "Exception": None}
        
        return {"Return": None, "Exception": None}
    
    # ===== INVENTORY SERVICE =====
    
    def handle_inventory_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка инвентаря"""
        user_id = self.get_current_user_id(client_id)
        
        if method == "getPlayerInventory":
            inventory = self._get_or_create_player_inventory(user_id)
            return {"Return": json.dumps(inventory, cls=DateTimeEncoder), "Exception": None}
        
        elif method == "getInventoryItemDefinitions":
            # Return definitions in the exact shape the client expects (BoltInventoryItemDefinition).
            raw_definitions = self.db.get_item_definitions()
            definitions: Dict[int, Dict[str, Any]] = {}

            for item_id, item in raw_definitions.items():
                buy_price = item.get("BuyPrice") if isinstance(item, dict) else None
                sell_price = item.get("SellPrice") if isinstance(item, dict) else None
                props = item.get("Properties") if isinstance(item, dict) else None

                definitions[int(item_id)] = {
                    "Id": int(item.get("Id", item_id)),
                    "DisplayName": item.get("DisplayName", ""),
                    "BuyPrice": {int(k): float(v) for k, v in (buy_price or {}).items()} if isinstance(buy_price, dict) else {},
                    "SellPrice": {int(k): float(v) for k, v in (sell_price or {}).items()} if isinstance(sell_price, dict) else {},
                    "Properties": {str(k): str(v) for k, v in (props or {}).items()} if isinstance(props, dict) else {},
                    "CanBeTraded": bool(item.get("CanBeTraded", item.get("Tradable", False))),
                }

            return {"Return": definitions, "Exception": None}

        elif method == "getInventoryItemPropertyDefinitions":
            # Not currently used by the client (code is commented out), but must never be null.
            return {"Return": [], "Exception": None}
        
        elif method == "buyInventoryItem":
            # Signature: (definitionId, quantity, currencyId, toManyItems)
            definition_id = int(params[0]) if params else 0
            quantity = int(params[1]) if len(params) > 1 else 1
            currency_id = int(params[2]) if len(params) > 2 else 0
            to_many_items = bool(params[3]) if len(params) > 3 else False

            if definition_id <= 0 or quantity <= 0:
                return {"Return": None, "Exception": {"Id": "InvalidArguments", "Code": 400, "Message": "Invalid buy arguments", "Params": {}}}

            definition = self._item_definitions_cache.get(definition_id) or self.db.get_item_definition(definition_id) or {}
            buy_price = definition.get("BuyPrice") if isinstance(definition, dict) else None
            price_raw = None
            if isinstance(buy_price, dict):
                price_raw = buy_price.get(str(currency_id), buy_price.get(currency_id))
            try:
                price = float(price_raw)
            except Exception:
                return {"Return": None, "Exception": {"Id": "ItemNotForSale", "Code": 400, "Message": f"Item {definition_id} is not for sale for currency {currency_id}", "Params": {}}}

            total_cost = price * float(quantity)
            inventory = self._get_or_create_player_inventory(user_id)
            if not self._currency_subtract(inventory, currency_id, total_cost):
                return {"Return": None, "Exception": {"Id": "InsufficientFunds", "Code": 402, "Message": "Not enough currency", "Params": {}}}

            new_items: List[Dict[str, Any]] = []
            if to_many_items:
                for _ in range(quantity):
                    new_items.append(self._add_inventory_item(inventory, definition_id, 1))
            else:
                new_items.append(self._add_inventory_item(inventory, definition_id, quantity))

            self._save_player_inventory(user_id, inventory)
            return {"Return": new_items, "Exception": None}

        elif method == "buyCollectionOffer":
            # Signature: (collectionName, quantity, currencyId, toManyItems)
            collection = str(params[0]) if params else ""
            quantity = int(params[1]) if len(params) > 1 else 1
            currency_id = int(params[2]) if len(params) > 2 else 0
            to_many_items = bool(params[3]) if len(params) > 3 else False

            # Find a box (pack) for this collection (Properties.collection match).
            box_definition_id = None
            for def_id, definition in self._item_definitions_cache.items():
                if not isinstance(definition, dict) or definition.get("Type") != "box":
                    continue
                props = definition.get("Properties") if isinstance(definition.get("Properties"), dict) else {}
                if str(props.get("collection", "")).lower() == collection.lower():
                    box_definition_id = int(def_id)
                    break

            if not box_definition_id:
                return {"Return": None, "Exception": {"Id": "CollectionOfferNotFound", "Code": 404, "Message": f"Collection offer not found: {collection}", "Params": {}}}

            return self.handle_inventory_service("buyInventoryItem", [box_definition_id, quantity, currency_id, to_many_items], client_id)

        elif method == "exchangeInventoryItems":
            # Signature: (recipeCode, currencies, inventoryItemIds)
            recipe_code = str(params[0]) if params else ""
            currencies = params[1] if len(params) > 1 else {}
            inventory_item_ids = params[2] if len(params) > 2 else []

            if not isinstance(currencies, dict):
                currencies = {}
            if not isinstance(inventory_item_ids, list):
                inventory_item_ids = []

            inventory = self._get_or_create_player_inventory(user_id)

            # Apply input costs (currencies/items).
            for k, v in currencies.items():
                try:
                    cid = int(k)
                    amount = float(v)
                except Exception:
                    continue
                if amount > 0 and not self._currency_subtract(inventory, cid, amount):
                    return {"Return": None, "Exception": {"Id": "InsufficientFunds", "Code": 402, "Message": "Not enough currency for exchange", "Params": {}}}

            for inv_item_id in inventory_item_ids:
                try:
                    inv_item_id_int = int(inv_item_id)
                except Exception:
                    continue
                if not self._remove_inventory_item(inventory, inv_item_id_int, 1):
                    return {"Return": None, "Exception": {"Id": "InventoryItemNotFound", "Code": 404, "Message": f"Inventory item not found: {inv_item_id_int}", "Params": {}}}

            result_items: List[Dict[str, Any]] = []
            result_currencies: Dict[int, float] = {}

            # Open case/box (roulette).
            if recipe_code.startswith("RECIPE_V2_"):
                try:
                    case_def_id = int(recipe_code.split("RECIPE_V2_", 1)[1])
                except Exception:
                    case_def_id = 0

                case_def = self._item_definitions_cache.get(case_def_id) or self.db.get_item_definition(case_def_id)
                if not isinstance(case_def, dict):
                    return {"Return": None, "Exception": {"Id": "CaseNotFound", "Code": 404, "Message": f"Case definition not found: {case_def_id}", "Params": {}}}

                props = case_def.get("Properties") if isinstance(case_def.get("Properties"), dict) else {}
                contains_raw = props.get("contains")
                candidates: List[int] = []
                if isinstance(contains_raw, str) and contains_raw.strip():
                    for part in contains_raw.split(","):
                        part = part.strip()
                        if not part:
                            continue
                        try:
                            candidates.append(int(part))
                        except Exception:
                            continue
                else:
                    collection = str(props.get("collection", "") or "")
                    is_box = case_def.get("Type") == "box"
                    try:
                        if 400 <= int(case_def_id) <= 499:
                            is_box = True
                    except Exception:
                        pass

                    if collection and collection != "None":
                        if is_box:
                            candidates = list(self._weapon_skins_by_collection.get(collection, []))
                        else:
                            # Default case contents: rare+ skins of this collection (plus knives/gloves if present).
                            for def_id, defn in self._item_definitions_cache.items():
                                if not isinstance(defn, dict):
                                    continue
                                p = defn.get("Properties") if isinstance(defn.get("Properties"), dict) else {}
                                if str(p.get("collection", "")) != collection:
                                    continue
                                t = defn.get("Type")
                                if t not in ("weapon", "knife", "gloves"):
                                    continue
                                try:
                                    vv = int(p.get("value", 0))
                                except Exception:
                                    vv = 0
                                if t in ("knife", "gloves") or vv >= 3:
                                    candidates.append(int(def_id))

                if not candidates:
                    return {"Return": None, "Exception": {"Id": "CaseEmpty", "Code": 500, "Message": "No items configured for this case/box", "Params": {}}}

                try:
                    reward_definition_id = self._weighted_choice(candidates)
                except Exception as e:
                    return {"Return": None, "Exception": {"Id": "RewardError", "Code": 500, "Message": str(e), "Params": {}}}

                result_items.append(self._add_inventory_item(inventory, reward_definition_id, 1))

            # Persist and build result.
            self._save_player_inventory(user_id, inventory)
            currencies_payload: Dict[int, float] = {}
            for cid, amt in result_currencies.items():
                currencies_payload[int(cid)] = float(amt)

            return {
                "Return": {
                    "InventoryItems": result_items,
                    "Currencies": currencies_payload
                },
                "Exception": None
            }

        elif method == "sellInventoryItem":
            # Overloads:
            # - SellInventoryItem(int inventoryItemId) -> BoltInventoryResult
            # - SellInventoryItem(int, int, int) -> InventoryItem (legacy)
            if len(params) >= 3:
                # Legacy proto-style: (inventoryItemId, quantity, _unused)
                inv_item_id = int(params[0]) if params else 0
                quantity = int(params[1]) if len(params) > 1 else 1
                inventory = self._get_or_create_player_inventory(user_id)
                player_inventory = inventory.get("PlayerInventory", {})
                item = player_inventory.get(str(inv_item_id))
                if not isinstance(item, dict):
                    return {"Return": None, "Exception": {"Id": "InventoryItemNotFound", "Code": 404, "Message": f"Inventory item not found: {inv_item_id}", "Params": {}}}

                definition_id = self._get_item_definition_id_from_inventory_item(item)
                self._remove_inventory_item(inventory, inv_item_id, quantity)
                self._save_player_inventory(user_id, inventory)

                remaining = inventory.get("PlayerInventory", {}).get(str(inv_item_id))
                remaining_qty = int(remaining.get("Quantity", 0) or 0) if isinstance(remaining, dict) else 0
                proto = {
                    "Id": int(inv_item_id),
                    "ItemDefinitionId": int(definition_id),
                    "Quantity": int(remaining_qty),
                    "Flags": int(item.get("Flags", 0) or 0),
                    "Date": int(item.get("Date", int(datetime.now().timestamp())) or 0),
                    "Properties": {},
                }
                return {"Return": proto, "Exception": None}

            inv_item_id = int(params[0]) if params else 0
            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})
            item = player_inventory.get(str(inv_item_id))
            if not isinstance(item, dict):
                return {"Return": None, "Exception": {"Id": "InventoryItemNotFound", "Code": 404, "Message": f"Inventory item not found: {inv_item_id}", "Params": {}}}

            definition_id = self._get_item_definition_id_from_inventory_item(item)
            definition = self._item_definitions_cache.get(definition_id) or self.db.get_item_definition(definition_id) or {}
            if not self._is_sell_supported_definition(definition):
                return {"Return": None, "Exception": {"Id": "SellNotSupported", "Code": 400, "Message": "This item cannot be sold", "Params": {}}}

            try:
                qty = int(item.get("Quantity", 1) or 1)
            except Exception:
                qty = 1
            gold_amount = float(self._get_sell_gold_amount(definition) * max(1, qty))

            # Remove the full stack.
            self._remove_inventory_item(inventory, inv_item_id, qty)
            self._currency_add(inventory, 102, gold_amount)
            self._save_player_inventory(user_id, inventory)

            return {
                "Return": {
                    "InventoryItems": [],
                    "Currencies": {102: gold_amount}
                },
                "Exception": None
            }

        elif method == "sellInventoryItems":
            item_ids = params[0] if params else []
            if not isinstance(item_ids, list):
                item_ids = []
            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})

            total_gold = 0.0
            # Validate first to keep operation atomic-ish.
            resolved: List[Dict[str, Any]] = []
            for raw_id in item_ids:
                try:
                    inv_item_id = int(raw_id)
                except Exception:
                    continue
                item = player_inventory.get(str(inv_item_id))
                if not isinstance(item, dict):
                    return {"Return": None, "Exception": {"Id": "InventoryItemNotFound", "Code": 404, "Message": f"Inventory item not found: {inv_item_id}", "Params": {}}}
                definition_id = self._get_item_definition_id_from_inventory_item(item)
                definition = self._item_definitions_cache.get(definition_id) or self.db.get_item_definition(definition_id) or {}
                if not self._is_sell_supported_definition(definition):
                    return {"Return": None, "Exception": {"Id": "SellNotSupported", "Code": 400, "Message": "This item cannot be sold", "Params": {}}}
                try:
                    qty = int(item.get("Quantity", 1) or 1)
                except Exception:
                    qty = 1
                gold = float(self._get_sell_gold_amount(definition) * max(1, qty))
                resolved.append({"inv_item_id": inv_item_id, "qty": qty, "gold": gold})

            for r in resolved:
                self._remove_inventory_item(inventory, int(r["inv_item_id"]), int(r["qty"]))
                total_gold += float(r["gold"])

            if total_gold:
                self._currency_add(inventory, 102, total_gold)
            self._save_player_inventory(user_id, inventory)

            return {
                "Return": {
                    "InventoryItems": [],
                    "Currencies": {102: total_gold}
                },
                "Exception": None
            }

        elif method == "consumeInventoryItem":
            inv_item_id = int(params[0]) if params else 0
            quantity = int(params[1]) if len(params) > 1 else 1
            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})
            item = player_inventory.get(str(inv_item_id))
            if not isinstance(item, dict):
                return {"Return": None, "Exception": {"Id": "InventoryItemNotFound", "Code": 404, "Message": f"Inventory item not found: {inv_item_id}", "Params": {}}}

            definition_id = self._get_item_definition_id_from_inventory_item(item)
            flags = int(item.get("Flags", 0) or 0)
            date_val = int(item.get("Date", int(datetime.now().timestamp())) or 0)

            self._remove_inventory_item(inventory, inv_item_id, quantity)
            remaining = inventory.get("PlayerInventory", {}).get(str(inv_item_id))
            remaining_qty = int(remaining.get("Quantity", 0) or 0) if isinstance(remaining, dict) else 0
            self._save_player_inventory(user_id, inventory)

            proto = {
                "Id": int(inv_item_id),
                "ItemDefinitionId": int(definition_id),
                "Quantity": int(remaining_qty),
                "Flags": flags,
                "Date": date_val,
                "Properties": {},
            }
            return {"Return": proto, "Exception": None}

        elif method == "transferInventoryItems":
            from_item_id = int(params[0]) if params else 0
            to_item_id = int(params[1]) if len(params) > 1 else 0
            quantity = int(params[2]) if len(params) > 2 else 0
            if quantity <= 0:
                return {"Return": [], "Exception": None}

            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})
            from_item = player_inventory.get(str(from_item_id))
            to_item = player_inventory.get(str(to_item_id))
            if not isinstance(from_item, dict) or not isinstance(to_item, dict):
                return {"Return": None, "Exception": {"Id": "InventoryItemNotFound", "Code": 404, "Message": "Inventory item not found", "Params": {}}}

            from_def_id = self._get_item_definition_id_from_inventory_item(from_item)
            to_def_id = self._get_item_definition_id_from_inventory_item(to_item)

            try:
                from_qty = int(from_item.get("Quantity", 1) or 1)
            except Exception:
                from_qty = 1
            if from_qty < quantity:
                return {"Return": None, "Exception": {"Id": "InsufficientQuantity", "Code": 400, "Message": "Not enough quantity", "Params": {}}}

            # Apply transfer.
            self._remove_inventory_item(inventory, from_item_id, quantity)
            to_item = inventory.get("PlayerInventory", {}).get(str(to_item_id)) or to_item
            try:
                to_qty = int(to_item.get("Quantity", 1) or 1)
            except Exception:
                to_qty = 1
            to_item["Quantity"] = to_qty + quantity
            inventory["PlayerInventory"][str(to_item_id)] = to_item
            self._save_player_inventory(user_id, inventory)

            updated_items: List[Dict[str, Any]] = []
            # Return updated TO item (and FROM if still exists).
            updated_items.append({
                "Id": int(to_item_id),
                "ItemDefinitionId": int(to_def_id),
                "Quantity": int(to_item.get("Quantity", 0) or 0),
                "Flags": int(to_item.get("Flags", 0) or 0),
                "Date": int(to_item.get("Date", int(datetime.now().timestamp())) or 0),
                "Properties": {},
            })
            remaining_from = inventory.get("PlayerInventory", {}).get(str(from_item_id))
            if isinstance(remaining_from, dict):
                updated_items.append({
                    "Id": int(from_item_id),
                    "ItemDefinitionId": int(from_def_id),
                    "Quantity": int(remaining_from.get("Quantity", 0) or 0),
                    "Flags": int(remaining_from.get("Flags", 0) or 0),
                    "Date": int(remaining_from.get("Date", int(datetime.now().timestamp())) or 0),
                    "Properties": {},
                })
            return {"Return": updated_items, "Exception": None}

        elif method == "setInventoryItemFlags":
            flags_map = params[0] if params else {}
            if not isinstance(flags_map, dict):
                return {"Return": "OK", "Exception": None}
            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})
            for raw_item_id, raw_flags in flags_map.items():
                try:
                    item_id = int(raw_item_id)
                    flags = int(raw_flags)
                except Exception:
                    continue
                item = player_inventory.get(str(item_id))
                if isinstance(item, dict):
                    item["Flags"] = flags
                    player_inventory[str(item_id)] = item
            inventory["PlayerInventory"] = player_inventory
            self._save_player_inventory(user_id, inventory)
            return {"Return": "OK", "Exception": None}

        elif method == "setSkinItemEquipped":
            equipped_map = params[0] if params else {}
            if not isinstance(equipped_map, dict):
                return {"Return": "OK", "Exception": None}
            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})
            for raw_item_id, raw_equipped in equipped_map.items():
                try:
                    item_id = int(raw_item_id)
                except Exception:
                    continue
                ct = False
                tr = False
                if isinstance(raw_equipped, list) and len(raw_equipped) >= 2:
                    ct = bool(raw_equipped[0])
                    tr = bool(raw_equipped[1])
                item = player_inventory.get(str(item_id))
                if isinstance(item, dict):
                    item["EquippedCt"] = ct
                    item["EquippedTr"] = tr
                    player_inventory[str(item_id)] = item
            inventory["PlayerInventory"] = player_inventory
            self._save_player_inventory(user_id, inventory)
            return {"Return": "OK", "Exception": None}

        elif method == "setInventoryItemsProperties":
            raw_json = str(params[0]) if params else ""
            data = self._parse_escaped_json_object(raw_json)
            if not isinstance(data, dict):
                return {"Return": "OK", "Exception": None}
            inventory = self._get_or_create_player_inventory(user_id)
            player_inventory = inventory.get("PlayerInventory", {})
            for raw_item_id, prop in data.items():
                try:
                    item_id = int(raw_item_id)
                except Exception:
                    continue
                item = player_inventory.get(str(item_id))
                if not isinstance(item, dict):
                    continue
                if "ItemProperties" not in item or not isinstance(item.get("ItemProperties"), dict):
                    item["ItemProperties"] = {"Properties": {}, "ChangedProperties": {}}
                ip = item["ItemProperties"]
                if "Properties" not in ip or not isinstance(ip.get("Properties"), dict):
                    ip["Properties"] = {}
                if isinstance(prop, dict):
                    name = prop.get("Name")
                    if isinstance(name, str) and name:
                        ip["Properties"][name] = prop
                item["ItemProperties"] = ip
                player_inventory[str(item_id)] = item
            inventory["PlayerInventory"] = player_inventory
            self._save_player_inventory(user_id, inventory)
            return {"Return": "OK", "Exception": None}
        
        return {
            "Return": None,
            "Exception": {
                "Id": "MethodNotImplemented",
                "Code": 404,
                "Message": f"InventoryRemoteService.{method} is not implemented",
                "Params": {}
            }
        }
    
    # ===== FRIENDS SERVICE =====
    
    def handle_friends_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка друзей"""
        user_id = self.get_current_user_id(client_id)

        def parse_statuses(raw) -> List[int]:
            if raw is None:
                return []
            if isinstance(raw, list):
                out: List[int] = []
                for x in raw:
                    try:
                        out.append(int(x))
                    except Exception:
                        continue
                return out
            try:
                return [int(raw)]
            except Exception:
                return []

        # RelationshipStatus enum (Axlebolt.Bolt.Friends.RelationshipStatus)
        REL_NONE = 0
        REL_BLOCKED = 1
        REL_REQUEST_RECIPIENT = 2
        REL_FRIEND = 3
        REL_REQUEST_INITIATOR = 4
        REL_IGNORED = 5

        if method == "getPlayerFriendsIds":
            relationship_statuses = parse_statuses(params[0] if params else [REL_FRIEND])
            friends = self.db.get_player_friends(user_id, relationship_statuses)
            return {"Return": json.dumps(friends or []), "Exception": None}

        if method == "getPlayerFriendsCount":
            relationship_statuses = parse_statuses(params[0] if params else [REL_FRIEND])
            records = self.db.get_player_friend_records(user_id, relationship_statuses)
            return {"Return": int(len(records or [])), "Exception": None}

        if method == "getPlayerFriends":
            relationship_statuses = parse_statuses(params[0] if params else [REL_FRIEND])
            records = self.db.get_player_friend_records(user_id, relationship_statuses)
            wrappers: List[Dict[str, Any]] = []
            for rec in records or []:
                fid = str(rec.get("friend_id") or "")
                st = int(rec.get("status", REL_NONE) or REL_NONE)
                friend_user = self.db.get_user(fid)
                if friend_user:
                    friend_user.pop("created_at", None)
                    friend_user.pop("updated_at", None)
                    wrappers.append(self._build_friend_wrapper(friend_user, st))
            return {"Return": json.dumps(wrappers, ensure_ascii=False), "Exception": None}

        if method == "getPlayerFriendById":
            player_id = str(params[0]) if params else ""
            friend_user = self.db.get_user(player_id)
            if not friend_user:
                return {"Return": "{}", "Exception": None}
            friend_user.pop("created_at", None)
            friend_user.pop("updated_at", None)
            rel = self.db.get_friend_status(user_id, player_id)
            wrapper = self._build_friend_wrapper(friend_user, rel)
            return {"Return": json.dumps(wrapper, ensure_ascii=False), "Exception": None}

        if method == "getPlayersCount":
            search_value = str(params[0]) if params else ""
            try:
                count = int(self.db.count_users(search_value))
            except Exception:
                count = 0
            return {"Return": count, "Exception": None}

        if method == "getOnlineStatus":
            player_id = str(params[0]) if params else ""
            player = self.db.get_user(player_id)
            if not player:
                return {"Return": "StateOffline", "Exception": None}
            return {"Return": self._get_user_online_status(player), "Exception": None}

        if method == "getAvatars":
            return {"Return": [], "Exception": None}

        if method == "sendFriendRequest":
            friend_id = str(params[0]) if params else ""
            if not friend_id or friend_id == user_id:
                return {"Return": REL_NONE, "Exception": None}
            if not self.db.get_user(friend_id):
                return {"Return": None, "Exception": {"Id": "PlayerNotFound", "Code": 404, "Message": "Player not found", "Params": {}}}

            current_status = self.db.get_friend_status(user_id, friend_id)
            if current_status in (REL_FRIEND, REL_BLOCKED, REL_REQUEST_RECIPIENT, REL_REQUEST_INITIATOR):
                return {"Return": int(current_status), "Exception": None}

            # Sender sees recipient as RequestRecipient; recipient sees sender as RequestInitiator.
            self.db.update_friend_status(user_id, friend_id, REL_REQUEST_RECIPIENT)
            self.db.update_friend_status(friend_id, user_id, REL_REQUEST_INITIATOR)

            sender_user = self.db.get_user(user_id) or {}
            sender_wrapper = self._build_friend_wrapper(sender_user, REL_REQUEST_INITIATOR)
            self._queue_event_to_user(friend_id, "FriendsRemoteEventListener", "onNewFriendshipRequest", [sender_wrapper])
            return {"Return": REL_REQUEST_RECIPIENT, "Exception": None}

        if method == "acceptFriendRequest":
            friend_id = str(params[0]) if params else ""
            if not friend_id or friend_id == user_id:
                return {"Return": REL_NONE, "Exception": None}

            # Update both sides to Friend.
            self.db.update_friend_status(user_id, friend_id, REL_FRIEND)
            self.db.update_friend_status(friend_id, user_id, REL_FRIEND)

            # Notify the initiator so their friends list updates in real-time.
            accepter_user = self.db.get_user(user_id) or {}
            initiator_user = self.db.get_user(friend_id) or {}
            accepter_wrapper = self._build_friend_wrapper(accepter_user, REL_FRIEND)
            initiator_wrapper = self._build_friend_wrapper(initiator_user, REL_FRIEND)
            self._queue_event_to_user(friend_id, "FriendsRemoteEventListener", "onFriendAdded", [accepter_wrapper])
            # Safe to also notify the accepter; if already added locally, TryAdd will fail silently.
            self._queue_event_to_user(user_id, "FriendsRemoteEventListener", "onFriendAdded", [initiator_wrapper])
            return {"Return": REL_FRIEND, "Exception": None}

        if method == "ignoreFriendRequest":
            friend_id = str(params[0]) if params else ""
            if friend_id:
                self.db.update_friend_status(user_id, friend_id, REL_IGNORED)
                # Initiator no longer has a pending request.
                self.db.update_friend_status(friend_id, user_id, REL_NONE)
            return {"Return": REL_NONE, "Exception": None}

        if method == "revokeFriendRequest":
            friend_id = str(params[0]) if params else ""
            if friend_id:
                self.db.update_friend_status(user_id, friend_id, REL_NONE)
                self.db.update_friend_status(friend_id, user_id, REL_NONE)
                # Notify recipient to drop the incoming request.
                self._queue_event_to_user(friend_id, "FriendsRemoteEventListener", "onRevokeFriendshipRequest", [user_id])
            return {"Return": REL_NONE, "Exception": None}

        if method == "removeFriend":
            friend_id = str(params[0]) if params else ""
            if friend_id:
                self.db.remove_friend(user_id, friend_id)
                self.db.remove_friend(friend_id, user_id)
                # Notify the other side only (the caller updates locally and may crash on duplicate event).
                self._queue_event_to_user(friend_id, "FriendsRemoteEventListener", "onFriendRemoved", [user_id])
            return {"Return": REL_NONE, "Exception": None}

        if method == "blockFriend":
            friend_id = str(params[0]) if params else ""
            if friend_id:
                self.db.update_friend_status(user_id, friend_id, REL_BLOCKED)
                # Other side no longer sees this as friend.
                self.db.update_friend_status(friend_id, user_id, REL_NONE)
                self._queue_event_to_user(friend_id, "FriendsRemoteEventListener", "onFriendRemoved", [user_id])
            return {"Return": REL_BLOCKED, "Exception": None}

        if method == "unblockFriend":
            friend_id = str(params[0]) if params else ""
            if friend_id:
                self.db.update_friend_status(user_id, friend_id, REL_NONE)
            return {"Return": REL_NONE, "Exception": None}

        if method == "searchPlayers":
            search_value = str(params[0]) if params else ""
            page = int(params[1]) if len(params) > 1 else 0
            size = int(params[2]) if len(params) > 2 else 10
            _ = page  # paging not implemented server-side yet

            search_results = self.db.search_users(search_value, size)
            wrappers: List[Dict[str, Any]] = []
            for u in search_results or []:
                u.pop("created_at", None)
                u.pop("updated_at", None)
                auth_id = str(u.get("AuthId") or "")
                if not auth_id:
                    continue
                rel = self.db.get_friend_status(user_id, auth_id)
                wrappers.append(self._build_friend_wrapper(u, rel))
            return {"Return": json.dumps(wrappers, ensure_ascii=False), "Exception": None}

        if method == "getPlayerById":
            player_id = str(params[0]) if params else ""
            player = self.db.get_user(player_id)
            if not player:
                return {"Return": None, "Exception": {"Id": "PlayerNotFound", "Code": 404, "Message": "Player not found", "Params": {}}}
            player.pop("created_at", None)
            player.pop("updated_at", None)
            # Return Axlebolt.Bolt.Protobuf.Player shape.
            return {
                "Return": {
                    "Id": str(player.get("AuthId") or player_id),
                    "Uid": str(player.get("Uid") or ""),
                    "Name": str(player.get("Name") or ""),
                    "AvatarId": str(player.get("AvatarId") or ""),
                    "TimeInGame": int(player.get("TimeInGame", 0) or 0),
                    "PlayerStatus": {
                        "PlayerId": str(player.get("AuthId") or player_id),
                        "PlayInGame": None,
                        "OnlineStatus": self._get_user_online_status(player),
                    },
                    "LogoutDate": 0,
                    "RegistrationDate": int(player.get("RegistrationDate", 0) or 0),
                },
                "Exception": None,
            }

        return {"Return": None, "Exception": None}
    
    # ===== MATCHMAKING SERVICE =====
    
    def handle_matchmaking_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка матчмейкинга"""
        user_id = self.get_current_user_id(client_id)

        def exc(code: int, ex_id: str, message: str) -> Dict[str, Any]:
            return {"Return": None, "Exception": {"Id": ex_id, "Code": int(code), "Message": message, "Params": {}}}

        # RpcException codes (Axlebolt.Bolt.Api.Exception.*)
        EX_LOBBY_NOT_FOUND = 5001
        EX_NOT_LOBBY_OWNER = 5002
        EX_NOT_LOBBY_MEMBER = 5003
        EX_NOT_IN_LOBBY = 5004
        EX_LOBBY_JOIN_RESTRICTED = 5005
        EX_LOBBY_IS_FULL = 5006
        EX_INCORRECT_PARAM = 5007

        def now_ms() -> int:
            try:
                return int(datetime.utcnow().timestamp() * 1000)
            except Exception:
                return 0

        if method == "createLobby":
            name = str(params[0]) if params else "Lobby"
            lobby_type = int(params[1]) if len(params) > 1 else 2  # Public
            max_members = int(params[2]) if len(params) > 2 else 10
            max_members = max(2, min(10, max_members))

            lobby_data = {
                "name": name,
                "type": lobby_type,
                "max_members": max_members,
                "joinable": True,
                "owner_id": user_id,
                "is_active": True,
                "members": [user_id],
                "invites": [],
                "data": {},
                "photon_game": None,
                "game_server": None,
            }
            lobby_id = self.db.create_lobby(lobby_data)
            if not lobby_id:
                return exc(500, "LobbyCreateFailed", "Failed to create lobby")

            self._set_user_lobby_id(user_id, lobby_id)
            lobby = self.db.get_lobby(lobby_id) or dict(lobby_data, **{"_id": lobby_id})
            return {"Return": self._build_lobby_wrapper(lobby, user_id), "Exception": None}

        if method == "getLobby":
            lobby_id = str(params[0]) if params else ""
            lobby = self.db.get_lobby(lobby_id)
            if not lobby or not lobby.get("is_active", True):
                return exc(EX_LOBBY_NOT_FOUND, "LobbyNotFound", "Lobby not found")
            return {"Return": self._build_lobby_wrapper(lobby, user_id), "Exception": None}

        if method == "joinLobby":
            lobby_id = str(params[0]) if params else ""
            lobby = self.db.get_lobby(lobby_id)
            if not lobby or not lobby.get("is_active", True):
                return exc(EX_LOBBY_NOT_FOUND, "LobbyNotFound", "Lobby not found")

            joinable = bool(lobby.get("joinable", True))
            if not joinable:
                return exc(EX_LOBBY_JOIN_RESTRICTED, "LobbyJoinRestricted", "Lobby is not joinable")

            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            max_members = int(lobby.get("max_members", 10) or 10)
            if user_id not in members and len(members) >= max_members:
                return exc(EX_LOBBY_IS_FULL, "LobbyIsFull", "Lobby is full")

            invites = lobby.get("invites") if isinstance(lobby.get("invites"), list) else []
            invited_ids = set()
            for inv in invites:
                if isinstance(inv, dict):
                    invited_ids.add(str(inv.get("player_id") or ""))
                else:
                    invited_ids.add(str(inv))

            lobby_type = int(lobby.get("type", 0) or 0)
            owner_id = str(lobby.get("owner_id") or "")

            # Restrict joining for non-public lobbies.
            if lobby_type in (0, 1) and user_id not in invited_ids and user_id != owner_id:
                if lobby_type == 1:
                    # FriendsOnly: require friendship with owner.
                    if self.db.get_friend_status(owner_id, user_id) != 3 and self.db.get_friend_status(user_id, owner_id) != 3:
                        return exc(EX_LOBBY_JOIN_RESTRICTED, "LobbyJoinRestricted", "Lobby join restricted")
                else:
                    return exc(EX_LOBBY_JOIN_RESTRICTED, "LobbyJoinRestricted", "Lobby join restricted")

            is_new_member = False
            if user_id not in members:
                members = list(members) + [user_id]
                is_new_member = True

            # Remove invite after join.
            new_invites: List[Any] = []
            for inv in invites:
                invited = str(inv.get("player_id") or "") if isinstance(inv, dict) else str(inv)
                if invited != user_id:
                    new_invites.append(inv)

            self.db.update_lobby(lobby_id, {"members": members, "invites": new_invites, "current_members": len(members)})
            self._set_user_lobby_id(user_id, lobby_id)

            lobby = self.db.get_lobby(lobby_id) or lobby
            result = {"Return": self._build_lobby_wrapper(lobby, user_id), "Exception": None}

            # Notify existing members about the new player.
            if is_new_member:
                new_user = self.db.get_user(user_id) or {}
                new_wrapper = self._build_friend_wrapper(new_user, self.db.get_friend_status(user_id, user_id))
                for mid in members:
                    mid = str(mid)
                    if mid and mid != user_id:
                        self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onNewPlayerJoinedLobby", [new_wrapper])

            return result

        if method == "leaveLobby":
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return {"Return": "OK", "Exception": None}

            lobby_id = str(lobby.get("_id") or "")
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            members = [str(m) for m in members if str(m)]
            if user_id in members:
                members.remove(user_id)

            owner_id = str(lobby.get("owner_id") or "")
            owner_changed = False
            new_owner_id = owner_id
            if owner_id == user_id and members:
                new_owner_id = members[0]
                owner_changed = True

            # Persist changes.
            self._set_user_lobby_id(user_id, "")
            if not members:
                self.db.delete_lobby(lobby_id)
                return {"Return": "OK", "Exception": None}
            self.db.update_lobby(lobby_id, {"members": members, "owner_id": new_owner_id, "current_members": len(members)})

            # Notify remaining members.
            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onPlayerLeftLobby", [user_id])
            if owner_changed:
                for mid in members:
                    self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onLobbyOwnerChanged", [new_owner_id])

            return {"Return": "OK", "Exception": None}

        if method == "getInvitesToLobby":
            # Return BoltLobbyInviteWrapper[]: { LobbyId, Friend, Timestamp }
            invites_out: List[Dict[str, Any]] = []
            try:
                lobbies = list(self.db.db.lobbies.find({"is_active": True}))
            except Exception:
                lobbies = []
            for lob in lobbies:
                try:
                    lob_id = str(lob.get("_id"))
                except Exception:
                    continue
                invs = lob.get("invites") if isinstance(lob.get("invites"), list) else []
                for inv in invs:
                    invited_id = ""
                    sender_id = str(lob.get("owner_id") or "")
                    ts = now_ms()
                    if isinstance(inv, dict):
                        invited_id = str(inv.get("player_id") or "")
                        sender_id = str(inv.get("sender_id") or sender_id)
                        try:
                            ts = int(inv.get("timestamp") or ts)
                        except Exception:
                            ts = now_ms()
                    else:
                        invited_id = str(inv or "")
                    if invited_id != user_id:
                        continue
                    sender_user = self.db.get_user(sender_id) or {}
                    sender_wrapper = self._build_friend_wrapper(sender_user, self.db.get_friend_status(user_id, sender_id))
                    invites_out.append({"LobbyId": lob_id, "Friend": sender_wrapper, "Timestamp": ts})
            return {"Return": invites_out, "Exception": None}

        if method == "invitePlayerToLobby":
            invited_player_id = str(params[0]) if params else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            if not invited_player_id:
                return exc(EX_INCORRECT_PARAM, "IncorrectLobbyParam", "invitedPlayerId is required")
            if invited_player_id == user_id:
                return {"Return": "OK", "Exception": None}
            if not self.db.get_user(invited_player_id):
                return exc(404, "PlayerNotFound", "Player not found")

            lobby_id = str(lobby.get("_id") or "")
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            members = [str(m) for m in members if str(m)]
            if invited_player_id in members:
                return {"Return": "OK", "Exception": None}

            invites = lobby.get("invites") if isinstance(lobby.get("invites"), list) else []
            already = False
            for inv in invites:
                invited = str(inv.get("player_id") or "") if isinstance(inv, dict) else str(inv)
                if invited == invited_player_id:
                    already = True
                    break
            if not already:
                invites = list(invites)
                invites.append({"player_id": invited_player_id, "sender_id": user_id, "timestamp": now_ms()})
                self.db.update_lobby(lobby_id, {"invites": invites})

            invited_user = self.db.get_user(invited_player_id) or {}
            invited_wrapper = self._build_friend_wrapper(invited_user, self.db.get_friend_status(user_id, invited_player_id))
            # Notify lobby members.
            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onNewPlayerInvitedToLobby", [user_id, invited_wrapper])
            # Notify invited player.
            sender_user = self.db.get_user(user_id) or {}
            sender_wrapper = self._build_friend_wrapper(sender_user, self.db.get_friend_status(invited_player_id, user_id))
            self._queue_event_to_user(invited_player_id, "MatchmakingRemoteEventListener", "onReceivedInviteToLobby", [sender_wrapper, lobby_id])

            return {"Return": "OK", "Exception": None}

        if method == "revokePlayerInvitationToLobby":
            revoked_player_id = str(params[0]) if params else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can revoke invites")

            invites = lobby.get("invites") if isinstance(lobby.get("invites"), list) else []
            new_invites: List[Any] = []
            for inv in invites:
                invited = str(inv.get("player_id") or "") if isinstance(inv, dict) else str(inv)
                if invited != revoked_player_id:
                    new_invites.append(inv)
            self.db.update_lobby(lobby_id, {"invites": new_invites})

            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            members = [str(m) for m in members if str(m)]
            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onRevokeInviteToLobby", [user_id, revoked_player_id])
            self._queue_event_to_user(revoked_player_id, "MatchmakingRemoteEventListener", "onRevokeInviteToLobby", [user_id, revoked_player_id])
            return {"Return": "OK", "Exception": None}

        if method == "refuseInvitationToLobby":
            lobby_id = str(params[0]) if params else ""
            lobby = self.db.get_lobby(lobby_id)
            if not lobby:
                return exc(EX_LOBBY_NOT_FOUND, "LobbyNotFound", "Lobby not found")
            invites = lobby.get("invites") if isinstance(lobby.get("invites"), list) else []
            new_invites: List[Any] = []
            for inv in invites:
                invited = str(inv.get("player_id") or "") if isinstance(inv, dict) else str(inv)
                if invited != user_id:
                    new_invites.append(inv)
            self.db.update_lobby(lobby_id, {"invites": new_invites})

            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            members = [str(m) for m in members if str(m)]
            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onRefuseInviteToLobby", [user_id])
            return {"Return": "OK", "Exception": None}

        if method == "kickPlayerFromLobby":
            kicked_player_id = str(params[0]) if params else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can kick players")

            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            members = [str(m) for m in members if str(m)]
            if kicked_player_id in members:
                members.remove(kicked_player_id)
                self.db.update_lobby(lobby_id, {"members": members, "current_members": len(members)})
                self._set_user_lobby_id(kicked_player_id, "")

            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onPlayerKickedFromLobby", [user_id, kicked_player_id])
            self._queue_event_to_user(kicked_player_id, "MatchmakingRemoteEventListener", "onPlayerKickedFromLobby", [user_id, kicked_player_id])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyName":
            name = str(params[0]) if params else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can change lobby name")
            self.db.update_lobby(lobby_id, {"name": name})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyNameChanged", [name])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyType":
            lobby_type = int(params[0]) if params else 0
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can change lobby type")
            self.db.update_lobby(lobby_id, {"type": lobby_type})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            lobby_type_name = self._lobby_type_to_name(lobby_type)
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyTypeChanged", [lobby_type_name])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyOwner":
            new_owner_id = str(params[0]) if params else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can change lobby owner")
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            members = [str(m) for m in members if str(m)]
            if new_owner_id not in members:
                return exc(EX_NOT_LOBBY_MEMBER, "NotLobbyMember", "New owner must be lobby member")
            self.db.update_lobby(lobby_id, {"owner_id": new_owner_id})
            for mid in members:
                self._queue_event_to_user(mid, "MatchmakingRemoteEventListener", "onLobbyOwnerChanged", [new_owner_id])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyMaxMembers":
            max_members = int(params[0]) if params else 10
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can change max members")
            max_members = max(2, min(10, max_members))
            self.db.update_lobby(lobby_id, {"max_members": max_members})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyMaxMembersChanged", [max_members])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyJoinable":
            joinable = bool(params[0]) if params else True
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            owner_id = str(lobby.get("owner_id") or "")
            if owner_id != user_id:
                return exc(EX_NOT_LOBBY_OWNER, "NotLobbyOwner", "Only owner can change joinable state")
            self.db.update_lobby(lobby_id, {"joinable": joinable})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyJoinableChanged", [joinable])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyData":
            data = params[0] if params else {}
            if not isinstance(data, dict):
                return exc(EX_INCORRECT_PARAM, "IncorrectLobbyParam", "data must be a dictionary")
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            current = lobby.get("data") if isinstance(lobby.get("data"), dict) else {}
            current = dict(current)
            for k, v in data.items():
                if v is None:
                    continue
                current[str(k)] = str(v)
            self.db.update_lobby(lobby_id, {"data": current})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyDataChanged", [ {str(k): str(v) for k, v in data.items()} ])
            return {"Return": "OK", "Exception": None}

        if method == "deleteLobbyData":
            keys = params[0] if params else []
            if not isinstance(keys, list):
                keys = []
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            current = lobby.get("data") if isinstance(lobby.get("data"), dict) else {}
            current = dict(current)
            changed: Dict[str, str] = {}
            for k in keys:
                kk = str(k)
                if kk in current:
                    current.pop(kk, None)
                    changed[kk] = ""
            self.db.update_lobby(lobby_id, {"data": current})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyDataChanged", [changed])
            return {"Return": "OK", "Exception": None}

        if method == "sendLobbyChatMsg":
            msg = str(params[0]) if params else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            if lobby_id:
                # Treat chat as activity for stale-lobby cleanup.
                self.db.update_lobby(lobby_id, {})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyChatMessage", [user_id, msg])
            return {"Return": "OK", "Exception": None}

        if method == "setLobbyPhotonGame":
            region = str(params[0]) if params else ""
            room_id = str(params[1]) if len(params) > 1 else ""
            app_version = str(params[2]) if len(params) > 2 else ""
            lobby = self._get_current_lobby(user_id)
            if not lobby:
                return exc(EX_NOT_IN_LOBBY, "NotInLobby", "Not in lobby")
            lobby_id = str(lobby.get("_id") or "")
            photon_game = self._build_bolt_photon_game(region, room_id, app_version)
            self.db.update_lobby(lobby_id, {"photon_game": photon_game})
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            for mid in members:
                self._queue_event_to_user(str(mid), "MatchmakingRemoteEventListener", "onLobbyPhotonGameChanged", [photon_game])
            return {"Return": "OK", "Exception": None}

        if method == "getLobbyPhotonGame":
            lobby_id = str(params[0]) if params else ""
            lobby = self.db.get_lobby(lobby_id)
            if not lobby:
                return exc(EX_LOBBY_NOT_FOUND, "LobbyNotFound", "Lobby not found")
            pg = lobby.get("photon_game")
            return {"Return": pg or {"Region": "", "RoomId": "", "AppVersion": "", "CustomProperties": {}}, "Exception": None}

        if method == "setPhotonGame":
            # Signature: (region, roomId, appVersion)
            region = str(params[0]) if params else ""
            room_id = str(params[1]) if len(params) > 1 else ""
            app_version = str(params[2]) if len(params) > 2 else ""
            self.db.update_user(user_id, {
                "PlayerStatus": {
                    "OnlineStatus": "StateOnline",
                    "PlayInGame": None
                },
                "LastPhotonGame": self._build_bolt_photon_game(region, room_id, app_version),
            })
            self._notify_friends_player_status_changed(user_id)
            return {"Return": "OK", "Exception": None}

        if method == "requestLobbyList":
            # Minimal implementation: return active lobbies (proto Lobby[] compatible).
            lobbies = self.db.get_active_lobbies(50)
            result: List[Dict[str, Any]] = []
            for lob in lobbies or []:
                try:
                    lob_id = str(lob.get("_id") or "")
                    owner_id = str(lob.get("owner_id") or "")
                    name = str(lob.get("name") or "Lobby")
                    lobby_type = int(lob.get("type", 0) or 0)
                    max_members = int(lob.get("max_members", 10) or 10)
                    joinable = bool(lob.get("joinable", True))
                    result.append({
                        "Id": lob_id,
                        "OwnerPlayerId": owner_id,
                        "Name": name,
                        "LobbyType": lobby_type,
                        "Joinable": joinable,
                        "MaxMembers": max_members,
                        "Data": {},
                        "Members": [],
                        "Invites": [],
                        "GameServer": None,
                        "PhotonGame": None,
                    })
                except Exception:
                    continue
            return {"Return": result, "Exception": None}

        if method == "getLobbyOwner":
            lobby_id = str(params[0]) if params else ""
            lobby = self.db.get_lobby(lobby_id)
            if not lobby:
                return exc(EX_LOBBY_NOT_FOUND, "LobbyNotFound", "Lobby not found")
            owner_id = str(lobby.get("owner_id") or "")
            owner = self.db.get_user(owner_id) or {}
            return {
                "Return": {
                    "Id": str(owner.get("AuthId") or owner_id),
                    "Uid": str(owner.get("Uid") or ""),
                    "Name": str(owner.get("Name") or ""),
                    "AvatarId": str(owner.get("AvatarId") or ""),
                    "TimeInGame": int(owner.get("TimeInGame", 0) or 0),
                    "PlayerStatus": {
                        "PlayerId": str(owner.get("AuthId") or owner_id),
                        "PlayInGame": None,
                        "OnlineStatus": self._get_user_online_status(owner),
                    },
                    "LogoutDate": 0,
                    "RegistrationDate": int(owner.get("RegistrationDate", 0) or 0),
                },
                "Exception": None
            }

        if method == "getLobbyMembers":
            lobby_id = str(params[0]) if params else ""
            lobby = self.db.get_lobby(lobby_id)
            if not lobby:
                return exc(EX_LOBBY_NOT_FOUND, "LobbyNotFound", "Lobby not found")
            members = lobby.get("members") if isinstance(lobby.get("members"), list) else []
            out: List[Dict[str, Any]] = []
            for mid in members:
                u = self.db.get_user(str(mid))
                if not u:
                    continue
                out.append({
                    "Id": str(u.get("AuthId") or mid),
                    "Uid": str(u.get("Uid") or ""),
                    "Name": str(u.get("Name") or ""),
                    "AvatarId": str(u.get("AvatarId") or ""),
                    "TimeInGame": int(u.get("TimeInGame", 0) or 0),
                    "PlayerStatus": {
                        "PlayerId": str(u.get("AuthId") or mid),
                        "PlayInGame": None,
                        "OnlineStatus": self._get_user_online_status(u),
                    },
                    "LogoutDate": 0,
                    "RegistrationDate": int(u.get("RegistrationDate", 0) or 0),
                })
            return {"Return": out, "Exception": None}

        if method == "getGameServerDetails":
            # Not used in Photon flow; return a stub.
            game_server_id = str(params[0]) if params else ""
            return {"Return": {"Id": game_server_id, "SuccessfulResponse": False, "DoNotRefresh": True}, "Exception": None}

        if method == "getGameServerPlayers":
            return {"Return": [], "Exception": None}

        if method == "getLobbyGameServer":
            return {"Return": None, "Exception": None}

        if method == "setLobbyGameServer":
            return {"Return": "OK", "Exception": None}

        elif method == "requestInternetServerList":
            map_name = params[0] if params else ""
            free_slots = params[1] if len(params) > 1 else None
            max_players = params[2] if len(params) > 2 else None
            with_password = params[3] if len(params) > 3 else False
            
            # Читаем серверы из game_settings.json
            try:
                with open("game_settings.json", "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
                
                game_servers = settings_data.get("game_servers", [])
                
                # Фильтруем серверы по параметрам если нужно
                filtered_servers = []
                for server in game_servers:
                    # Фильтр по карте
                    if map_name and server.get("Map", "") != map_name:
                        continue
                    
                    # Фильтр по свободным слотам
                    if free_slots is not None:
                        current_players = server.get("Players", 0)
                        max_players_server = server.get("MaxPlayers", 10)
                        free_slots_server = max_players_server - current_players
                        if free_slots_server < free_slots:
                            continue
                    
                    # Фильтр по максимальным игрокам
                    if max_players is not None:
                        if server.get("MaxPlayers", 10) != max_players:
                            continue
                    
                    # Фильтр по паролю
                    if not with_password and server.get("HasPassword", False):
                        continue
                    
                    # Преобразуем в формат GameServer
                    filtered_servers.append({
                        "Id": server.get("Id", ""),
                        "Ip": server.get("Ip", ""),
                        "Port": server.get("Port", 7777)
                    })
                
                return {"Return": filtered_servers, "Exception": None}
                
            except Exception as e:
                logger.exception("Error loading game servers: %s", e)
                # Fallback серверы если файл не читается
                servers = [
                    {
                        "Id": "server_eu_001",
                        "Ip": "127.0.0.1",
                        "Port": 7777
                    },
                    {
                        "Id": "server_fr_001",
                        "Ip": "127.0.0.1",
                        "Port": 7778
                    }
                ]
                return {"Return": servers, "Exception": None}

        return {"Return": None, "Exception": None}
    
    # ===== GAME SETTINGS SERVICE =====
    
    def handle_game_settings_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """Обработка настроек игры"""
        if method == "getGameSettings":
            try:
                settings_data: Dict[str, Any] = {}

                # Optional file-based settings (kept for compatibility/dev).
                base_dir = os.path.dirname(os.path.abspath(__file__))
                candidates = [
                    os.path.join(base_dir, "game_settings.json"),
                    os.path.join(base_dir, "..", "game_settings.json"),
                    "game_settings.json",
                ]
                settings_path = next((p for p in candidates if os.path.exists(p)), None)
                if settings_path:
                    with open(settings_path, "r", encoding="utf-8") as f:
                        settings_data = json.load(f) or {}

                # DB-driven main settings (SettingsMain).
                main_settings = self.db.get_settings_main() or {}
                # Ensure expected fields exist for the client.
                main_settings.setdefault("HelpUrl", main_settings.get("help_url", "https://example.com/help"))
                # Maintenance flag (requested by user): both snake_case and PascalCase for safety.
                maintenance_mode = bool(main_settings.get("maintenance_mode") or main_settings.get("MaintenanceMode"))
                main_settings["maintenance_mode"] = maintenance_mode
                main_settings["MaintenanceMode"] = maintenance_mode
                # Disable packs flag used by currency controllers.
                if "DisablePacks" not in main_settings:
                    main_settings["DisablePacks"] = bool(main_settings.get("disable_packs", False))

                settings_data["main_settings"] = main_settings
                
                game_settings = []
                for key, value in settings_data.items():
                    setting = {
                        "Key": key,
                        "Value": json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value),
                        "Type": self._get_setting_type(value)
                    }
                    game_settings.append(setting)
                
                return {"Return": game_settings, "Exception": None}
            
            except Exception as e:
                return {
                    "Return": None,
                    "Exception": {
                        "Id": "SettingsLoadError",
                        "Code": 500,
                        "Message": f"Failed to load game settings: {str(e)}"
                    }
                }
        
        # Remote returns an array (GameSetting[]). Never return null.
        return {"Return": [], "Exception": None}
    
    def _get_setting_type(self, value):
        """Определяет тип настройки"""
        if isinstance(value, list):
            return "Array"
        elif isinstance(value, dict):
            return "Object"
        elif isinstance(value, int):
            return "Int"
        else:
            return "String"

    # ===== STORAGE SERVICE =====

    def handle_storage_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        """
        StorageRemoteService stubs.

        The C# client crashes on `null` for non-void RPCs (it does `response.Return.ToString()`),
        so for array-returning methods we always return an empty array instead of null.
        """
        if method == "readAllFiles":
            return {"Return": [], "Exception": None}

        if method == "readFile":
            # Remote expects byte[]. RpcService treats it as an array and parses JSON array into byte[].
            return {"Return": [], "Exception": None}

        if method in ("writeFile", "deleteFile"):
            return {"Return": "OK", "Exception": None}

        return {"Return": "OK", "Exception": None}
    
    # ===== ДОПОЛНИТЕЛЬНЫЕ СЕРВИСЫ =====
    
    def handle_bolt_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        return {"Return": "OK", "Exception": None}
    
    def handle_avatar_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        if method == "getAvatars":
            avatar_ids = params[0] if params else []
            # BoltAvatarService expects a JSON array of objects with fields: { Id, Avatar } where Avatar is base64.
            # Empty string is valid base64 for an empty payload and will be treated as "no avatar" on the client.
            avatars = [{"Id": aid, "Avatar": ""} for aid in avatar_ids]
            return {"Return": avatars, "Exception": None}
        return {"Return": None, "Exception": None}
    
    def handle_clan_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        user_id = self.get_current_user_id(client_id)
        
        if method == "createClan":
            name = params[0] if params else "New Clan"
            tag = params[1] if len(params) > 1 else "CLAN"
            
            clan_data = {
                "name": name,
                "tag": tag,
                "owner_id": user_id,
                "members": [user_id],
                "level": 1,
                "experience": 0
            }
            
            clan_id = self.db.create_clan(clan_data)
            if clan_id:
                clan_data["_id"] = clan_id
                return {"Return": clan_data, "Exception": None}
            return {"Return": None, "Exception": {"Id": "ClanCreateFailed", "Code": 500}}
        
        elif method == "getClan":
            clan_id = params[0] if params else ""
            clan = self.db.get_clan(clan_id)
            return {"Return": clan, "Exception": None} if clan else {"Return": None, "Exception": {"Id": "ClanNotFound", "Code": 404}}
        
        elif method == "searchClans":
            query = params[0] if params else ""
            clans = self.db.search_clans(query)
            return {"Return": json.dumps(clans, cls=DateTimeEncoder), "Exception": None}
        
        return {"Return": None, "Exception": None}
    
    def handle_chat_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        # ChatRemoteService methods used by BoltMessagesService.
        # Never return null for array/int methods, the client will crash on `response.Return.ToString()`.
        if method in ("getGroupMsgs", "getFriendMsgs"):
            return {"Return": [], "Exception": None}
        if method == "getChatUsers":
            return {"Return": [], "Exception": None}
        if method == "getUnreadChatUsersCount":
            return {"Return": 0, "Exception": None}
        if method in (
            "readFriendMsgs",
            "deleteFriendMsgs",
            "sendFriendMsg",
            "readGroupMsgs",
            "deleteGroupMsgs",
            "sendGroupMsg",
        ):
            return {"Return": "OK", "Exception": None}

        return {"Return": "OK", "Exception": None}
    
    def handle_ads_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        # AdsRemoteService is void-only in the client; return OK for consistency.
        return {"Return": "OK", "Exception": None}
    
    def handle_analytics_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        return {"Return": "OK", "Exception": None}
    
    def handle_marketplace_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        # MarketplaceRemoteService has many non-void methods; never return null.
        if method in (
            "getPlayerClosedRequests",
            "getTradeOpenPurchaseRequests",
            "getPlayerOpenRequests",
            "getPlayerProcessingRequest",
            "getTrades",
            "getTradeOpenSaleRequests",
        ):
            return {"Return": [], "Exception": None}

        if method == "getPlayerClosedRequestsCount":
            return {"Return": 0, "Exception": None}

        if method in ("createPurchaseRequestBySale", "createSaleRequest", "createPurchaseRequest"):
            return {"Return": "", "Exception": None}

        if method in ("getTrade", "getMarketplaceSettings"):
            return {"Return": {}, "Exception": None}

        if method == "cancelRequest":
            return {"Return": "OK", "Exception": None}

        return {"Return": "OK", "Exception": None}
    
    def handle_gameserver_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        return {"Return": None, "Exception": None}
    
    def handle_google_inapp_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        if method == "buyInApp":
            # Client expects PlayerInventory object.
            return {"Return": {}, "Exception": None}
        return {"Return": "OK", "Exception": None}
    
    def handle_appstore_inapp_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        if method == "buyInApp":
            return {"Return": {}, "Exception": None}
        return {"Return": "OK", "Exception": None}
    
    def handle_amazon_inapp_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        if method == "buyInApp":
            return {"Return": {}, "Exception": None}
        return {"Return": "OK", "Exception": None}
    
    def handle_admin_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        # Minimal admin endpoints for server control (maintenance/bans).
        # This is intentionally simple and can be extended with auth/roles later.
        if method == "setMaintenanceMode":
            enabled = bool(params[0]) if params else False
            settings = self.db.get_settings_main() or {}
            settings["maintenance_mode"] = enabled
            settings["MaintenanceMode"] = enabled
            self.db.upsert_settings_main(settings)
            return {"Return": "OK", "Exception": None}

        if method == "getMaintenanceMode":
            settings = self.db.get_settings_main() or {}
            enabled = bool(settings.get("maintenance_mode") or settings.get("MaintenanceMode"))
            return {"Return": enabled, "Exception": None}

        if method == "banUser":
            # Params: user_id, duration_seconds (0=perm), reason
            user_id = str(params[0]) if params else ""
            duration_seconds = int(params[1]) if len(params) > 1 else 0
            reason = str(params[2]) if len(params) > 2 else ""
            if not user_id:
                return {"Return": None, "Exception": {"Id": "InvalidArguments", "Code": 400, "Message": "user_id is required", "Params": {}}}
            self.db.ban_user(user_id, reason=reason, duration_seconds=duration_seconds, created_by=self.get_current_user_id(client_id))
            return {"Return": "OK", "Exception": None}

        if method == "unbanUser":
            user_id = str(params[0]) if params else ""
            if not user_id:
                return {"Return": None, "Exception": {"Id": "InvalidArguments", "Code": 400, "Message": "user_id is required", "Params": {}}}
            self.db.unban_user(user_id)
            return {"Return": "OK", "Exception": None}

        if method == "getBan":
            user_id = str(params[0]) if params else ""
            ban = self.db.get_active_ban(user_id) if user_id else None
            return {"Return": ban or {}, "Exception": None}

        return {"Return": "OK", "Exception": None}
    
    def handle_promocode_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        user_id = self.get_current_user_id(client_id)
        if method == "activatePromo":
            promo = str(params[0]) if params else ""
            result = self.activate_promocode(user_id, promo)
            return {"Return": result, "Exception": None}
        return {"Return": "OK", "Exception": None}
    
    def handle_rank_service(self, method: str, params: List, client_id: int = None) -> Dict[str, Any]:
        user_id = self.get_current_user_id(client_id)

        if method == "rankAssignment":
            is_win = bool(params[0]) if params else False

            other_stats = self._normalize_flat_str_dict(self.db.get_other_stats(user_id))
            defaults = self._get_default_other_stats()

            if not other_stats:
                other_stats = defaults
                self.db.create_other_stats(user_id, dict(other_stats))
            else:
                self._merge_defaults(other_stats, defaults)

            try:
                rank_old = int(other_stats.get("ranked_rank", "0"))
                mmr_old = int(other_stats.get("ranked_current_mmr", "1000"))
                played_old = int(other_stats.get("ranked_played_matches", "0"))
                won_old = int(other_stats.get("ranked_won_matches", "0"))
                calibration_old = int(other_stats.get("ranked_calibration_match_count", "0"))
            except Exception:
                rank_old = 0
                mmr_old = 1000
                played_old = 0
                won_old = 0
                calibration_old = 0

            delta = 25 if is_win else -25
            mmr_new = max(0, mmr_old + delta)

            played_new = played_old + 1
            won_new = won_old + (1 if is_win else 0)

            calibration_new = calibration_old
            if calibration_new < 10:
                calibration_new += 1
            calibration_left = max(0, 10 - calibration_new)

            now_parts = self._split_long_to_int_parts(self._dotnet_utc_seconds())

            other_stats["ranked_current_mmr"] = str(mmr_new)
            other_stats["ranked_target_mmr"] = str(mmr_new)
            other_stats["ranked_played_matches"] = str(played_new)
            other_stats["ranked_won_matches"] = str(won_new)
            other_stats["ranked_calibration_match_count"] = str(calibration_new)
            other_stats["ranked_calibration_status"] = "1" if calibration_new >= 10 else "0"
            other_stats["ranked_last_activity_time1"] = str(now_parts[0])
            other_stats["ranked_last_activity_time2"] = str(now_parts[1])
            other_stats["ranked_last_match_status"] = "1"

            self.db.update_other_stats(user_id, dict(other_stats))

            return {
                "Return": {
                    "RankNew": rank_old,
                    "RankOld": rank_old,
                    "Mmr": mmr_new,
                    "CalibrationMatchesLeft": calibration_left,
                    "IsSuccessful": True,
                },
                "Exception": None,
            }

        return {"Return": None, "Exception": None}
    
    def disconnect_user(self, client_id: int):
        """Обработка отключения пользователя"""
        if self.clients_manager:
            user_id = self.clients_manager.get_user_id(client_id)
            if user_id:
                # Ensure the user is removed from any active lobby on disconnect.
                try:
                    self._leave_lobby_server_side(user_id)
                except Exception:
                    pass
                self.db.update_user(user_id, {
                    "PlayerStatus": {
                        "OnlineStatus": "StateOffline",
                        "PlayInGame": None
                    }
                })
                # Notify friends that this user went offline.
                self._notify_friends_player_status_changed(user_id)
