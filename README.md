# svc-whitelist
Микросервис управления белым списком игроков Minecraft-сети серверов.

Сервис хранит whitelist игроков и предоставляет REST API для:
* добавления игрока в whitelist
* проверки доступа
* удаления игрока из whitelist

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
IP сервиса из docker-compose: `http://[fd98:2dd6:8f48:1d99:8164:b5f6::2]`

IP базы данных: `[fd98:2dd6:8f48:1d99:8164:b5f6::3]:5432`

Swagger документация: `http://[fd98:2dd6:8f48:1d99:8164:b5f6::2]/docs`

---

[документация](https://github.com/FreedomDevs/svcLibs/blob/master/docs/svc-whitelist.md)
