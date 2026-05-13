from sqlalchemy import Column, Integer, String, Text, Date, Enum, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class CloudResourceStatus(str, enum.Enum):
    AVAILABLE = "available"
    USED = "used"
    RESERVED = "reserved"
    EXPIRED = "expired"


class CloudResource(Base):
    __tablename__ = "cloud_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    resource_code = Column(String(50), unique=True, nullable=False, index=True)  # 资源编码
    resource_type = Column(String(100), nullable=False, index=True)  # 云服务器/云存储/云数据库/弹性IP
    resource_quota = Column(DECIMAL(10, 2), nullable=False)  # 资源配额
    used_quota = Column(DECIMAL(10, 2), nullable=False, default=0)  # 已使用配额
    provider = Column(String(100), nullable=False)  # 云服务商：阿里云/腾讯云/华为云/AWS
    region = Column(String(50), nullable=False)  # 地域：华东1/华北2/华南3
    status = Column(Enum(CloudResourceStatus), default=CloudResourceStatus.AVAILABLE, nullable=False, index=True)
    effective_date = Column(Date, index=True)  # 生效日期
    expiry_date = Column(Date)  # 过期日期
    description = Column(Text)  # 资源描述
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系 - 字符串延迟引用
    project = relationship("Project", back_populates="cloud_resources")
    creator = relationship("User", foreign_keys=[created_by])
