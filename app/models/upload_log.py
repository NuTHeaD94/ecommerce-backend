from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class UploadLog(Base):
    __tablename__ = "upload_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)  # File size in bytes
    total_rows = Column(Integer)
    processed_rows = Column(Integer)
    successful_rows = Column(Integer)
    failed_rows = Column(Integer)
    status = Column(String, default="processing")  # processing, completed, failed
    error_message = Column(Text)
    processing_data = Column(JSON)  # Store any processing details
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", back_populates="upload_logs")