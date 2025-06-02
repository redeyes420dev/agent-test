# Agents Overview

| Agent | Ядро (LLM + Tools) | Ответственность | Основные MCP-серверы |
|-------|-------------------|-----------------|----------------------|
| **Programmer** | gpt-4.1-mini + fs, git, docs | Генерация и рефакторинг кода | sandbox, docs, git |
| **Tester** | gpt-4.1-mini + pytest-runner | Unit / integration tests, покрытие | sandbox, testing |
| **Validator** | gpt-4.1-mini + pylint, mypy, bandit | Статический анализ, безопасность | quality, security |

## Жизненный цикл pull-request

```mermaid
graph TD
    A[User task] --> B(Programmer)
    B --> C(Tester)
    C -- все тесты пройдены --> D(Validator)
    D -- OK --> E(Merge & Deploy)
    D -- ошибки --> B
````

## Директории

| Путь                | Содержимое                                                   |
| ------------------- | ------------------------------------------------------------ |
| **backend/**        | FastAPI + LangGraph workflow, REST + WebSocket API           |
| **agents/**         | Код трёх специализированных агентов                          |
| **frontend/**       | React + MUI SPA (панель управления, генератор кода, Git-GUI) |
| **plugins/**        | Механизм расширений (entry-points `coding_agent.plugins`)    |
| **infrastructure/** | Dockerfile, docker-compose, GitHub Actions, Vault шаблоны    |
| **docs/**           | Markdown, C4, OpenAPI spec, diagrams-as-code                 |

## Ключевые технологии

* **LLM** — *gpt-4.1-mini-2025-04-14* (контекст 1 M токенов).
* **LangGraph** — надёжная оркестрация многоагентных workflow.
* **Model Context Protocol (MCP)** — унифицированный доступ к sandbox / lint / git / docs инструментам.
* **FastAPI** — API + WebSocket стриминг.
* **React + MUI** — SPA-интерфейс (API-keys менеджер уже реализован ).
* **GitPython** — клон/ветки/пуш из агента.
* **Docker** — чистые окружения для выполнения сгенерированного кода.

## Безопасность

* Изолированное выполнение в `CodeSandbox` (Docker, `network_mode: none`).
* Проверка OWASP Top-10 на backend-слое (FastAPI middlewares).
* Шифрование API-ключей (`cryptography.Fernet`) и хранение только в БД (см. реализацию контекста `ApiKeyContext` ).
* Circuit-breaker для MCP-серверов, health-checks `/health`.

## Быстрый старт

```bash
# 1. Клонировать репо
git clone https://github.com/your-org/coding-agent.git
cd coding-agent

# 2. Настроить переменные
cp .env.example .env        # OPENAI_API_KEY, ENCRYPTION_KEY, ...

# 3. Запустить всё
docker-compose up -d

# 4. UI
open http://localhost:3002  # Dashboard, API-keys, Git-manager
```

## Разработка

```bash
# Запуск unit-тестов
pytest -q

# Линт + типы
pylint backend agents && mypy backend agents

# Генерация схемы OpenAPI
uvicorn backend.main:app --reload
```

## CI/CD

* GitHub Actions `ci.yml` — lint → tests → build images → push to GHCR → deploy via SSH.
* Blue/Green — две группы сервисов в compose, переключатель трафика через Traefik.
* Обсервабилити — Prometheus + Grafana (дашборд `infrastructure/grafana/agents.json`).

## Расширение агентного стека

1. Создать класс агента, реализующий `BaseAgent` и объявить инструменты MCP.
2. Зарегистрировать entry-point в `pyproject.toml`.
3. Добавить узел в `workflow.py` и описать переходы.
4. Создать E2E-тесты в `tests/agents/`.
