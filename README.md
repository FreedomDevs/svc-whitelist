

# svc-whitelist

Микросервис управления белым списком игроков Minecraft-сети серверов.

Сервис хранит whitelist игроков и предоставляет REST API для:

* добавления игрока в whitelist
* проверки доступа
* удаления игрока из whitelist

Данные сохраняются в PostgreSQL и доступны через HTTP API.

---

# Запуск

Сервис запускается через **docker compose**.

```bash
docker compose up --build
```

После запуска будут подняты:

* **svc-whitelist-app-dev** — приложение
* **svc-whitelist-postgres** — база данных

---

# Сетевые адреса

IP сервиса из docker-compose:

```
http://[fd98:2dd6:8f48:1d99:8164:b5f6::2]
```

IP базы данных:

```
[fd98:2dd6:8f48:1d99:8164:b5f6::3]:5432
```

Swagger документация:

```
http://[fd98:2dd6:8f48:1d99:8164:b5f6::2]/docs
```

---

# Пример запроса

## Добавление игрока в whitelist

POST `/whitelist`

```json
{
  "servername": "test_server",
  "userid": "1",
  "username": "Alex"
}
```

### Ответ

HTTP `201 Created`

```json
"POST /whitelist HTTP/1.1" 201 Created
```

---

## Ошибка: игрок уже существует

HTTP `409 Conflict`

```json
{
  "error": {
    "message": "User already in whitelist",
    "code": "WHITELIST_ALREADY_EXISTS"
  },
  "meta": {
    "traceId": "8d4c5c8c4e624154bd7f5105f6254bc7",
    "timestamp": "2026-02-26T17:05:51.909123Z"
  }
}
```

---

# Проверка whitelist

GET `/whitelist/check`

Пример запроса:

```
/whitelist/check?servername=test_server&userid=1
```

### Ответ (если игрок в whitelist)

```json
{
  "data": {
    "allowed": true
  },
  "message": "Whitelist check successful",
  "meta": {
    "code": "WHITELIST_CHECK_OK",
    "traceId": "8d4c5c8c4e624154bd7f5105f6254bc7",
    "timestamp": "2026-02-26T17:05:51.909123Z"
  }
}
```

---

# Удаление игрока

DELETE `/whitelist`

```json
{
  "servername": "test_server",
  "userid": "1"
}
```

### Ответ

```json
{
  "message": "User removed from whitelist",
  "meta": {
    "code": "WHITELIST_REMOVED_OK",
    "traceId": "8d4c5c8c4e624154bd7f5105f6254bc7",
    "timestamp": "2026-02-26T17:05:51.909123Z"
  }
}
```

---

# Эндпоинты

| Метод  | Endpoint         | Описание                     |
| ------ | ---------------- | ---------------------------- |
| POST   | /whitelist       | Добавить игрока в whitelist  |
| GET    | /whitelist/check | Проверить whitelist          |
| DELETE | /whitelist       | Удалить игрока из whitelist  |
| GET    | /health          | Проверка здоровья сервиса    |
| GET    | /live            | Проверка доступности сервиса |

---

# HTTP коды статусов

| Код                      | HTTP | Описание              |
| ------------------------ | ---- | --------------------- |
| WHITELIST_CREATED_OK     | 201  | Игрок добавлен        |
| WHITELIST_CHECK_OK       | 200  | Проверка whitelist    |
| WHITELIST_REMOVED_OK     | 200  | Игрок удалён          |
| WHITELIST_ALREADY_EXISTS | 409  | Игрок уже в whitelist |
| WHITELIST_NOT_FOUND      | 404  | Игрок не найден       |
| HEALTH_OK                | 200  | Сервис работает       |
| LIVE_OK                  | 200  | Сервис доступен       |

---

