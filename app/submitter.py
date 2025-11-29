import httpx
import json
import time

MAX_RETRIES = 3

def submit_answer(url, email, secret, quiz_url, answer):
    payload = {
        "email": email,
        "secret": secret,
        "url": quiz_url,
        "answer": answer
    }

    last_exc = None

    for _ in range(MAX_RETRIES):
        try:
            with httpx.Client(timeout=20.0) as client:
                r = client.post(url, json=payload)
                txt = r.text.strip()

                try:
                    return json.loads(txt)
                except:
                    return {"correct": False, "raw_response_text": txt}

        except Exception as e:
            last_exc = e
            time.sleep(0.5)

    return {"correct": False, "reason": f"submit_failed after retries: {last_exc}"}
