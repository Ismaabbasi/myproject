from typing import Optional, List
from app.schema.base_schema import ModelBaseInfo, FindBase, SearchOptions, FindResult, Blank
from pydantic import BaseModel



class CommentDetails(BaseModel):
    id: int
    question: str
    comment: str

class GetCommentResponse(BaseModel):
    projects: List[CommentDetails]

class CommentBase(BaseModel):
    user_id: int
    question_id: int
    comment: str

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    user_id: int
    question_id: int
    comment: str


class DeleteResponse(BaseModel):
    message: str


class Comment(ModelBaseInfo, CommentBase):
    pass


class FindComment(FindBase, CommentBase):
    pass


class UpsertComment(CommentBase):
    pass


class FindCommentResult(FindResult):
    founds: Optional[List[Comment]]
    search_options: Optional[SearchOptions]
