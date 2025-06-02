
from openai import AsyncOpenAI

class LLMClient:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4.1-mini-2025-04-14"

    async def generate_code(self, prompt: str, **kwargs):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=32768,
            **kwargs
        )
        return response
