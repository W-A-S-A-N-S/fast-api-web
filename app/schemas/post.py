from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostAuthor(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    author_id: int
    author: PostAuthor
    views: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    id: int
    title: str
    author: PostAuthor
    views: int
    created_at: datetime

    class Config:
        from_attributes = True
