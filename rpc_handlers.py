# database.py - MongoDB база данных для V2 Standoff Server
import json
import logging
import os
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
from bson import ObjectId

logger = logging.getLogger("V2Server")

class Database:
    """MongoDB база данных для игрового сервера"""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "v2_standoff"):
        self.db_name = db_name
        
        try:
            # Подключаемся к MongoDB
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Проверяем соединение
            self.db = self.client[db_name]
            logger.info("Connected to MongoDB: %s", db_name)
            
            # Создаем индексы
            self._create_indexes()
            
        except Exception as e:
            logger.error("MongoDB connection failed: %s", e)
            raise Exception("MongoDB is required! Please start MongoDB server.")
    
    def _create_indexes(self):
        """Создание индексов для оптимизации"""
        try:
            # Индексы для пользователей
            self.db.users.create_index("AuthId", unique=True)
            self.db.users.create_index("Uid")
            
            # Индексы для сессий
            # Some old records may contain `ticket: null`, which breaks unique index creation.
            # Use a partial unique index so only real tickets participate.
            try:
                self.db.sessions.delete_many({"ticket": None})
                self.db.sessions.delete_many({"ticket": {"$exists": False}})
            except Exception as e:
                logger.warning("Session cleanup failed: %s", e)

            self.db.sessions.create_index("ticket", unique=True, sparse=True)
            self.db.sessions.create_index("created_at", expireAfterSeconds=86400)  # 24 часа
            
            # Индексы для друзей
            self.db.friends.create_index([("user_id", 1), ("friend_id", 1)], unique=True)

            # Lobby indexes (activity cleanup / membership queries)
            self.db.lobbies.create_index("is_active")
            self.db.lobbies.create_index("updated_at")
            self.db.lobbies.create_index("members")
            
            # Индексы для кланов
            self.db.clans.create_index("tag", unique=True)
            self.db.clans.create_index("name")

            # Индексы для банов
            self.db.bans.create_index("user_id", unique=True)
            self.db.bans.create_index("expires_at")

            # Индексы для промокодов
            self.db.promocodes.create_index("code", unique=True)
            self.db.promocode_redemptions.create_index([("code", 1), ("user_id", 1)], unique=True)
            
            logger.info("Database indexes created")
        except Exception as e:
            logger.warning("Index creation failed: %s", e)
    
    # ===== USERS =====
    
    def create_user(self, auth_id: str, user_data: Dict[str, Any]) -> bool:
        """Создать нового пользователя"""
        try:
            user_data["AuthId"] = auth_id
            user_data["created_at"] = datetime.now()
            user_data["updated_at"] = datetime.now()
            self.db.users.insert_one(user_data)
            return True
        except pymongo.errors.DuplicateKeyError:
            return False
    
    def get_user(self, auth_id: str) -> Optional[Dict[str, Any]]:
        """Получить пользователя по AuthId"""
        user = self.db.users.find_one({"AuthId": auth_id})
        if user:
            user.pop("_id", None)
        return user
    
    def get_user_by_uid(self, uid: str) -> Optional[Dict[str, Any]]:
        """Получить пользователя по UID"""
        user = self.db.users.find_one({"Uid": uid})
        if user:
            user.pop("_id", None)
        return user
    
    def update_user(self, auth_id: str, update_data: Dict[str, Any]) -> bool:
        """Обновить данные пользователя"""
        update_data["updated_at"] = datetime.now()
        result = self.db.users.update_one(
            {"AuthId": auth_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def search_users(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Поиск пользователей по имени или UID"""
        users = self.db.users.find({
            "$or": [
                {"Name": {"$regex": query, "$options": "i"}},
                {"Uid": {"$regex": query}}
            ]
        }).limit(limit)
        
        result = []
        for user in users:
            user.pop("_id", None)
            result.append(user)
        return result

    def count_users(self, query: str) -> int:
        """Подсчитать количество пользователей для FriendsRemoteService.getPlayersCount."""
        try:
            q = str(query or "")
            return int(
                self.db.users.count_documents(
                    {
                        "$or": [
                            {"Name": {"$regex": q, "$options": "i"}},
                            {"Uid": {"$regex": q}},
                        ]
                    }
                )
            )
        except Exception:
            return 0
    
    # ===== SESSIONS =====
    
    def create_session(self, ticket: str, user_id: str) -> bool:
        """Создать сессию"""
        try:
            self.db.sessions.insert_one({
                "ticket": ticket,
                "user_id": user_id,
                "created_at": datetime.now()
            })
            return True
        except:
            return False
    
    def get_session(self, ticket: str) -> Optional[str]:
        """Получить user_id по ticket"""
        session = self.db.sessions.find_one({"ticket": ticket})
        return session["user_id"] if session else None
    
    def delete_session(self, ticket: str) -> bool:
        """Удалить сессию"""
        result = self.db.sessions.delete_one({"ticket": ticket})
        return result.deleted_count > 0
    
    # ===== PLAYER STATS =====
    
    def create_player_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Создать статистику игрока"""
        try:
            stats["user_id"] = user_id
            stats["created_at"] = datetime.now()
            stats["updated_at"] = datetime.now()
            self.db.player_stats.insert_one(stats)
            return True
        except:
            return False
    
    def get_player_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получить статистику игрока"""
        stats = self.db.player_stats.find_one({"user_id": user_id})
        if stats:
            stats.pop("_id", None)
            stats.pop("user_id", None)
            stats.pop("created_at", None)
            stats.pop("updated_at", None)
        return stats
    
    def update_player_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Обновить статистику игрока"""
        stats["updated_at"] = datetime.now()
        result = self.db.player_stats.update_one(
            {"user_id": user_id},
            {"$set": stats},
            upsert=True
        )
        return True
    
    # ===== OTHER STATS (RANKED) =====
    
    def create_other_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Создать дополнительную статистику"""
        try:
            stats["user_id"] = user_id
            stats["created_at"] = datetime.now()
            stats["updated_at"] = datetime.now()
            self.db.other_stats.insert_one(stats)
            return True
        except:
            return False
    
    def get_other_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получить дополнительную статистику"""
        stats = self.db.other_stats.find_one({"user_id": user_id})
        if stats:
            stats.pop("_id", None)
            stats.pop("user_id", None)
            stats.pop("created_at", None)
            stats.pop("updated_at", None)
        return stats
    
    def update_other_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Обновить дополнительную статистику"""
        stats["updated_at"] = datetime.now()
        result = self.db.other_stats.update_one(
            {"user_id": user_id},
            {"$set": stats},
            upsert=True
        )
        return True
    
    # ===== INVENTORY =====
    
    def create_player_inventory(self, user_id: str, inventory: Dict[str, Any]) -> bool:
        """Создать инвентарь игрока"""
        try:
            inventory["user_id"] = user_id
            inventory["created_at"] = datetime.now()
            inventory["updated_at"] = datetime.now()
            self.db.player_inventory.insert_one(inventory)
            return True
        except:
            return False
    
    def get_player_inventory(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получить инвентарь игрока"""
        inventory = self.db.player_inventory.find_one({"user_id": user_id})
        if inventory:
            inventory.pop("_id", None)
            inventory.pop("user_id", None)
        return inventory
    
    def update_player_inventory(self, user_id: str, inventory: Dict[str, Any]) -> bool:
        """Обновить инвентарь игрока"""
        inventory["updated_at"] = datetime.now()
        result = self.db.player_inventory.update_one(
            {"user_id": user_id},
            {"$set": inventory},
            upsert=True
        )
        return True
    
    # ===== FRIENDS =====
    
    def add_friend(self, user_id: str, friend_id: str, status: int = 4) -> bool:
        """Добавить друга"""
        try:
            self.db.friends.insert_one({
                "user_id": user_id,
                "friend_id": friend_id,
                "status": status,
                "created_at": datetime.now()
            })
            return True
        except:
            return False
    
    def get_player_friends(self, user_id: str, statuses: List[int] = None) -> List[str]:
        """Получить список друзей"""
        query = {"user_id": user_id}
        if statuses:
            query["status"] = {"$in": statuses}
        
        friends = self.db.friends.find(query)
        return [f["friend_id"] for f in friends]

    def get_player_friend_records(self, user_id: str, statuses: List[int] = None) -> List[Dict[str, Any]]:
        """Получить записи друзей (friend_id + status + даты)"""
        query: Dict[str, Any] = {"user_id": user_id}
        if statuses:
            query["status"] = {"$in": statuses}
        friends = self.db.friends.find(query)
        result: List[Dict[str, Any]] = []
        for f in friends:
            f.pop("_id", None)
            result.append(f)
        return result

    def get_friend_status(self, user_id: str, friend_id: str) -> int:
        """Получить статус отношений (если нет -> 0)."""
        try:
            doc = self.db.friends.find_one({"user_id": user_id, "friend_id": friend_id})
            if not doc:
                return 0
            return int(doc.get("status", 0) or 0)
        except Exception:
            return 0
    
    def update_friend_status(self, user_id: str, friend_id: str, status: int) -> bool:
        """Обновить статус дружбы"""
        result = self.db.friends.update_one(
            {"user_id": user_id, "friend_id": friend_id},
            {"$set": {"status": status}},
            upsert=True
        )
        return True
    
    def remove_friend(self, user_id: str, friend_id: str) -> bool:
        """Удалить друга"""
        result = self.db.friends.delete_one({
            "user_id": user_id,
            "friend_id": friend_id
        })
        return result.deleted_count > 0
    
    # ===== CLANS =====
    
    def create_clan(self, clan_data: Dict[str, Any]) -> Optional[str]:
        """Создать клан"""
        try:
            clan_data["created_at"] = datetime.now()
            clan_data["updated_at"] = datetime.now()
            result = self.db.clans.insert_one(clan_data)
            return str(result.inserted_id)
        except:
            return None
    
    def get_clan(self, clan_id: str) -> Optional[Dict[str, Any]]:
        """Получить клан по ID"""
        try:
            clan = self.db.clans.find_one({"_id": ObjectId(clan_id)})
            if clan:
                clan["_id"] = str(clan["_id"])
            return clan
        except:
            return None
    
    def get_clan_by_tag(self, tag: str) -> Optional[Dict[str, Any]]:
        """Получить клан по тегу"""
        clan = self.db.clans.find_one({"tag": tag})
        if clan:
            clan["_id"] = str(clan["_id"])
        return clan
    
    def update_clan(self, clan_id: str, update_data: Dict[str, Any]) -> bool:
        """Обновить клан"""
        try:
            update_data["updated_at"] = datetime.now()
            result = self.db.clans.update_one(
                {"_id": ObjectId(clan_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def search_clans(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Поиск кланов"""
        clans = self.db.clans.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"tag": {"$regex": query, "$options": "i"}}
            ]
        }).limit(limit)
        
        result = []
        for clan in clans:
            clan["_id"] = str(clan["_id"])
            result.append(clan)
        return result
    
    # ===== LOBBIES =====
    
    def create_lobby(self, lobby_data: Dict[str, Any]) -> Optional[str]:
        """Создать лобби"""
        try:
            lobby_data["created_at"] = datetime.now()
            lobby_data["updated_at"] = datetime.now()
            result = self.db.lobbies.insert_one(lobby_data)
            return str(result.inserted_id)
        except:
            return None
    
    def get_lobby(self, lobby_id: str) -> Optional[Dict[str, Any]]:
        """Получить лобби"""
        try:
            lobby = self.db.lobbies.find_one({"_id": ObjectId(lobby_id)})
            if lobby:
                lobby["_id"] = str(lobby["_id"])
            return lobby
        except:
            return None
    
    def update_lobby(self, lobby_id: str, update_data: Dict[str, Any]) -> bool:
        """Обновить лобби"""
        try:
            update_data["updated_at"] = datetime.now()
            result = self.db.lobbies.update_one(
                {"_id": ObjectId(lobby_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_lobby(self, lobby_id: str) -> bool:
        """Удалить лобби"""
        try:
            result = self.db.lobbies.delete_one({"_id": ObjectId(lobby_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def get_active_lobbies(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получить активные лобби"""
        lobbies = self.db.lobbies.find({"is_active": True}).limit(limit)
        result = []
        for lobby in lobbies:
            lobby["_id"] = str(lobby["_id"])
            result.append(lobby)
        return result
    
    # ===== ITEM DEFINITIONS =====
    
    def init_item_definitions(self, items: List[Dict[str, Any]]) -> bool:
        """Инициализировать определения предметов"""
        try:
            # Удаляем старые определения
            self.db.item_definitions.delete_many({})
            
            # Вставляем новые
            if items:
                self.db.item_definitions.insert_many(items)
            
            logger.info("Initialized %s item definitions", len(items))
            return True
        except Exception as e:
            logger.exception("Failed to init item definitions: %s", e)
            return False
    
    def get_item_definitions(self) -> Dict[int, Dict[str, Any]]:
        """Получить все определения предметов"""
        items = self.db.item_definitions.find({})
        result = {}
        for item in items:
            item.pop("_id", None)
            item_id = item.get("Id")
            if item_id:
                result[item_id] = item
        return result
    
    def get_item_definition(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Получить определение предмета по ID"""
        item = self.db.item_definitions.find_one({"Id": item_id})
        if item:
            item.pop("_id", None)
        return item

    # ===== SETTINGS =====

    def get_settings_main(self) -> Dict[str, Any]:
        """
        Получить настройки из коллекции SettingsMain.

        Ожидается один документ с флагами вроде `maintenance_mode`.
        """
        try:
            # Prefer a well-known singleton id if present.
            doc = self.db["SettingsMain"].find_one({"_id": "main"}) or self.db["SettingsMain"].find_one({})
            if not doc:
                return {}
            doc.pop("_id", None)
            return doc
        except Exception:
            return {}

    def upsert_settings_main(self, settings: Dict[str, Any]) -> bool:
        """Обновить/создать singleton документ SettingsMain."""
        try:
            data = dict(settings or {})
            data["updated_at"] = datetime.now()
            self.db["SettingsMain"].update_one(
                {"_id": "main"},
                {"$set": data, "$setOnInsert": {"created_at": datetime.now()}},
                upsert=True,
            )
            return True
        except Exception:
            return False

    # ===== BANS =====

    def get_active_ban(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получить активный бан пользователя (если есть)."""
        try:
            ban = self.db.bans.find_one({"user_id": user_id, "active": True})
            if not ban:
                return None
            ban.pop("_id", None)

            expires_at = ban.get("expires_at")
            if isinstance(expires_at, datetime) and expires_at <= datetime.now():
                # Auto-expire
                self.db.bans.update_one({"user_id": user_id}, {"$set": {"active": False, "updated_at": datetime.now()}})
                ban["active"] = False
                return None
            return ban
        except Exception:
            return None

    def ban_user(self, user_id: str, reason: str = "", duration_seconds: int = 0, created_by: str = "") -> bool:
        """Забанить пользователя. duration_seconds=0 -> перманент."""
        try:
            expires_at = None
            if duration_seconds and int(duration_seconds) > 0:
                expires_at = datetime.now() + timedelta(seconds=int(duration_seconds))
            doc = {
                "user_id": user_id,
                "reason": reason or "",
                "active": True,
                "expires_at": expires_at,
                "created_by": created_by or "",
                "updated_at": datetime.now(),
            }
            self.db.bans.update_one(
                {"user_id": user_id},
                {"$set": doc, "$setOnInsert": {"created_at": datetime.now()}},
                upsert=True,
            )
            return True
        except Exception:
            return False

    def unban_user(self, user_id: str) -> bool:
        """Снять бан пользователя."""
        try:
            self.db.bans.update_one(
                {"user_id": user_id},
                {"$set": {"active": False, "updated_at": datetime.now()}},
                upsert=True,
            )
            return True
        except Exception:
            return False

    # ===== PROMOCODES =====

    def get_promocode(self, code: str) -> Optional[Dict[str, Any]]:
        try:
            doc = self.db.promocodes.find_one({"code": str(code).upper()})
            if not doc:
                return None
            doc.pop("_id", None)
            return doc
        except Exception:
            return None

    def record_promocode_redemption(self, code: str, user_id: str) -> bool:
        try:
            self.db.promocode_redemptions.insert_one(
                {"code": str(code).upper(), "user_id": str(user_id), "redeemed_at": datetime.now()}
            )
            return True
        except Exception:
            return False

    def has_promocode_redemption(self, code: str, user_id: str) -> bool:
        try:
            return self.db.promocode_redemptions.find_one({"code": str(code).upper(), "user_id": str(user_id)}) is not None
        except Exception:
            return False

    def increment_promocode_use(self, code: str) -> None:
        try:
            self.db.promocodes.update_one(
                {"code": str(code).upper()},
                {"$inc": {"uses": 1}, "$set": {"updated_at": datetime.now()}},
                upsert=False,
            )
        except Exception:
            pass
