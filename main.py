from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from models import ReviewRequest, ReviewResponse
from github_client import get_pr_diff, get_pr_metadata
from reviewer import review_pr
import os

load_dotenv()
app = FastAPI(title="AI Code Reviewer")

@app.post("/review", response_model=ReviewResponse)
async def review_pull_request(request: ReviewRequest):
    try:
        # 1. Fetch PR data from GitHub
        diff = await get_pr_diff(request.repo, request.pr_number)
        metadata = await get_pr_metadata(request.repo, request.pr_number)
        pr_title = metadata.get("title", "Untitled PR")

        # 2. Send to Claude for review
        review = await review_pr(diff, pr_title)
        return review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/test-github/{repo:path}/{pr_number}")
async def test_github(repo: str, pr_number: int):
    diff = await get_pr_diff(repo, pr_number)
    return {"diff_length": len(diff), "preview": diff[:500]}



@app.get("/debug-env")
async def debug_env():
    return {
        "github_token_set": bool(os.getenv("GITHUB_TOKEN")),
        "github_token_preview": os.getenv("GITHUB_TOKEN", "NOT FOUND")[:10],
        "anthropic_key_set": bool(os.getenv("ANTHROPIC_API_KEY")),
    }