# BACKEND

## Структура backend
```
📁 mcp-file-server/
├── 📁 backend/
│   ├── 📁 mcp_server/
│   │   ├── 📝 __init__.py
│   │   ├── 📝 server.py
│   │   └── 📝 file_tools.py
│   ├── 📝 Dockerfile
│   ├── 📝 requirements.txt
│   └── main.py
├── 📁 frontend/
│   ├── 📁 public/
│   ├── 📁 src/
│   │   ├── 📝 App.jsx
│   │   ├── 📝 App.css
│   │   └── 📝 index.jsx
│   ├── 📝 package.json
│   └── 📝 Dockerfile.react
├── 📁 shared-data/
│   └── 📝 test.md
├── 📝 docker-compose.yml
└── ...
```

## Настройка окружения и запуск
Создание виртуального окружения Python
```bash
python3 -m venv .venv
```

## Активация виртуального окружения
```bash
. .venv/bin/activate
# Команда для выхода из окружения
deactivate
```

## Установка зависимостей проекта
```bash
pip3 install -r requirements.txt
```