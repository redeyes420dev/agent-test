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
   ```
   git clone https://github.com/redeyes420dev/agent-test.git
   cd agent-test
   ```

2. Install dependencies:
   ```
   ./install.sh
   ```

3. Run the application:
   ```
   ./run.sh
   ```

4. Access the web interface at http://localhost:3000

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
   ```
   ./build.sh
   ```

2. Run the Docker containers:
   ```
   ./run_docker.sh
   ```

This will start both the backend and frontend containers. The backend will be available at http://localhost:8000 and the frontend at http://localhost:3000.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.