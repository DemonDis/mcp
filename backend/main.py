from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import json

app = FastAPI(title="MCP File Server API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

def read_file_content(filename: str):
    try:
        filepath = f"/shared-data/{filename}"
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    try:
        # Получаем список файлов
        files = os.listdir("/shared-data")
        if not files:
            return {"answer": "В папке shared-data нет файлов для анализа"}
        
        # Читаем все файлы
        files_content = []
        for filename in files:
            content = read_file_content(filename)
            if content:
                files_content.append(f"ФАЙЛ: {filename}\nСОДЕРЖИМОЕ:\n{content}\n")
        
        if not files_content:
            return {"answer": "Не удалось прочитать файлы"}
        
        # Формируем контекст для модели
        context = "\n".join(files_content)
        
        # Улучшенный промпт с четким разделением ролей
        prompt = f"""
        РОЛЬ: Ты - ассистент, который анализирует содержимое файлов и отвечает на вопросы пользователя.

        КОНТЕКСТ:
        Пользователь задал вопрос о файлах в папке shared-data.

        ВОПРОС ПОЛЬЗОВАТЕЛЯ: "{request.question}"

        СОДЕРЖИМОЕ ФАЙЛОВ:
        {context}

        ИНСТРУКЦИЯ:
        1. Анализируй ВОПРОС пользователя и отвечай на него на основе СОДЕРЖИМОГО ФАЙЛОВ
        2. Не проси пользователя предоставить текст - весь необходимый текст уже в файлах
        3. Отвечай конкретно на вопрос пользователя
        4. Используй только информацию из предоставленных файлов
        5. Если информации недостаточно - скажи об этом честно
        6. Ответ дай на русском языке

        ПРИМЕР:
        Вопрос: "Что содержится в файле test.md?"
        Ответ: "Файл test.md содержит: 1. Заголовок 'Анализ текста', 2. Пример текста 'Привет, мир!...', 3. Инструкцию для анализа тональности"

        ТВОЙ ОТВЕТ на вопрос "{request.question}":
        """
        
        payload = {
            "model": "qwen2:0.5b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        response = requests.post("http://ollama:11434/api/generate", json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        answer = result.get("response", "Не удалось получить ответ").strip()
        
        return {
            "answer": answer,
            "files_used": files,
            "files_count": len(files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки вопроса: {str(e)}")
    
@app.get("/api/files")
async def list_files():
    try:
        files = os.listdir("/shared-data")
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файлов: {str(e)}")

@app.get("/api/files/{filename}")
async def read_file(filename: str):
    try:
        content = read_file_content(filename)
        if content is None:
            raise HTTPException(status_code=404, detail="Файл не найден")
        return {"filename": filename, "content": content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения файла: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)