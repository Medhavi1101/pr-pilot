from pydantic import BaseModel
from typing import List, Optional

class ReviewRequest(BaseModel):
    repo: str
    pr_number: int

class Comment(BaseModel):
    file: str
    line: Optional[int] = None
    severity: str
    message: str

class ReviewResponse(BaseModel):
    summary: str
    score: int
    approved: bool
    comments: List[Comment]