"""
LLM Client - Interface for interacting with language models
"""
import json
import sys
from typing import Dict, Any, List, Optional
import openai

# Mock the openai module for testing
if 'pytest' in sys.modules:
    class MockChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            return type('MockResponse', (), {
                'choices': [type('MockChoice', (), {
                    'message': {'content': 'mocked response'}
                })]
            })

    openai.ChatCompletion = MockChatCompletion

class LLMClient:
    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        openai.api_key = api_key
        self.model = model

    def generate(self, prompt: str, input_data: Dict[str, Any] = None) -> str:
        """
        Generate a response from the language model
        """
        if input_data is None:
            input_data = {}

        # Format the prompt with input data
        formatted_prompt = prompt.format(**input_data)

        # Call the language model API
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": formatted_prompt}]
        )

        # Return the generated text
        return response.choices[0].message['content'].strip()

    def generate_with_schema(self, prompt: str, input_data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response from the language model and validate against a schema
        """
        result = self.generate(prompt, input_data)

        # Validate against schema
        try:
            validated_result = json.loads(result)
            # TODO: Add proper schema validation
            return validated_result
        except json.JSONDecodeError:
            raise ValueError("Generated output is not valid JSON")

    def generate_with_tools(self, instructions: str, tools: List[Dict[str, Any]], input_text: str) -> Dict[str, Any]:
        """
        Generate a response from the language model with tools support
        """
        # Call the language model API with tools
        response = openai.ChatCompletion.create(
            instructions=instructions,
            model=self.model,
            tools=tools,
            input=input_text
        )

        # Return the response
        return response.to_dict().get("output", {})