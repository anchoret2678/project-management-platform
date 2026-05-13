from sqlalchemy import Column, Integer, String, Text, BigInteger, Boolean, Enum, JSON, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class AccessLevel(str, enum.Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"


class KnowledgeCategory(Base):
    __tablename__ = "knowledge_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("knowledge_categories.id"))
    sort_order = Column(Integer, default=0, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 自引用关系
    parent = relationship("KnowledgeCategory", remote_side=[id], backref="children")
    documents = relationship("KnowledgeDocument", back_populates="category")


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("knowledge_categories.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text)
    file_path = Column(String(500))
    file_type = Column(String(50))
    file_size = Column(BigInteger)
    tags = Column(JSON)
    view_count = Column(Integer, default=0, index=True)
    is_published = Column(Boolean, default=True, index=True)
    access_level = Column(Enum(AccessLevel), default=AccessLevel.INTERNAL, nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project", back_populates="knowledge_documents")
    category = relationship("KnowledgeCategory", back_populates="documents")
    creator = relationship("User", foreign_keys=[created_by])