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

mcp-file-server/
├── backend/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── file_tools.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── shared-data/
│   └── test.md
├── docker-compose.yml
└── README.md