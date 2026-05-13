from sqlalchemy import Column, Integer, String, Text, Date, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    ONLINE = "online"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, nullable=False, index=True)
    project_name = Column(String(200), nullable=False, index=True)
    application_name = Column(String(200), nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False, index=True)
    launch_date = Column(Date)
    description = Column(Text)
    remark = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系 - 字符串延迟引用
    manager = relationship("User", foreign_keys=[manager_id])
    creator = relationship("User", foreign_keys=[created_by])
    
    # 反向关系 - 字符串延迟引用 + lazy="dynamic"
    cloud_assets = relationship("CloudAsset", back_populates="project", cascade="all, delete-orphan", lazy="dynamic")
    cloud_resources = relationship("CloudResource", back_populates="project", cascade="all, delete-orphan", lazy="dynamic")
    sows = relationship("SOW", back_populates="project", cascade="all, delete-orphan", lazy="dynamic")
    slas = relationship("SLA", back_populates="project", cascade="all, delete-orphan", lazy="dynamic")
    knowledge_documents = relationship("KnowledgeDocument", back_populates="project", cascade="all, delete-orphan", lazy="dynamic")
