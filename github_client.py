import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def get_pr_diff(repo: str, pr_number: int) -> str:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Accept": "application/vnd.github.v3.diff"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.text


async def get_pr_metadata(repo: str, pr_number: int) -> dict:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()