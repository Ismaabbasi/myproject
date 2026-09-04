from sqlalchemy.orm import Session
from app.model.comment import Comment
from app.schema.domain_schema import DomainCreate
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status

class CommentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Comment)
        
        
    def get_comments_by_user(self, user_id: int):
        with self.session_factory() as session:
            comments = session.query(Comment).filter(Comment.user_id == user_id).order_by(Comment.id).all()
            
            if comments is None:
                return []
            
            return comments

