from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from app.models.sow import SOWStatus


# 基础模式
class SOWBase(BaseModel):
    project_id: int
    sow_number: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    version: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None
    status: SOWStatus = SOWStatus.DRAFT
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


# 创建SOW（包含文件上传）
class SOWCreate(SOWBase):
    pass


# 更新SOW
class SOWUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    version: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    status: Optional[SOWStatus] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


# SOW响应
class SOWResponse(SOWBase):
    id: int
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    project_name: Optional[str] = None
    creator_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# 文件上传
class FileUpload(BaseModel):
    file_path: str
    file_size: int
    file_type: str


# 查询参数
class SOWQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    project_id: Optional[int] = None
    sow_number: Optional[str] = None
    title: Optional[str] = None
    status: Optional[SOWStatus] = None
    version: Optional[str] = None
    keyword: Optional[str] = None


# SOW详情（包含文件信息）
class SOWDetailResponse(SOWResponse):
    download_url: Optional[str] = None
    preview_url: Optional[str] = None