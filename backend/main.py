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
        files = os.listdir("/shared-data")
        if not files:
            return {"answer": "В папке shared-data нет файлов для анализа"}
        
        content = read_file_content(files[0])
        if not content:
            return {"answer": "Не удалось прочитать файл"}
        
        # Очень простой и прямой промпт
        prompt = f"""
        Содержимое файла:
        {content}

        Вопрос: {request.question}

        Ответь на вопрос используя только информацию из файла.
        """
        
        payload = {
            "model": "qwen2:0.5b-instruct",  # Используем более мощную модель
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9
            }
        }
        
        response = requests.post("http://ollama:11434/api/generate", json=payload, timeout=120)
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