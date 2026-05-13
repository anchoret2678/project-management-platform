from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.cloud_asset import (
    CloudAssetCreate, CloudAssetUpdate, CloudAssetResponse, 
    CloudAssetQueryParams, CloudAssetExport
)
from app.services.cloud_asset_service import CloudAssetService
from app.core.dependencies import get_current_user, admin_only, user_or_admin
from app.models.user import User
from app.utils.excel_export import ExcelExporter
from app.utils.exceptions import NotFoundException
from app.models.cloud_asset import CloudProvider, LifecycleStatus

router = APIRouter(prefix="/cloud-assets", tags=["云资产管理"])


@router.get("/", response_model=List[CloudAssetResponse])
async def get_cloud_assets(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    project_id: int = Query(None, description="项目ID"),
    cloud_provider: CloudProvider = Query(None, description="云厂商"),
    resource_type: str = Query(None, description="资源类型"),
    region: str = Query(None, description="地域"),
    lifecycle: LifecycleStatus = Query(None, description="生命周期"),
    keyword: str = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取云资产列表（分页）"""
    # 构建查询参数
    query_params = CloudAssetQueryParams(
        page=page,
        page_size=page_size,
        project_id=project_id,
        cloud_provider=cloud_provider,
        resource_type=resource_type,
        region=region,
        lifecycle=lifecycle,
        keyword=keyword
    )
    
    # 如果有关键词，使用搜索功能
    if keyword:
        assets = CloudAssetService.search_cloud_assets(db, keyword, (page-1)*page_size, page_size)
        total = CloudAssetService.count_search_cloud_assets(db, keyword)
    else:
        assets = CloudAssetService.get_cloud_assets(db, (page-1)*page_size, page_size, query_params)
        total = CloudAssetService.count_cloud_assets(db, query_params)
    
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": assets
    }


@router.get("/{asset_id}", response_model=CloudAssetResponse)
async def get_cloud_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取云资产详情"""
    asset = CloudAssetService.get_cloud_asset_by_id(db, asset_id)
    if not asset:
        raise NotFoundException("云资产不存在")
    return asset


@router.post("/", response_model=CloudAssetResponse)
async def create_cloud_asset(
    asset_data: CloudAssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """创建云资产（仅管理员）"""
    return CloudAssetService.create_cloud_asset(db, asset_data, current_user.id)


@router.put("/{asset_id}", response_model=CloudAssetResponse)
async def update_cloud_asset(
    asset_id: int,
    asset_data: CloudAssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新云资产（仅管理员）"""
    return CloudAssetService.update_cloud_asset(db, asset_id, asset_data)


@router.delete("/{asset_id}")
async def delete_cloud_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """删除云资产（仅管理员）"""
    success = CloudAssetService.delete_cloud_asset(db, asset_id)
    return {"message": "云资产删除成功"}


@router.get("/project/{project_id}")
async def get_assets_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目的所有云资产"""
    assets = CloudAssetService.get_assets_by_project(db, project_id)
    return {
        "project_id": project_id,
        "total": len(assets),
        "items": assets
    }


@router.get("/stats/summary")
async def get_cloud_asset_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取云资产统计信息"""
    return CloudAssetService.get_cloud_asset_stats(db)


@router.get("/export/excel")
async def export_cloud_assets_to_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """导出云资产数据到Excel"""
    # 获取所有云资产
    assets = CloudAssetService.get_cloud_assets(db, skip=0, limit=10000)
    
    # 格式化数据
    formatted_data = []
    for asset in assets:
        asset_dict = {
            "项目ID": asset.project_id,
            "项目名称": asset.project.project_name if asset.project else "",
            "云厂商": asset.cloud_provider.value,
            "资源类型": asset.resource_type,
            "实例规格": asset.instance_spec or "",
            "地域": asset.region,
            "可用区": asset.zone or "",
            "账号信息": asset.account_info or "",
            "IP地址": asset.ip_address or "",
            "生命周期": asset.lifecycle.value,
            "创建时间": asset.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "更新时间": asset.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "创建人": asset.creator.full_name if asset.creator else ""
        }
        formatted_data.append(asset_dict)
    
    return ExcelExporter.export_cloud_assets(formatted_data)


@router.get("/provider/{provider}")
async def get_assets_by_provider(
    provider: CloudProvider,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """按云厂商获取云资产"""
    assets = CloudAssetService.get_assets_by_provider(db, provider)
    return {
        "provider": provider.value,
        "total": len(assets),
        "items": assets
    }


@router.put("/{asset_id}/lifecycle")
async def update_asset_lifecycle(
    asset_id: int,
    lifecycle: LifecycleStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新云资产生命周期（仅管理员）"""
    asset = CloudAssetService.update_asset_lifecycle(db, asset_id, lifecycle)
    return {
        "message": "生命周期更新成功",
        "asset": asset
    }


@router.get("/search/suggestions")
async def get_cloud_asset_suggestions(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取云资产搜索建议"""
    assets = CloudAssetService.search_cloud_assets(db, keyword, skip=0, limit=limit)
    
    suggestions = []
    for asset in assets:
        suggestions.append({
            "id": asset.id,
            "resource_type": asset.resource_type,
            "instance_spec": asset.instance_spec or "",
            "region": asset.region,
            "cloud_provider": asset.cloud_provider.value,
            "project_name": asset.project.project_name if asset.project else ""
        })
    
    return {"suggestions": suggestions}


@router.get("/lifecycle/stats")
async def get_lifecycle_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取生命周期统计"""
    stats = CloudAssetService.get_cloud_asset_stats(db)
    return {
        "lifecycle_stats": stats.get("lifecycle_stats", []),
        "total_assets": stats.get("total_assets", 0),
        "running_assets": stats.get("running_assets", 0)
    }