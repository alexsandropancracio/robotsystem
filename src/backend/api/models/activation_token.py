# backend/api/models/activation_token.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from backend.api.database.base import Base # seu Base do SQLAlchemy

class ActivationToken(Base):
    __tablename__ = "activation_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(6), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)

    user = relationship("User", back_populates="activation_tokens")
