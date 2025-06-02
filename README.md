# Coding Agent

Coding Agent is a multi-agent system for automated code development. It consists of three specialized agents:

1. **Programmer Agent**: Generates code based on user requirements
2. **Tester Agent**: Creates unit tests and integration tests for the generated code
3. **Validator Agent**: Validates code quality, checks for security issues, and fixes errors

## Features

- REST API interface using FastAPI
- Integration with OpenAI GPT-4.1
- Support for MCP (Model Context Protocol)
- Structured output with JSON Schema validation
- Support for long context (up to 1M tokens)
- File system operations, Git integration, and code execution
- Web interface using React
- CLI interface for automation
- WebSocket for real-time updates
- Session and history management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/redeyes420dev/agent-test.git
   cd agent-test
   ```

2. Install dependencies:
   ```bash
   ./install.sh
   ```

## Running the Application

### Without Docker

1. Start the application:
   ```bash
   ./run.sh
   ```

2. Access the web interface at [http://localhost:3002](http://localhost:3002)

### With Docker

1. Build the Docker images:
   ```bash
   ./build.sh
   ```

2. Start the application:
   ```bash
   ./run_docker.sh
   ```

3. Access the web interface at [http://localhost:8000](http://localhost:8000)

## Usage

### Generate Code

To generate code based on requirements, send a POST request to `/generate_code` with a JSON body containing the requirements:

```json
{
  "requirements": "Create a simple web application with user authentication and a dashboard"
}
```

The response will contain the generated code, documentation, and tests.

### Validate Code

To validate code quality, send a POST request to `/validate_code` with a JSON body containing the code:

```json
{
  "code": "your_code_here"
}
```

The response will contain the analysis results, security check, and standards validation.

### Refactor Code

To refactor code, send a POST request to `/refactor_code` with a JSON body containing the code:

```json
{
  "code": "your_code_here"
}
```

The response will contain the refactored code.

### Optimize Code

To optimize code, send a POST request to `/optimize_code` with a JSON body containing the code:

```json
{
  "code": "your_code_here"
}
```

The response will contain the optimized code.

## Running with Docker

1. Build the Docker images:
   ```bash
   ./build.sh
   ```

2. Run the Docker containers:
   ```bash
   ./run_docker.sh
   ```

This will start both the backend and frontend containers. The application will be available at [http://localhost:8000](http://localhost:8000).

## Running Tests

To run all tests, execute:
```bash
./test.sh
```

This will run both Python and React tests.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Project Structure

```
coding_agent/
├── agents/
│   ├── programmer_agent.py
│   ├── tester_agent.py
│   └── validator_agent.py
├── core/
│   ├── llm_client.py
│   ├── prompt_manager.py
│   └── state_manager.py
├── tools/
│   ├── file_operations.py
│   ├── code_executor.py
│   └── git_integration.py
├── api/
│   ├── routes.py
│   └── websocket.py
├── ui/
│   └── react_app/
├── config/
│   └── settings.py
└── tests/
```

## License

This project is licensed under the MIT License.