from app.repository import CommentRepository
from app.services.base_service import BaseService

from app.schema.comment_schema import CommentCreate, CommentUpdate


class CommentService(BaseService):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        super().__init__(comment_repository)
        
    def create_comment(self, comment_data: CommentCreate):
        
        created_comment = self.comment_repository.create(comment_data)
        
        return created_comment
        
    def delete_comment(self, comment_id: int):
        
        deleted_comment = self.comment_repository.delete_by_id(comment_id)
        
        return deleted_comment
    
    
    def update_comment(self, comment_id: int, comment: str):
        
        updated_comment = self.comment_repository.update_attr(id= comment_id, column= 'comment', value= comment)
        
        return updated_comment

    # def get_user_comments(self, user_id: int):
        
    #     user_comments = self.comment_repository.get_user_comments(user_id)
        
    #     return user_comments
