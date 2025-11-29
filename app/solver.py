import time
import httpx
import pandas as pd
import pdfplumber
import json
from app.fetcher import fetch_page
from app.submitter import submit_answer
from app.parser import parse_quiz
from openai import OpenAI
import os

client = OpenAI()

def ask(system, user):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0
    )
    return resp.choices[0].message.content

def download(url):
    with httpx.Client(timeout=30.0) as c:
        r = c.get(url)
        r.raise_for_status()
        return r.content

def solve_csv(bytes_data, question):
    df = pd.read_csv(pd.io.common.BytesIO(bytes_data))
    preview = df.head().to_csv(index=False)

    out = ask(
        "Return JSON with key 'answer' only.",
        f"Question:\n{question}\nCSV:\n{preview}"
    )

    try:
        return json.loads(out)["answer"]
    except:
        return out

def solve_pdf(bytes_data, question):
    with pdfplumber.open(pd.io.common.BytesIO(bytes_data)) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages[:3])

    out = ask(
        "Return JSON with key 'answer'.",
        f"Question:\n{question}\nPDF Extract:\n{text[:4000]}"
    )

    try:
        return json.loads(out)["answer"]
    except:
        return out

def solve_single(url, email, secret):
    html = fetch_page(url)
    parsed = parse_quiz(html)
    q = parsed["question"]
    links = parsed["links"]

    for link in links:
        if link.endswith(".csv"):
            data = download(link)
            return solve_csv(data, q), parsed.get("submit_url")
        if link.endswith(".pdf"):
            data = download(link)
            return solve_pdf(data, q), parsed.get("submit_url")

    out = ask(
        "Return JSON {'answer': <value>}.",
        f"Question: {q}"
    )

    try:
        ans = json.loads(out)["answer"]
    except:
        ans = out

    return ans, parsed.get("submit_url")

def solve_quiz(start_url, email, secret):
    url = start_url
    start = time.time()

    while True:
        if time.time() - start > 180:
            return {"correct": False, "reason": "timeout"}

        answer, submit_url = solve_single(url, email, secret)
        if not submit_url:
            submit_url = url.rstrip("/") + "/submit"

        resp = submit_answer(submit_url, email, secret, url, answer)

        if resp.get("correct") is True:
            if resp.get("url"):
                url = resp["url"]
                continue
            return {"correct": True, "reason": None}

        if resp.get("url"):
            url = resp["url"]
            continue
