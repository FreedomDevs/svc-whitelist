# svc-whitelist
## Клонирование репозитория

```bash
git clone https://github.com/FreedomDevs/svc-whitelist
cd svc-whitelist
```
## Установка зависимостей
```
pip install -r requirements.txt
```
## Запуск
```
uvicorn app.main:app --reload
```
Документация будет доступна по адресу:
http://127.0.0.1:8000/docs

# Проверка
```

{
  "servername": "test_server", <br>
  "userid": "1", <br>
  "username": "Alex" <br>
}

```
Ответ:
```"POST /v1/whitelist HTTP/1.1" 201 Created```

Если уже был добавлен:
```
{
  "error": { <br>
    "message": "User already in whitelist", <br>
    "code": "WHITELIST_ALREADY_EXISTS" <br>
  }, <br>
  "meta": { <br>
    "traceId": "8d4c5c8c4e624154bd7f5105f6254bc7", <br>
    "timestamp": "2026-02-26T17:05:51.909123Z" <br>
  }
}
```

# Эндпоинты
```
post | /v1/whitelist | add player <br>
get | /v1/whitrlist/check | check white list <br>
delete | /v1/whitelist | del player <br>
get | /health | health check <br>
get | /live | liveness <br>
```

## HTTP Коды статусов
```
WHITELIST_CREATED_OK |	201 |	Игрок добавлен <br>
WHITELIST_CHECK_OK |	200 |	Проверка whitelist <br>
WHITELIST_REMOVED_OK |	200 |	Игрок удалён <br>
WHITELIST_ALREADY_EXISTS |	409 |	Игрок уже в whitelist <br>
WHITELIST_NOT_FOUND |	404 |	Игрок не найден <br>

```
HEALTH_OK |	200 |	Сервис здоров
LIVE_OK |	200 |	Сервис жив


