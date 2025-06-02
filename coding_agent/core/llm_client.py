"""
LLM Client - Interface for interacting with language models
"""
import json
from typing import Dict, Any
import openai

class LLMClient:
    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        openai.api_key = api_key
        self.model = model

    def generate(self, prompt: str, input_data: Dict[str, Any]) -> str:
        """
        Generate a response from the language model
        """
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