from fastapi import FastAPI, Request, HTTPException
from app.solver import solve_quiz

EXPECTED_SECRET = "z1F9@8qW4r"

app = FastAPI()

@app.post("/")
async def handle(req: Request):
    try:
        payload = await req.json()
        print("PAYLOAD RECEIVED:", payload)
    except:
        raise HTTPException(400, "Invalid JSON")

    if payload.get("secret") != EXPECTED_SECRET:
        raise HTTPException(403, "Invalid secret")

    email = payload.get("email")
    url = payload.get("url")

    if not email or not url:
        raise HTTPException(400, "Missing required fields")

    result = solve_quiz(url, email, payload["secret"])
    return result
