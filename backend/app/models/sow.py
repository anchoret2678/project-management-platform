from sqlalchemy import Column, Integer, String, Text, BigInteger, Date, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class SOWStatus(str, enum.Enum):
    DRAFT = "draft"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"


class SOW(Base):
    __tablename__ = "sows"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    sow_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    version = Column(String(20), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger)
    file_type = Column(String(50))
    description = Column(Text)
    status = Column(Enum(SOWStatus), default=SOWStatus.DRAFT, nullable=False, index=True)
    effective_date = Column(Date, index=True)
    expiry_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系 - 字符串延迟引用
    project = relationship("Project", back_populates="sows")
    creator = relationship("User", foreign_keys=[created_by])
