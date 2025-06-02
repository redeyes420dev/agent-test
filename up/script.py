# Создаем структуру проекта
import os

project_structure = {
    "coding_agent": {
        "agents": [
            "programmer_agent.py",
            "tester_agent.py", 
            "validator_agent.py",
            "__init__.py"
        ],
        "core": [
            "llm_client.py",
            "mcp_integration.py",
            "prompt_manager.py",
            "state_manager.py",
            "__init__.py"
        ],
        "tools": [
            "file_operations.py",
            "code_executor.py", 
            "git_integration.py",
            "mcp_tool_manager.py",
            "__init__.py"
        ],
        "api": [
            "routes.py",
            "websocket.py",
            "keys.py",
            "__init__.py"
        ],
        "mcp": [
            "key_validation.py",
            "servers_config.py",
            "__init__.py"
        ],
        "security": [
            "encryption.py",
            "auth.py",
            "__init__.py"
        ],
        "monitoring": [
            "usage_tracker.py",
            "metrics.py",
            "__init__.py"
        ],
        "config": [
            "settings.py",
            "__init__.py"
        ]
    },
    "frontend": {
        "src": {
            "components": [
                "ApiKeyManager.jsx",
                "RepoConnect.jsx",
                "CodeEditor.jsx",
                "UsageDashboard.jsx",
                "AgentWorkflow.jsx"
            ],
            "hooks": [
                "useWebSocket.js",
                "useApiKeys.js"
            ],
            "utils": [
                "security.js",
                "api.js"
            ],
            "views": [
                "MainView.jsx",
                "SettingsView.jsx"
            ]
        },
        "public": ["index.html"],
        "": ["package.json", "webpack.config.js"]
    },
    "docker": [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.mcp.yml"
    ],
    "": [
        "requirements.txt",
        "main.py",
        ".env.example",
        "README.md"
    ]
}

def create_structure(base_path, structure, level=0):
    """Создает структуру файлов и папок"""
    for key, value in structure.items():
        if isinstance(value, dict):
            # Создаем директорию
            dir_path = os.path.join(base_path, key) if key else base_path
            os.makedirs(dir_path, exist_ok=True)
            print("  " * level + f"📁 {key}/")
            create_structure(dir_path, value, level + 1)
        elif isinstance(value, list):
            # Создаем файлы
            dir_path = os.path.join(base_path, key) if key else base_path
            os.makedirs(dir_path, exist_ok=True)
            if key:
                print("  " * level + f"📁 {key}/")
            for file_name in value:
                file_path = os.path.join(dir_path, file_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {file_name}\n# Файл создан автоматически\n")
                print("  " * (level + 1) + f"📄 {file_name}")

print("🚀 Создание структуры проекта агента разработки...")
create_structure(".", project_structure)
print("\n✅ Структура проекта создана!")