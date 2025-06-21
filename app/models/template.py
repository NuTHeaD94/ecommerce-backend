from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # amazon, ebay, walmart, bigcommerce
    template_name = Column(String, nullable=False)
    file_path = Column(String)  # Path to generated template file
    file_url = Column(String)  # URL to download template
    status = Column(String, default="generated")  # generated, downloaded, uploaded
    template_data = Column(JSON)  # Store the actual template data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    product_id = Column(Integer, ForeignKey("products.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    product = relationship("Product", back_populates="templates")
    created_by = relationship("User", back_populates="templates")