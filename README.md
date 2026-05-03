# AI Code Reviewer

An agentic backend API that automatically reviews GitHub Pull Requests using Claude AI.

## What it does
- POST a GitHub repo + PR number
- Fetches the real PR diff via GitHub API
- Claude analyzes it using tool use and structured output
- Returns JSON with quality score, summary, and line-by-line comments

## Tech stack
- Python + FastAPI
- Anthropic Claude API (tool use + agentic workflows)
- GitHub REST API
- Pydantic for schema validation

## Setup
cp .env.example .env
# Add your ANTHROPIC_API_KEY and GITHUB_TOKEN

pip install -r requirements.txt
uvicorn main:app --reload

## API
POST /review
{
  "repo": "owner/repo-name",
  "pr_number": 42
}