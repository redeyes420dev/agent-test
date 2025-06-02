# GPT-4.1 Integration for Coding Agent

This document describes the integration of GPT-4.1 agentic workflows into the Coding Agent project.

## Overview

The integration adds the following capabilities:

1. Agentic workflows for solving coding issues
2. Tool-based interactions with the codebase
3. Patch application for code changes
4. Enhanced prompting techniques for better LLM interactions

## Components

### 1. LLM Client

The `LLMClient` class in `coding_agent/core/llm_client.py` has been updated to support tool-based interactions with the `generate_with_tools` method.

### 2. System Prompts

Two new system prompts have been added:

- `agentic_workflow.json`: A detailed prompt for agentic coding workflows
- `customer_service.json`: A sample customer service prompt

### 3. Tools

A new tool has been added for executing Python code, bash commands, and applying patches:

- `python_bash_patch_tool.py`: Defines the tool description and parameters
- `apply_patch.py`: A standalone script for applying patches to the codebase

### 4. Agents

All agents (ProgrammerAgent, TesterAgent, ValidatorAgent) have been updated to:

- Initialize with the Python/Bash/Patch tool
- Add methods for solving issues using the agentic workflow

### 5. API Endpoints

New API endpoints have been added:

- `/solve_issue`: Solve an issue using the agentic workflow
- `/apply_patch`: Apply a patch to the codebase

## Usage

### Solving Issues

To solve a coding issue, use the `/solve_issue` endpoint with a description of the issue. The agent will:

1. Use the agentic workflow prompt to guide its actions
2. Use tools to investigate and fix the issue
3. Apply patches as needed

### Applying Patches

To apply a patch, use the `/apply_patch` endpoint with a patch in the V4A diff format. The patch will be applied using the `apply_patch.py` script.

## Example Patch Format

```plaintext
*** Begin Patch
*** Update File: path/to/file.py
@@ class SomeClass
@@     def some_method():
-    old_code_here
+    new_code_here
*** End Patch
```

## Running the Application

To run the application with the new capabilities:

1. Set the OPENAI_API_KEY environment variable
2. Run the main application: `python coding_agent/main.py`

## Testing

To test the new functionality:

1. Use the `/solve_issue` endpoint with various issue descriptions
2. Use the `/apply_patch` endpoint with different patch formats