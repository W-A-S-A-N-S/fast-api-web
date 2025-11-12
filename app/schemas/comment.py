from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentAuthor(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class CommentResponse(CommentBase):
    id: int
    post_id: int
    author_id: int
    author: CommentAuthor
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
