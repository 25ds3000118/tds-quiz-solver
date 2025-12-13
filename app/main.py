from fastapi import FastAPI, Request, HTTPException
from solver import QuizSolver
from settings import settings
import asyncio

app = FastAPI()

@app.post("/")
async def solve(request: Request):
    body = await request.json()

    if body["secret"] != settings.SECRET:
        raise HTTPException(403)

    solver = QuizSolver()
    asyncio.create_task(solver.solve(body["url"]))

    return {"status": "accepted"}

@app.get("/health")
def health():
    return {"ok": True}
