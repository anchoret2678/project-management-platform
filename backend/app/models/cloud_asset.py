from sqlalchemy import Column, Integer, String, Enum, JSON, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum


class CloudProvider(str, enum.Enum):
    ALIYUN = "aliyun"
    HUAWEI = "huawei"
    TENCENT = "tencent"
    SELF_BUILT = "self_built"


class LifecycleStatus(str, enum.Enum):
    CREATING = "creating"
    RUNNING = "running"
    STOPPED = "stopped"
    DELETING = "deleting"
    DELETED = "deleted"


class CloudAsset(Base):
    __tablename__ = "cloud_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    cloud_provider = Column(Enum(CloudProvider), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)
    instance_spec = Column(String(100))
    region = Column(String(50), nullable=False, index=True)
    zone = Column(String(50))
    account_info = Column(String(200))
    ip_address = Column(String(50))
    config_json = Column(JSON)
    lifecycle = Column(Enum(LifecycleStatus), default=LifecycleStatus.RUNNING, nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关系
    project = relationship("Project", back_populates="cloud_assets")
    creator = relationship("User", foreign_keys=[created_by])