# svc-whitelist
Микросервис управления белым списком игроков.  
Предоставляет операции для добавления игроков в whitelist серверов, проверки доступа и удаления записей.

IP локальной базы данных из docker-compose: [fd98:2dd6:8f48:1d99:8164:b5f6:6317:0002]:5432

## Клонирование репозитория

```bash
git clone https://github.com/FreedomDevs/svc-whitelist
cd svc-whitelist
```
## Установка зависимостей
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Запуск
```
uvicorn app.main:app --reload
```
Документация будет доступна по адресу:
http://localhost:9008/docs

# Проверка
```

{
  "servername": "test_server", 
  "userid": "1", 
  "username": "Alex" 
}

```
Ответ:
```"POST /v1/whitelist HTTP/1.1" 201 Created```

Если уже был добавлен:
```
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

# Эндпоинты
```
post | /v1/whitelist | Добавить игрока 
get | /v1/whitrlist/check | Проверка whitelist 
delete | /v1/whitelist | Удалить игрока 
get | /health | Сервер здоров
get | /live | Сервер жив
```

## HTTP Коды статусов
```
WHITELIST_CREATED_OK |	201 |	Игрок добавлен 
WHITELIST_CHECK_OK |	200 |	Проверка whitelist 
WHITELIST_REMOVED_OK |	200 |	Игрок удалён 
WHITELIST_ALREADY_EXISTS |	409 |	Игрок уже в whitelist 
WHITELIST_NOT_FOUND |	404 |	Игрок не найден 
HEALTH_OK |	200 |	Сервис здоров
LIVE_OK |	200 |	Сервис жив
```

