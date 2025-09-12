# MCP (Model Context Protocol)

- Ollama - `http://localhost:11434`
- Filesystem MCP Server - `http://localhost:28000`

## Структура проекта
```
📁 mcp/
├──📁  
|   └── 
├── 📝 
└── 📝 
```

## Запуск модели
### Скачивание образа Ollama
```bash
docker pull ollama/ollama
```


### Запуск Ollama в Docker
```bash
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama-data:/root/.ollama \
  ollama/ollama
```

### Запуск языковой модели через Ollama
Загружает и запускает модель **qwen2:0.5b** (или codeqwen:1.5b или Qwen2-0.5B-Instruct или llama2:7b)
```bash
docker exec ollama ollama pull qwen2:0.5b-instruct
```

## Запуск MCP-сервера (Filesystem)
1. Создайте директорию, к которой вы хотите дать доступ серверу (например, ~/mcp-test-dir).
2. Запустите filesystem-сервер в Docker

### Собираем образ
```bash
docker build -t mcp-fileserver-local .
```

### Запускаем наш локальный образ
```bash
docker run -d \
  --name mcp-fileserver \
  -p 28000:28000 \
  -v /home/sdd/mcp-test-dir:/root/mcp-test-dir \
  -e MCP_FILESYSTEM_DIRS='["/root/mcp-test-dir"]' \
  mcp-fileserver-local \
  -- sse --port 28000
```

**-p 28000:28000**: Пробрасываем порт для SSE-соединения.
**-v ...**: Пробрасываем вашу тестовую папку внутрь контейнера.
**-e MCP_FILESYSTEM_DIRS=...**: Говорим серверу, с какой папкой внутри контейнера он может работать.

```bash
docker run -it --rm \
  --network host \
  -v /home/sdd/mcp-test-dir:/root/mcp-test-dir \
  -v /home/sdd/mcp-config.json:/root/mcp-config.json \
  node:20-bookworm-slim \
  npx -y @modelcontextprotocol/cli@latest --config /root/mcp-config.json
```

docker run -d \
  --name mcp-fileserver \
  -p 28000:28000 \
  -v /home/sdd/mcp-test-dir:/root/mcp-test-dir \
  -e MCP_FILESYSTEM_DIRS='["/root/mcp-test-dir"]' \
  mcp-fileserver-local \
  bash -c "npx -y @modelcontextprotocol/server-filesystem /root/mcp-test-dir sse --port 28000"

[Ваша хост-машина (Linux)]
       |
       | (HTTP/SSE)
       |
+---------------+
| Контейнер 1:  |   [MCP-сервер]  (например, filesystem или simple)
| - MCP Server  |   предоставляет инструменты для работы с файлами
+---------------+
       |
       | (HTTP/SSE)
       |
+---------------+
| Контейнер 2:  |   [MCP-клиент]  (Ollama + модель + клиентское приложение)
| - Ollama      |   запрашивает инструменты у MCP-сервера
| - Модель      |
+---------------+



### Технологический стек
- **Python**: 3.10.12
- **Docker**: 28.3.3, build 980b856
- **Ubuntu**: 24.04