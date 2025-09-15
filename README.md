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

### Технологический стек
- **Python**: 3.10.12
- **Docker**: 28.3.3, build 980b856
- **Ubuntu**: 24.04