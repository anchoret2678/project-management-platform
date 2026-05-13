from sqlalchemy import Column, Integer, String, Text, Date, Enum, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class SLAStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class SLA(Base):
    __tablename__ = "slas"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    sla_number = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    availability_rate = Column(DECIMAL(5, 2), nullable=False, index=True)
    response_time = Column(String(50), nullable=False)
    fault_handling_time = Column(String(50), nullable=False)
    maintenance_window = Column(String(200))
    penalty_terms = Column(Text)
    description = Column(Text)
    status = Column(Enum(SLAStatus), default=SLAStatus.ACTIVE, nullable=False, index=True)
    effective_date = Column(Date, index=True)
    expiry_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系 - 字符串延迟引用
    project = relationship("Project", back_populates="slas")
    creator = relationship("User", foreign_keys=[created_by])
