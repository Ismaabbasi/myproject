# from datetime import datetime
# from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from app.model.base_model import BaseModel

# class UserSelectedMeasures(BaseModel):
#     __tablename__ = "user_measures"

#     # user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
#     # sustainability_id = Column(Integer, ForeignKey("sustainability_measures.id"), nullable=False)

#     # user_measures_user = relationship("User", back_populates="user_measure")
#     # user_measures_sus = relationship("SustainabilityMeasures", back_populates="user_measure")