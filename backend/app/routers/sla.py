from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.sla import (
    SLACreate, SLAUpdate, SLAResponse, 
    SLAQueryParams
)
from app.services.sla_service import SLAService
from app.core.dependencies import get_current_user, admin_only, user_or_admin
from app.models.user import User

router = APIRouter(prefix="/slas", tags=["SLA管理"])


@router.get("/", response_model=List[SLAResponse])
async def get_slas(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    project_id: int = Query(None, description="项目ID"),
    status: str = Query(None, description="状态"),
    availability_min: float = Query(None, description="最低可用率"),
    availability_max: float = Query(None, description="最高可用率"),
    keyword: str = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SLA列表（分页）"""
    # 构建查询参数
    query_params = SLAQueryParams(
        page=page,
        page_size=page_size,
        project_id=project_id,
        status=status,
        availability_min=availability_min,
        availability_max=availability_max,
        keyword=keyword
    )
    
    # 如果有关键词，使用搜索功能
    if keyword:
        slas = SLAService.search_slas(db, keyword, (page-1)*page_size, page_size)
        total = SLAService.count_search_slas(db, keyword)
    else:
        slas = SLAService.get_slas(db, (page-1)*page_size, page_size, query_params)
        total = SLAService.count_slas(db, query_params)
    
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": slas
    }


@router.get("/{sla_id}", response_model=SLAResponse)
async def get_sla(
    sla_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SLA详情"""
    sla = SLAService.get_sla_by_id(db, sla_id)
    if not sla:
        raise HTTPException(status_code=404, detail="SLA不存在")
    return sla


@router.post("/", response_model=SLAResponse)
async def create_sla(
    sla_data: SLACreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """创建SLA（仅管理员）"""
    return SLAService.create_sla(db, sla_data, current_user.id)


@router.put("/{sla_id}", response_model=SLAResponse)
async def update_sla(
    sla_id: int,
    sla_data: SLAUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新SLA（仅管理员）"""
    return SLAService.update_sla(db, sla_id, sla_data)


@router.delete("/{sla_id}")
async def delete_sla(
    sla_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """删除SLA（仅管理员）"""
    success = SLAService.delete_sla(db, sla_id)
    return {"message": "SLA删除成功"}


@router.get("/project/{project_id}")
async def get_slas_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目的所有SLA"""
    slas = SLAService.get_slas_by_project(db, project_id)
    return {
        "project_id": project_id,
        "total": len(slas),
        "items": slas
    }


@router.get("/stats/summary")
async def get_sla_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SLA统计信息"""
    return SLAService.get_sla_stats(db)


@router.put("/{sla_id}/status")
async def update_sla_status(
    sla_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新SLA状态（仅管理员）"""
    from app.models.sla import SLAStatus
    sla_status = SLAStatus(status)
    sla = SLAService.update_sla_status(db, sla_id, sla_status)
    return {
        "message": "SLA状态更新成功",
        "sla": sla
    }