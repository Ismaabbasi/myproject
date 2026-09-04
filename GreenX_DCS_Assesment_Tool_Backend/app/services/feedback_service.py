from app.repository import StrengthsRepository, ImprovementsRepository
from app.services.base_service import BaseService

from app.schema.feedback_schema import FeedbackCreate, StrengthCreate, ImprovementCreate


class FeedbackService(BaseService):
    def __init__(self, strengths_repository: StrengthsRepository, improvements_repository: ImprovementsRepository):
        self.strengths_repository = strengths_repository
        self.improvements_repository = improvements_repository
        
    def create_feedback(self, feedback_data: FeedbackCreate):
        
        strength = feedback_data.strength
        improvement = feedback_data.improvement
        user_id = feedback_data.user_id
        
        if strength:
            strength_data = StrengthCreate(strength=strength, user_id=user_id)
            self.strengths_repository.create(strength_data)
            
        if improvement:
            improvement_data = ImprovementCreate(improvement=improvement, user_id=user_id)
            self.improvements_repository.create(improvement_data)
            
        return "Feedback sent successfully"
        
