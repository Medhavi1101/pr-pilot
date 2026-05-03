import anthropic
import os
from dotenv import load_dotenv
from models import ReviewResponse, Comment

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

REVIEW_TOOL = {
    "name": "submit_review",
    "description": "Submit a structured code review with comments and score",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "Overall summary of the PR quality"
            },
            "score": {
                "type": "integer",
                "description": "Code quality score from 0 to 100",
                "minimum": 0,
                "maximum": 100
            },
            "approved": {
                "type": "boolean",
                "description": "Whether the PR should be approved"
            },
            "comments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "file": {"type": "string"},
                        "line": {"type": "integer"},
                        "severity": {
                            "type": "string",
                            "enum": ["critical", "warning", "suggestion"]
                        },
                        "message": {"type": "string"}
                    },
                    "required": ["file", "severity", "message"]
                }
            }
        },
        "required": ["summary", "score", "approved", "comments"]
    }
}


def get_mock_review() -> ReviewResponse:
    return ReviewResponse(
        summary="Mock review: Code looks generally clean with minor issues found.",
        score=75,
        approved=True,
        comments=[
            Comment(
                file="main.py",
                line=10,
                severity="suggestion",
                message="Consider adding docstrings to your functions."
            ),
            Comment(
                file="main.py",
                line=22,
                severity="warning",
                message="No error handling around the external API call."
            )
        ]
    )


async def review_pr(diff: str, pr_title: str) -> ReviewResponse:
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    # Use mock if no real API key set yet
    if not anthropic_key or anthropic_key == "your_key_here":
        print("No Anthropic API key found — returning mock review")
        return get_mock_review()

    # Real Claude call
    prompt = f"""You are an expert code reviewer. Review the following pull request.

PR Title: {pr_title}

Diff:
{diff[:8000]}

Review the code for:
- Bugs and logical errors (critical)
- Security issues (critical)
- Performance problems (warning)
- Code style and best practices (suggestion)
- Missing error handling (warning)

Use the submit_review tool to return your structured review."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        tools=[REVIEW_TOOL],
        tool_choice={"type": "any"},
        messages=[{"role": "user", "content": prompt}]
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "submit_review":
            data = block.input
            return ReviewResponse(
                summary=data["summary"],
                score=data["score"],
                approved=data["approved"],
                comments=[Comment(**c) for c in data["comments"]]
            )

    raise ValueError("Claude did not return a structured review")