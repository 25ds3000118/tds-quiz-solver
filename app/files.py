import httpx
import pandas as pd
import json
from io import BytesIO
import PyPDF2

async def fetch_file(url: str) -> dict | None:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        if r.status_code != 200:
            return None

        if url.endswith(".csv"):
            df = pd.read_csv(BytesIO(r.content))
            return {
                "type": "csv",
                "columns": df.columns.tolist(),
                "rows": df.head(10).to_dict("records"),
                "full": df.to_dict("records")
            }

        if url.endswith(".json"):
            return {
                "type": "json",
                "data": json.loads(r.content)
            }

        if url.endswith(".pdf"):
            reader = PyPDF2.PdfReader(BytesIO(r.content))
            pages = [p.extract_text() for p in reader.pages[:5]]
            return {
                "type": "pdf",
                "pages": pages
            }

        return None
