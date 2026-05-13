from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from app.models.sla import SLAStatus


# 基础模式
class SLABase(BaseModel):
    project_id: int
    sla_number: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=200)
    availability_rate: Decimal = Field(..., ge=0, le=100)
    response_time: str = Field(..., min_length=1, max_length=50)
    fault_handling_time: str = Field(..., min_length=1, max_length=50)
    maintenance_window: Optional[str] = Field(None, max_length=200)
    penalty_terms: Optional[str] = None
    description: Optional[str] = None
    status: SLAStatus = SLAStatus.ACTIVE
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


# 创建SLA
class SLACreate(SLABase):
    pass


# 更新SLA
class SLAUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    availability_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    response_time: Optional[str] = Field(None, min_length=1, max_length=50)
    fault_handling_time: Optional[str] = Field(None, min_length=1, max_length=50)
    maintenance_window: Optional[str] = Field(None, max_length=200)
    penalty_terms: Optional[str] = None
    description: Optional[str] = None
    status: Optional[SLAStatus] = None
    effective_date: Optional[date] = None
    expiry_date: Optional[date] = None


# SLA响应
class SLAResponse(SLABase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    project_name: Optional[str] = None
    creator_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# 查询参数
class SLAQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    project_id: Optional[int] = None
    sla_number: Optional[str] = None
    title: Optional[str] = None
    status: Optional[SLAStatus] = None
    min_availability: Optional[Decimal] = Field(None, ge=0, le=100)
    keyword: Optional[str] = None


# SLA统计
class SLAStats(BaseModel):
    total_count: int
    active_count: int
    expired_count: int
    average_availability: Decimal
    projects_with_sla: int