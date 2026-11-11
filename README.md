# Mini-Redis

Легковесная Key-Value БД на Python.

## Возможности
- TCP-сервер (порт 6380)
- Команды: `PING`, `SET`, `GET`, `DEL`, `EXPIRE`
- TTL (time-to-live)
- AOF (append-only log) — сохранение на диск
- Восстановление состояния при перезапуске
- Поддержка UTF-8 (русские значения)

## Запуск

```bash
python server.py
#в другом теминале
python client.py