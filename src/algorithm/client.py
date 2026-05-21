"""MiMo API client with mock mode support."""

import os
import json
import httpx
from typing import AsyncIterator


class MiMoClient:
    def __init__(self):
        self.api_key = os.getenv("MIMO_API_KEY", "")
        self.base_url = os.getenv("MIMO_BASE_URL", "https://api.xiaomimimo.com/v1")
        self.model = os.getenv("MIMO_MODEL", "mimo-v2.5-pro")
        self.mock_mode = not self.api_key
        self.total_tokens = 0
        self.request_count = 0

    async def chat(self, messages: list[dict], **kwargs) -> dict:
        if self.mock_mode:
            return self._mock_response(messages)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": messages, **kwargs},
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            self.total_tokens += data.get("usage", {}).get("total_tokens", 0)
            self.request_count += 1
            return data

    async def chat_stream(self, messages: list[dict], **kwargs) -> AsyncIterator[str]:
        if self.mock_mode:
            mock = self._mock_response(messages)
            yield mock["choices"][0]["message"]["content"]
            return
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": messages, "stream": True, **kwargs},
                timeout=120,
            ) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        chunk = json.loads(line[6:])
                        delta = chunk["choices"][0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]

    async def structured_output(self, messages: list[dict], schema: dict) -> dict:
        if self.mock_mode:
            return self._mock_structured(messages)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "response_format": {"type": "json_object"},
                },
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            self.total_tokens += data.get("usage", {}).get("total_tokens", 0)
            self.request_count += 1
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)

    def get_usage_stats(self) -> dict:
        return {
            "total_tokens": self.total_tokens,
            "request_count": self.request_count,
            "mock_mode": self.mock_mode,
        }

    def _mock_response(self, messages: list[dict]) -> dict:
        return {
            "choices": [{"message": {"role": "assistant", "content": "Mock response. Set MIMO_API_KEY for real API."}}],
            "usage": {"total_tokens": 0},
        }

    def _mock_structured(self, messages: list[dict]) -> dict:
        return {
            "approach": "Hash Map",
            "language": "python",
            "code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
            "complexity_time": "O(n)",
            "complexity_space": "O(n)",
            "explanation": "We use a hash map to store seen numbers. For each number, check if its complement exists.",
            "test_cases": [
                {"input": "[2,7,11,15], 9", "expected": "[0,1]", "description": "Basic case"},
                {"input": "[3,3], 6", "expected": "[0,1]", "description": "Duplicate numbers"},
            ],
        }
