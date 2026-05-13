from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://pmp_user:Pmp@123456@localhost:3306/project_management_platform"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 应用配置
    DEBUG: bool = True
    ALLOWED_HOSTS: List[str] = ["*"]
    UPLOAD_DIR: str = "./app/static/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 管理员初始账号
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_EMAIL: str = "admin@company.com"
    
    # 项目配置
    PROJECT_NAME: str = "企业项目管理平台"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()