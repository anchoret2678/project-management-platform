from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime
from app.models.cloud_asset import CloudProvider, LifecycleStatus


# 基础模式
class CloudAssetBase(BaseModel):
    project_id: int
    cloud_provider: CloudProvider
    resource_type: str = Field(..., min_length=1, max_length=100)
    instance_spec: Optional[str] = Field(None, max_length=100)
    region: str = Field(..., min_length=1, max_length=50)
    zone: Optional[str] = Field(None, max_length=50)
    account_info: Optional[str] = Field(None, max_length=200)
    ip_address: Optional[str] = Field(None, max_length=50)
    config_json: Optional[Any] = None
    lifecycle: LifecycleStatus = LifecycleStatus.RUNNING


# 创建云资产
class CloudAssetCreate(CloudAssetBase):
    pass


# 更新云资产
class CloudAssetUpdate(BaseModel):
    cloud_provider: Optional[CloudProvider] = None
    resource_type: Optional[str] = Field(None, min_length=1, max_length=100)
    instance_spec: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, min_length=1, max_length=50)
    zone: Optional[str] = Field(None, max_length=50)
    account_info: Optional[str] = Field(None, max_length=200)
    ip_address: Optional[str] = Field(None, max_length=50)
    config_json: Optional[Any] = None
    lifecycle: Optional[LifecycleStatus] = None


# 云资产响应
class CloudAssetResponse(CloudAssetBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    project_name: Optional[str] = None
    creator_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# 查询参数
class CloudAssetQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    project_id: Optional[int] = None
    cloud_provider: Optional[CloudProvider] = None
    resource_type: Optional[str] = None
    region: Optional[str] = None
    lifecycle: Optional[LifecycleStatus] = None
    keyword: Optional[str] = None


# 导出数据
class CloudAssetExport(BaseModel):
    items: List[CloudAssetResponse]
    export_time: datetime = Field(default_factory=datetime.now)
    total_count: int