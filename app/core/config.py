import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "7625086805")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # File Upload
    UPLOAD_DIR: str = "app/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".xlsx", ".xls"}
    
    # E-commerce Platforms
    SUPPORTED_PLATFORMS: list = ["amazon", "ebay", "walmart", "bigcommerce"]
    
    # API Settings
    AMAZON_API_KEY: str = os.getenv("AMAZON_API_KEY", "")
    EBAY_API_KEY: str = os.getenv("EBAY_API_KEY", "")
    WALMART_API_KEY: str = os.getenv("WALMART_API_KEY", "")
    BIGCOMMERCE_API_KEY: str = os.getenv("BIGCOMMERCE_API_KEY", "")

settings = Settings()