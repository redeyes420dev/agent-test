"""
Интеграция Model Context Protocol (MCP) для агента разработки
"""

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters
from typing import List, Dict, Any, Optional
from contextlib import AsyncExitStack
import asyncio
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_integration")


class McpToolset:
    """Обертка для инструментов MCP"""
    
    def __init__(self, client, server_name: str):
        self.client = client
        self.server_name = server_name
        self.tools = {}
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Получение списка доступных инструментов"""
        if not self.client:
            return []
        
        try:
            response = await self.client.list_tools()
            return response
        except Exception as e:
            logger.error(f"Failed to list tools from {self.server_name}: {e}")
            return []
            
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Вызов инструмента по имени"""
        if not self.client:
            raise ValueError(f"MCP client for {self.server_name} is not initialized")
            
        try:
            response = await self.client.call_tool(tool_name, params)
            return response
        except Exception as e:
            logger.error(f"Failed to call tool {tool_name} from {self.server_name}: {e}")
            raise


class CodeAgentMcpClient:
    """Клиент MCP для агента разработки кода"""
    
    def __init__(self, config: Dict[str, Any]):
        self.servers_config = config.get('mcp_servers', [])
        self.active_connections = {}
        self.tool_cache = {}
        self.exit_stack = AsyncExitStack()
        
    async def initialize_servers(self):
        """Асинхронная инициализация MCP-серверов"""
        for server_config in self.servers_config:
            try:
                await self.connect_server(server_config)
            except Exception as e:
                logger.error(f"Failed to initialize MCP server {server_config['name']}: {e}")
                
    async def connect_server(self, server_config: Dict[str, Any]) -> Optional[McpToolset]:
        """Подключение к MCP-серверу с обработкой ошибок"""
        server_name = server_config.get('name', 'unknown')
        
        try:
            # Создаем параметры для подключения
            connection_params = StdioServerParameters(
                command=server_config.get('command', ''),
                args=server_config.get('args', []),
                env=server_config.get('env', {}),
                cwd=server_config.get('cwd', '')
            )
            
            # Подключаемся к серверу
            client = await McpClient.connect(connection_params)
            
            # Оборачиваем клиент в наш toolset
            toolset = McpToolset(client, server_name)
            
            # Получаем список инструментов
            tools = await toolset.list_tools()
            
            # Кэшируем список инструментов
            for tool in tools:
                self.tool_cache[tool['name']] = {
                    'server': server_name,
                    'schema': tool
                }
                
            # Добавляем соединение в активные
            self.active_connections[server_name] = toolset
            
            logger.info(f"Connected to MCP server {server_name} with {len(tools)} tools")
            return toolset
            
        except Exception as e:
            logger.error(f"Error connecting to MCP server {server_name}: {e}")
            return None
            
    async def call_tool(self, server_name: str, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Вызов инструмента MCP"""
        if server_name not in self.active_connections:
            raise ValueError(f"MCP server {server_name} is not connected")
            
        return await self.active_connections[server_name].call_tool(tool_name, params)
        
    async def call_tool_by_name(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Вызов инструмента по имени (автоматический поиск сервера)"""
        if tool_name not in self.tool_cache:
            raise ValueError(f"Tool {tool_name} not found in any MCP server")
            
        server_name = self.tool_cache[tool_name]['server']
        return await self.call_tool(server_name, tool_name, params)
        
    async def cleanup(self):
        """Закрытие всех соединений при завершении работы"""
        for server_name, toolset in self.active_connections.items():
            try:
                if hasattr(toolset.client, 'close') and callable(toolset.client.close):
                    await toolset.client.close()
                logger.info(f"Closed connection to {server_name}")
            except Exception as e:
                logger.error(f"Error closing connection to {server_name}: {e}")
                
        # Очищаем кэш и соединения
        self.tool_cache = {}
        self.active_connections = {}
        
    async def get_available_tools(self) -> Dict[str, List[Dict[str, Any]]]:
        """Получение всех доступных инструментов по серверам"""
        result = {}
        
        for server_name, toolset in self.active_connections.items():
            tools = await toolset.list_tools()
            result[server_name] = tools
            
        return result
        
    async def ping_all_servers(self) -> Dict[str, bool]:
        """Проверка доступности всех серверов"""
        result = {}
        
        for server_name, toolset in self.active_connections.items():
            try:
                await toolset.list_tools()
                result[server_name] = True
            except Exception:
                result[server_name] = False
                
        return result