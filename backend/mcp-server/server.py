import os
from typing import List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, TextContentType
import asyncio
from .file_tools import FileTools

# Инициализация сервера
server = Server("file-server")

# Инициализация инструментов
file_tools = FileTools()

@server.list_tools()
async def list_tools() -> List[Tool]:
    return file_tools.get_tools()

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    return await file_tools.call_tool(name, arguments)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())