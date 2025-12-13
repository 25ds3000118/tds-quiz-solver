import re
import time
from browser import Browser
from files import fetch_file
from llm import LLM
from executor import Executor
import httpx

class QuizSolver:
    def __init__(self):
        self.browser = Browser()
        self.llm = LLM()
        self.exec = Executor()

    async def solve(self, url: str):
        start = time.time()

        while True:
            text, html = await self.browser.load(url)

            submit = self._find_submit(text)
            files = self._find_files(html)

            context = text
            data = {}

            for f in files:
                parsed = await fetch_file(f)
                if parsed:
                    data[f] = parsed

            prompt = self._build_prompt(context, data)
            answer = await self.llm.ask(prompt)

            result = await self._submit(submit, url, answer)

            if result.get("correct"):
                return result

            if time.time() - start > 160:
                return result

    def _find_submit(self, text):
        for u in re.findall(r'https?://\S+', text):
            if "submit" in u:
                return u
        return None

    def _find_files(self, html):
        return re.findall(r'href="([^"]+\.(csv|json|pdf))"', html)

    def _build_prompt(self, question, files):
        p = f"Answer the question correctly.\n\n{question}\n"
        for k, v in files.items():
            p += f"\nFile {k}: {v}\n"
        p += "\nReturn ONLY the final answer."
        return p

    async def _submit(self, submit_url, quiz_url, answer):
        async with httpx.AsyncClient() as c:
            r = await c.post(submit_url, json={
                "email": settings.EMAIL,
                "secret": settings.SECRET,
                "url": quiz_url,
                "answer": answer
            })
            return r.json()
