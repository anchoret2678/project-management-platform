from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, 
    ProjectDetailResponse, ProjectQueryParams, PaginatedResponse
)
from app.services.project_service import ProjectService
from app.core.dependencies import get_current_user, admin_only, user_or_admin
from app.models.user import User
from app.utils.excel_export import ExcelExporter
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/projects", tags=["项目管理"])


@router.get("/", response_model=PaginatedResponse)
async def get_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    project_code: str = Query(None, description="项目编号"),
    project_name: str = Query(None, description="项目名称"),
    department: str = Query(None, description="所属部门"),
    status: str = Query(None, description="项目状态"),
    manager_id: int = Query(None, description="负责人ID"),
    start_date: str = Query(None, description="开始日期"),
    end_date: str = Query(None, description="结束日期"),
    keyword: str = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目列表（分页）"""
    # 构建查询参数
    query_params = ProjectQueryParams(
        page=page,
        page_size=page_size,
        project_code=project_code,
        project_name=project_name,
        department=department,
        status=status,
        manager_id=manager_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # 如果有关键词，使用搜索功能
    if keyword:
        projects = ProjectService.search_projects(db, keyword, (page-1)*page_size, page_size)
        total = ProjectService.count_search_projects(db, keyword)
    else:
        projects = ProjectService.get_projects(db, (page-1)*page_size, page_size, query_params)
        total = ProjectService.count_projects(db, query_params)
    
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": projects
    }


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目详情"""
    project_detail = ProjectService.get_project_detail(db, project_id)
    if not project_detail:
        raise NotFoundException("项目不存在")
    return project_detail


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """创建项目（仅管理员）"""
    return ProjectService.create_project(db, project_data, current_user.id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新项目（仅管理员）"""
    return ProjectService.update_project(db, project_id, project_data)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """删除项目（仅管理员）"""
    success = ProjectService.delete_project(db, project_id)
    return {"message": "项目删除成功"}


@router.get("/{project_id}/assets")
async def get_project_assets(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目所有关联资产"""
    assets = ProjectService.get_project_assets(db, project_id)
    return assets


@router.get("/stats/summary")
async def get_project_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目统计信息"""
    return ProjectService.get_project_stats(db)


@router.get("/export/excel")
async def export_projects_to_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """导出项目数据到Excel"""
    # 获取所有项目
    projects = ProjectService.get_projects(db, skip=0, limit=10000)
    
    # 格式化数据
    formatted_data = []
    for project in projects:
        project_dict = {
            "项目编号": project.project_code,
            "项目名称": project.project_name,
            "应用名称": project.application_name,
            "所属部门": project.department,
            "负责人": project.manager.full_name if project.manager else "",
            "项目状态": project.status.value,
            "上线时间": project.launch_date.strftime("%Y-%m-%d") if project.launch_date else "",
            "创建时间": project.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "更新时间": project.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "描述": project.description or "",
            "备注": project.remark or ""
        }
        formatted_data.append(project_dict)
    
    return ExcelExporter.export_projects(formatted_data)


@router.get("/search/suggestions")
async def get_project_suggestions(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目搜索建议"""
    projects = ProjectService.search_projects(db, keyword, skip=0, limit=limit)
    
    suggestions = []
    for project in projects:
        suggestions.append({
            "id": project.id,
            "project_code": project.project_code,
            "project_name": project.project_name,
            "application_name": project.application_name,
            "department": project.department
        })
    
    return {"suggestions": suggestions}


@router.get("/department/{department}")
async def get_projects_by_department(
    department: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """按部门获取项目"""
    query_params = ProjectQueryParams(
        page=page,
        page_size=page_size,
        department=department
    )
    
    projects = ProjectService.get_projects(db, (page-1)*page_size, page_size, query_params)
    total = ProjectService.count_projects(db, query_params)
    
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "department": department,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": projects
    }


@router.get("/status/{status}")
async def get_projects_by_status(
    status: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """按状态获取项目"""
    query_params = ProjectQueryParams(
        page=page,
        page_size=page_size,
        status=status
    )
    
    projects = ProjectService.get_projects(db, (page-1)*page_size, page_size, query_params)
    total = ProjectService.count_projects(db, query_params)
    
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "status": status,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": projects
    }