# V2 Standoff Server

Полноценный WebSocket сервер для игры Standoff 2 (V2).

## Структура проекта

```
old_server/
├── server.py              # Главный WebSocket сервер
├── rpc_handlers.py        # Обработчики всех RPC сервисов
├── database.py            # Работа с базой данных (JSON)
├── real_items_collection.py  # Коллекция предметов игры
├── requirements.txt       # Зависимости Python
├── render.yaml           # Конфигурация для Render
├── Procfile              # Процессы для деплоя
├── runtime.txt           # Версия Python
├── .env.example          # Пример переменных окружения
├── start_server.bat       # Запуск сервера (Windows)
└── README.md             # Документация
```

## Деплой на Render

### Автоматический деплой
1. Создайте аккаунт на [Render.com](https://render.com)
2. Подключите ваш GitHub репозиторий
3. Создайте новый Web Service
4. Укажите папку `old_server` как Root Directory
5. Render автоматически обнаружит `render.yaml` и развернет сервер

### Ручная настройка
1. Build Command: `pip install -r requirements.txt`
2. Start Command: `python server.py`
3. Environment: `Python 3`

### Переменные окружения
- `PORT` - Порт сервера (автоматически устанавливается Render)
- `HTTP_PORT` - Порт HTTP сервера (PORT + 1)

## Локальная установка

1. Установите Python 3.9+
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск сервера

### Windows
```bash
start_server.bat
```

### Linux/Mac
```bash
python server.py
```

### С переменными окружения
```bash
PORT=8080 python server.py
```

Сервер запустится на `ws://0.0.0.0:PORT`

## Реализованные сервисы

### Аутентификация
- `V2AuthRemoteService` - Авторизация по логину/паролю
- `GoogleAuthRemoteService` - Google авторизация
- `FacebookAuthRemoteService` - Facebook авторизация
- `GameCenterAuthRemoteService` - GameCenter авторизация

### Основные сервисы
- `HandshakeRemoteService` - Handshake и logout
- `PlayerRemoteService` - Управление профилем игрока
- `PlayerStatsRemoteService` - Статистика игрока
- `OtherStatsRemoteService` - Дополнительная статистика (ранкед)
- `InventoryRemoteService` - Инвентарь и предметы
- `FriendsRemoteService` - Друзья и поиск игроков
- `MatchmakingRemoteService` - Матчмейкинг и лобби
- `GameSettingsRemoteService` - Настройки игры

### Дополнительные сервисы
- `AvatarRemoteService` - Аватары
- `ClanRemoteService` - Кланы
- `ChatRemoteService` - Чат
- `AdsRemoteService` - Реклама
- `AnalyticsRemoteService` - Аналитика
- `MarketplaceRemoteService` - Маркетплейс
- `GameServerRemoteService` - Игровые серверы

### In-App Purchase
- `GoogleInAppRemoteService` - Google покупки
- `AppStoreInAppRemoteService` - App Store покупки
- `AmazonInAppRemoteService` - Amazon покупки

### Ultramax сервисы
- `AdminRemoteService` - Админ функции
- `PromocodeRemoteService` - Промокоды
- `RankRemoteService` - Ранги

## База данных

Сервер использует JSON файлы для хранения данных:
- `db_users.json` - Пользователи
- `db_sessions.json` - Сессии
- `db_player_stats.json` - Статистика игроков
- `db_other_stats.json` - Дополнительная статистика
- `db_player_inventory.json` - Инвентарь игроков
- `db_friends.json` - Друзья

## Настройка клиента Unity

В Unity измените настройки подключения:
1. Откройте `BoltApi.cs`
2. Установите IP сервера: `127.0.0.1` (для локального) или IP вашего сервера
3. Порт: `25505`

## Логирование

Сервер выводит подробные логи всех RPC запросов:
- Подключения/отключения клиентов
- RPC запросы (сервис, метод, параметры)
- Результаты выполнения
- Ошибки

### Telegram (опционально)

Если заданы переменные окружения, сервер будет дублировать логи в Telegram бота (не блокируя основной поток):

Обязательные:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Опциональные:
- `TELEGRAM_LOG_LEVEL` (по умолчанию: `ERROR`)
- `TELEGRAM_LOG_TIMEOUT_S` (по умолчанию: `5`)
- `TELEGRAM_LOG_MAX_QUEUE` (по умолчанию: `200`)
- `TELEGRAM_LOG_MIN_INTERVAL_S` (по умолчанию: `1.0`)
- `TELEGRAM_LOG_PREFIX` (по умолчанию: `[V2Server]`)

## Особенности

- Автоматическое создание пользователей при первом входе
- Генерация случайных UID (8-9 цифр)
- Поддержка WebSocket ping/pong
- Обработка отключений клиентов
- Thread-safe операции с базой данных
- Полная коллекция предметов (227 items)

## Разработка

Для добавления нового RPC метода:
1. Добавьте метод в соответствующий handler в `rpc_handlers.py`
2. Метод должен возвращать `{"Return": result, "Exception": None}`
3. При ошибке возвращайте `{"Return": None, "Exception": {...}}`

## Лицензия

Проект создан для образовательных целей.
