from fastapi import APIRouter, Request, HTTPException
from dotenv import load_dotenv
import os
import json

from app.utils.security import verify_github_signature

load_dotenv()

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    event = request.headers.get("X-GitHub-Event")

    secret = os.getenv("GITHUB_WEBHOOK_SECRET")

    if not verify_github_signature(payload, signature, secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = json.loads(payload)

    print("\n🔔 GitHub Event Received:", event)

    # Only care about pull requests for now
    if event == "pull_request":
        action = data.get("action")
        pr = data.get("pull_request", {})

        print("📌 Action:", action)
        print("📌 PR Title:", pr.get("title"))
        print("📌 PR Number:", pr.get("number"))
        print("📌 Author:", pr.get("user", {}).get("login"))
        print("📌 Base Branch:", pr.get("base", {}).get("ref"))
        print("📌 Head Branch:", pr.get("head", {}).get("ref"))

    return {"status": "received"}
