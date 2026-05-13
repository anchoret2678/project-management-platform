from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.sow import (
    SOWCreate, SOWUpdate, SOWResponse,
    SOWQueryParams
)
from app.services.sow_service import SOWService
from app.core.dependencies import get_current_user, admin_only, user_or_admin
from app.models.user import User
from app.utils.exceptions import NotFoundException
import os
import uuid
from datetime import date

router = APIRouter(prefix="/sows", tags=["SOW管理"])


@router.get("/")
async def get_sows(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    project_id: int = Query(None, description="项目ID"),
    sow_number: str = Query(None, description="SOW编号"),
    title: str = Query(None, description="标题"),
    status: str = Query(None, description="状态"),
    version: str = Query(None, description="版本"),
    keyword: str = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SOW列表（分页）"""
    query_params = SOWQueryParams(
        page=page,
        page_size=page_size,
        project_id=project_id,
        sow_number=sow_number,
        title=title,
        status=status,
        version=version,
        keyword=keyword
    )

    if keyword:
        sows = SOWService.search_sows(db, keyword, (page - 1) * page_size, page_size)
        total = SOWService.count_search_sows(db, keyword)
    else:
        sows = SOWService.get_sows(db, (page - 1) * page_size, page_size, query_params)
        total = SOWService.count_sows(db, query_params)

    total_pages = (total + page_size - 1) // page_size

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": sows
    }


@router.get("/stats/summary")
async def get_sow_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SOW统计信息"""
    return SOWService.get_sow_stats(db)


@router.get("/{sow_id}")
async def get_sow(
    sow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SOW详情"""
    sow = SOWService.get_sow_by_id(db, sow_id)
    if not sow:
        raise NotFoundException("SOW不存在")
    return sow


@router.post("/")
async def create_sow(
    project_id: int = Form(...),
    sow_number: str = Form(...),
    title: str = Form(...),
    version: str = Form(...),
    description: str = Form(None),
    status: str = Form("draft"),
    effective_date: str = Form(None),
    expiry_date: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """创建SOW（仅管理员，含文件上传）"""
    # 保存文件
    upload_dir = "app/static/uploads/sows"
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1] if file.filename else ".pdf"
    file_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    file_info = {
        "file_path": file_path,
        "file_size": len(content),
        "file_type": file.content_type or "application/octet-stream"
    }

    # 构建 SOW 数据
    sow_data = SOWCreate(
        project_id=project_id,
        sow_number=sow_number,
        title=title,
        version=version,
        description=description,
        status=status,
        effective_date=date.fromisoformat(effective_date) if effective_date else None,
        expiry_date=date.fromisoformat(expiry_date) if expiry_date else None
    )

    return SOWService.create_sow(db, sow_data, file_info, current_user.id)


@router.put("/{sow_id}")
async def update_sow(
    sow_id: int,
    sow_data: SOWUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新SOW（仅管理员）"""
    return SOWService.update_sow(db, sow_id, sow_data)


@router.delete("/{sow_id}")
async def delete_sow(
    sow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """删除SOW（仅管理员）"""
    SOWService.delete_sow(db, sow_id)
    return {"message": "SOW删除成功"}


@router.get("/project/{project_id}")
async def get_sows_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目的所有SOW"""
    sows = SOWService.get_sows_by_project(db, project_id)
    return {
        "project_id": project_id,
        "total": len(sows),
        "items": sows
    }


@router.put("/{sow_id}/status")
async def update_sow_status(
    sow_id: int,
    status: str = Query(..., description="新状态"),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新SOW状态（仅管理员）"""
    from app.models.sow import SOWStatus
    sow_status = SOWStatus(status)
    sow = SOWService.update_sow_status(db, sow_id, sow_status)
    return {
        "message": "SOW状态更新成功",
        "sow": sow
    }


@router.get("/{sow_id}/file-info")
async def get_sow_file_info(
    sow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取SOW文件信息"""
    return SOWService.get_sow_file_info(db, sow_id)
