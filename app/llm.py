import httpx
import re
from settings import settings

class LLM:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=120)

    async def ask(self, prompt: str):
        payload = {
            "model": settings.MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        r = await self.client.post(
            f"{settings.LLM_BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"},
            json=payload
        )

        text = r.json()["choices"][0]["message"]["content"]
        return self._parse(text)

    def _parse(self, text: str):
        try:
            return int(text)
        except:
            try:
                return float(text)
            except:
                return text.strip()

    async def close(self):
        await self.client.aclose()
