import asyncio
from playwright.async_api import async_playwright

class Browser:
    async def load(self, url: str) -> tuple[str, str]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            text = await page.evaluate("() => document.body.innerText")
            html = await page.content()

            await browser.close()
            return text, html
