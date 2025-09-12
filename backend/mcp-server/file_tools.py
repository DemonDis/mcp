import os
import aiofiles
from typing import List, Optional
from mcp.types import TextContent, TextContentType
import requests
import json

class FileTools:
    def __init__(self):
        self.base_path = "/shared-data"
        self.ollama_url = "http://ollama:11434/api/generate"
    
    def get_tools(self):
        return [
            {
                "name": "read_file",
                "description": "Чтение содержимого файла из shared-data папки",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Имя файла для чтения"
                        }
                    },
                    "required": ["filename"]
                }
            },
            {
                "name": "list_files",
                "description": "Список всех файлов в shared-data папке",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "analyze_with_context",
                "description": "Анализ вопроса с учетом содержимого файлов",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Вопрос пользователя"
                        },
                        "files_content": {
                            "type": "string",
                            "description": "Содержимое relevant файлов"
                        }
                    },
                    "required": ["question", "files_content"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: dict):
        if name == "read_file":
            return await self.read_file(arguments["filename"])
        elif name == "list_files":
            return await self.list_files()
        elif name == "analyze_with_context":
            return await self.analyze_with_context(arguments["question"], arguments["files_content"])
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def read_file(self, filename: str):
        filepath = os.path.join(self.base_path, filename)
        try:
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            return [TextContent(
                type=TextContentType.TEXT,
                text=content
            )]
        except Exception as e:
            return [TextContent(
                type=TextContentType.TEXT,
                text=f"Ошибка при чтении файла: {str(e)}"
            )]
    
    async def list_files(self):
        try:
            files = os.listdir(self.base_path)
            return files
        except Exception as e:
            return []
    
    async def analyze_with_context(self, question: str, files_content: str):
        try:
            prompt = f"""
            ВОПРОС ПОЛЬЗОВАТЕЛЯ: {question}

            СОДЕРЖИМОЕ ФАЙЛОВ ДЛЯ АНАЛИЗА:
            {files_content}

            ИНСТРУКЦИЯ:
            1. Внимательно проанализируй содержимое файлов
            2. Ответь ТОЛЬКО на основе предоставленного содержимого файлов
            3. Не придумывай информацию, которой нет в файлах
            4. Если в файлах нет информации для ответа - так и скажи
            5. Ответ дай на русском языке
            6. Будь точным и конкретным

            ОТВЕТ:
            """
            
            payload = {
                "model": "qwen2:0.5b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Низкая температура для большей точности
                    "top_p": 0.9
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "Не удалось получить ответ")
            
        except Exception as e:
            return f"Ошибка при анализе: {str(e)}"