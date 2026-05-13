from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from app.models.project import ProjectStatus


# 基础模式
class ProjectBase(BaseModel):
    project_code: str = Field(..., min_length=1, max_length=50)
    project_name: str = Field(..., min_length=1, max_length=200)
    application_name: str = Field(..., min_length=1, max_length=200)
    department: str = Field(..., min_length=1, max_length=100)
    manager_id: int
    status: ProjectStatus = ProjectStatus.PLANNING
    launch_date: Optional[date] = None
    description: Optional[str] = None
    remark: Optional[str] = None


# 创建项目
class ProjectCreate(ProjectBase):
    pass


# 更新项目
class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, min_length=1, max_length=200)
    application_name: Optional[str] = Field(None, min_length=1, max_length=200)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    manager_id: Optional[int] = None
    status: Optional[ProjectStatus] = None
    launch_date: Optional[date] = None
    description: Optional[str] = None
    remark: Optional[str] = None


# 项目响应（包含关联数据）
class ProjectResponse(ProjectBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    manager_name: Optional[str] = None
    creator_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# 项目详情响应（包含所有关联资产）
class ProjectDetailResponse(ProjectResponse):
    cloud_assets_count: int = 0
    sows_count: int = 0
    slas_count: int = 0
    knowledge_documents_count: int = 0


# 分页查询参数
class ProjectQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    project_code: Optional[str] = None
    project_name: Optional[str] = None
    department: Optional[str] = None
    status: Optional[ProjectStatus] = None
    manager_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# 分页响应
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ProjectResponse]