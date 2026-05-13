from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.cloud_asset import CloudAsset, CloudProvider, LifecycleStatus
from app.models.project import Project
from app.models.user import User
from app.schemas.cloud_asset import CloudAssetCreate, CloudAssetUpdate, CloudAssetQueryParams
from app.utils.exceptions import NotFoundException, BadRequestException


class CloudAssetService:
    """云资产服务"""
    
    @staticmethod
    def get_cloud_asset_by_id(db: Session, asset_id: int) -> Optional[CloudAsset]:
        """根据ID获取云资产"""
        return db.query(CloudAsset).filter(CloudAsset.id == asset_id).first()
    
    @staticmethod
    def get_cloud_assets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        query_params: Optional[CloudAssetQueryParams] = None
    ) -> List[CloudAsset]:
        """获取云资产列表"""
        query = db.query(CloudAsset)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(CloudAsset.project_id == query_params.project_id)
            
            if query_params.cloud_provider:
                query = query.filter(CloudAsset.cloud_provider == query_params.cloud_provider)
            
            if query_params.resource_type:
                query = query.filter(CloudAsset.resource_type.ilike(f"%{query_params.resource_type}%"))
            
            if query_params.region:
                query = query.filter(CloudAsset.region.ilike(f"%{query_params.region}%"))
            
            if query_params.lifecycle:
                query = query.filter(CloudAsset.lifecycle == query_params.lifecycle)
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        CloudAsset.account_info.ilike(f"%{query_params.keyword}%"),
                        CloudAsset.ip_address.ilike(f"%{query_params.keyword}%"),
                        CloudAsset.instance_spec.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        # 按创建时间倒序排序
        query = query.order_by(CloudAsset.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_cloud_assets(
        db: Session,
        query_params: Optional[CloudAssetQueryParams] = None
    ) -> int:
        """统计云资产数量"""
        query = db.query(CloudAsset)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(CloudAsset.project_id == query_params.project_id)
            
            if query_params.cloud_provider:
                query = query.filter(CloudAsset.cloud_provider == query_params.cloud_provider)
            
            if query_params.resource_type:
                query = query.filter(CloudAsset.resource_type.ilike(f"%{query_params.resource_type}%"))
            
            if query_params.region:
                query = query.filter(CloudAsset.region.ilike(f"%{query_params.region}%"))
            
            if query_params.lifecycle:
                query = query.filter(CloudAsset.lifecycle == query_params.lifecycle)
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        CloudAsset.account_info.ilike(f"%{query_params.keyword}%"),
                        CloudAsset.ip_address.ilike(f"%{query_params.keyword}%"),
                        CloudAsset.instance_spec.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        return query.count()
    
    @staticmethod
    def create_cloud_asset(db: Session, asset_data: CloudAssetCreate, created_by: int) -> CloudAsset:
        """创建云资产"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == asset_data.project_id).first()
        if not project:
            raise BadRequestException("项目不存在")
        
        # 创建云资产
        db_asset = CloudAsset(
            **asset_data.dict(),
            created_by=created_by
        )
        
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
    
    @staticmethod
    def update_cloud_asset(db: Session, asset_id: int, asset_data: CloudAssetUpdate) -> CloudAsset:
        """更新云资产"""
        db_asset = CloudAssetService.get_cloud_asset_by_id(db, asset_id)
        if not db_asset:
            raise NotFoundException("云资产不存在")
        
        # 如果更新了项目ID，检查项目是否存在
        if asset_data.project_id and asset_data.project_id != db_asset.project_id:
            project = db.query(Project).filter(Project.id == asset_data.project_id).first()
            if not project:
                raise BadRequestException("项目不存在")
        
        # 更新字段
        update_data = asset_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asset, field, value)
        
        db.commit()
        db.refresh(db_asset)
        return db_asset
    
    @staticmethod
    def delete_cloud_asset(db: Session, asset_id: int) -> bool:
        """删除云资产"""
        db_asset = CloudAssetService.get_cloud_asset_by_id(db, asset_id)
        if not db_asset:
            raise NotFoundException("云资产不存在")
        
        db.delete(db_asset)
        db.commit()
        return True
    
    @staticmethod
    def get_cloud_asset_stats(db: Session) -> Dict[str, Any]:
        """获取云资产统计信息"""
        # 按云厂商统计
        provider_stats = db.query(
            CloudAsset.cloud_provider,
            db.func.count(CloudAsset.id).label('count')
        ).group_by(CloudAsset.cloud_provider).all()
        
        # 按资源类型统计
        resource_stats = db.query(
            CloudAsset.resource_type,
            db.func.count(CloudAsset.id).label('count')
        ).group_by(CloudAsset.resource_type).order_by(db.func.count(CloudAsset.id).desc()).limit(10).all()
        
        # 按地域统计
        region_stats = db.query(
            CloudAsset.region,
            db.func.count(CloudAsset.id).label('count')
        ).group_by(CloudAsset.region).order_by(db.func.count(CloudAsset.id).desc()).limit(10).all()
        
        # 按生命周期统计
        lifecycle_stats = db.query(
            CloudAsset.lifecycle,
            db.func.count(CloudAsset.id).label('count')
        ).group_by(CloudAsset.lifecycle).all()
        
        total_assets = db.query(CloudAsset).count()
        running_assets = db.query(CloudAsset).filter(CloudAsset.lifecycle == LifecycleStatus.RUNNING).count()
        
        return {
            "total_assets": total_assets,
            "running_assets": running_assets,
            "provider_stats": [
                {"provider": provider.value, "count": count}
                for provider, count in provider_stats
            ],
            "resource_stats": [
                {"resource_type": resource_type, "count": count}
                for resource_type, count in resource_stats
            ],
            "region_stats": [
                {"region": region, "count": count}
                for region, count in region_stats
            ],
            "lifecycle_stats": [
                {"lifecycle": lifecycle.value, "count": count}
                for lifecycle, count in lifecycle_stats
            ]
        }
    
    @staticmethod
    def get_assets_by_project(db: Session, project_id: int) -> List[CloudAsset]:
        """获取项目的所有云资产"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException("项目不存在")
        
        return db.query(CloudAsset).filter(CloudAsset.project_id == project_id).all()
    
    @staticmethod
    def search_cloud_assets(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[CloudAsset]:
        """搜索云资产"""
        query = db.query(CloudAsset).filter(
            or_(
                CloudAsset.account_info.ilike(f"%{keyword}%"),
                CloudAsset.ip_address.ilike(f"%{keyword}%"),
                CloudAsset.instance_spec.ilike(f"%{keyword}%"),
                CloudAsset.region.ilike(f"%{keyword}%"),
                CloudAsset.resource_type.ilike(f"%{keyword}%")
            )
        ).order_by(CloudAsset.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_search_cloud_assets(db: Session, keyword: str) -> int:
        """统计搜索云资产数量"""
        return db.query(CloudAsset).filter(
            or_(
                CloudAsset.account_info.ilike(f"%{keyword}%"),
                CloudAsset.ip_address.ilike(f"%{keyword}%"),
                CloudAsset.instance_spec.ilike(f"%{keyword}%"),
                CloudAsset.region.ilike(f"%{keyword}%"),
                CloudAsset.resource_type.ilike(f"%{keyword}%")
            )
        ).count()
    
    @staticmethod
    def get_assets_by_provider(db: Session, provider: CloudProvider) -> List[CloudAsset]:
        """按云厂商获取云资产"""
        return db.query(CloudAsset).filter(CloudAsset.cloud_provider == provider).all()
    
    @staticmethod
    def update_asset_lifecycle(db: Session, asset_id: int, lifecycle: LifecycleStatus) -> CloudAsset:
        """更新云资产生命周期"""
        db_asset = CloudAssetService.get_cloud_asset_by_id(db, asset_id)
        if not db_asset:
            raise NotFoundException("云资产不存在")
        
        db_asset.lifecycle = lifecycle
        db.commit()
        db.refresh(db_asset)
        return db_asset