from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from datetime import date
from app.models.project import Project, ProjectStatus
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectQueryParams
from app.utils.exceptions import NotFoundException, ConflictException, BadRequestException


class ProjectService:
    """项目服务"""
    
    @staticmethod
    def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
        """根据ID获取项目"""
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def get_project_by_code(db: Session, project_code: str) -> Optional[Project]:
        """根据项目编号获取项目"""
        return db.query(Project).filter(Project.project_code == project_code).first()
    
    @staticmethod
    def get_projects(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        query_params: Optional[ProjectQueryParams] = None
    ) -> List[Project]:
        """获取项目列表"""
        query = db.query(Project)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_code:
                query = query.filter(Project.project_code.ilike(f"%{query_params.project_code}%"))
            
            if query_params.project_name:
                query = query.filter(Project.project_name.ilike(f"%{query_params.project_name}%"))
            
            if query_params.department:
                query = query.filter(Project.department.ilike(f"%{query_params.department}%"))
            
            if query_params.status:
                query = query.filter(Project.status == query_params.status)
            
            if query_params.manager_id:
                query = query.filter(Project.manager_id == query_params.manager_id)
            
            if query_params.start_date:
                query = query.filter(Project.launch_date >= query_params.start_date)
            
            if query_params.end_date:
                query = query.filter(Project.launch_date <= query_params.end_date)
        
        # 按创建时间倒序排序
        query = query.order_by(Project.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_projects(
        db: Session,
        query_params: Optional[ProjectQueryParams] = None
    ) -> int:
        """统计项目数量"""
        query = db.query(Project)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_code:
                query = query.filter(Project.project_code.ilike(f"%{query_params.project_code}%"))
            
            if query_params.project_name:
                query = query.filter(Project.project_name.ilike(f"%{query_params.project_name}%"))
            
            if query_params.department:
                query = query.filter(Project.department.ilike(f"%{query_params.department}%"))
            
            if query_params.status:
                query = query.filter(Project.status == query_params.status)
            
            if query_params.manager_id:
                query = query.filter(Project.manager_id == query_params.manager_id)
            
            if query_params.start_date:
                query = query.filter(Project.launch_date >= query_params.start_date)
            
            if query_params.end_date:
                query = query.filter(Project.launch_date <= query_params.end_date)
        
        return query.count()
    
    @staticmethod
    def create_project(db: Session, project_data: ProjectCreate, created_by: int) -> Project:
        """创建项目"""
        # 检查项目编号是否已存在
        if ProjectService.get_project_by_code(db, project_data.project_code):
            raise ConflictException("项目编号已存在")
        
        # 检查负责人是否存在
        manager = db.query(User).filter(User.id == project_data.manager_id).first()
        if not manager:
            raise BadRequestException("负责人不存在")
        
        # 创建项目
        db_project = Project(
            **project_data.dict(),
            created_by=created_by
        )
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def update_project(db: Session, project_id: int, project_data: ProjectUpdate) -> Project:
        """更新项目"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise NotFoundException("项目不存在")
        
        # 如果更新了负责人，检查负责人是否存在
        if project_data.manager_id:
            manager = db.query(User).filter(User.id == project_data.manager_id).first()
            if not manager:
                raise BadRequestException("负责人不存在")
        
        # 更新字段
        update_data = project_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        """删除项目"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise NotFoundException("项目不存在")
        
        db.delete(db_project)
        db.commit()
        return True
    
    @staticmethod
    def get_project_detail(db: Session, project_id: int) -> Dict[str, Any]:
        """获取项目详情（包含关联数据统计）"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise NotFoundException("项目不存在")
        
        # 获取关联数据统计
        from app.models.cloud_asset import CloudAsset
        from app.models.sow import SOW
        from app.models.sla import SLA
        from app.models.knowledge import KnowledgeDocument
        
        cloud_assets_count = db.query(CloudAsset).filter(CloudAsset.project_id == project_id).count()
        sows_count = db.query(SOW).filter(SOW.project_id == project_id).count()
        slas_count = db.query(SLA).filter(SLA.project_id == project_id).count()
        knowledge_documents_count = db.query(KnowledgeDocument).filter(KnowledgeDocument.project_id == project_id).count()
        
        # 获取负责人和创建人信息
        manager = db.query(User).filter(User.id == db_project.manager_id).first()
        creator = db.query(User).filter(User.id == db_project.created_by).first()
        
        result = {
            "id": db_project.id,
            "project_code": db_project.project_code,
            "project_name": db_project.project_name,
            "application_name": db_project.application_name,
            "department": db_project.department,
            "manager_id": db_project.manager_id,
            "manager_name": manager.full_name if manager else None,
            "status": db_project.status,
            "launch_date": db_project.launch_date,
            "description": db_project.description,
            "remark": db_project.remark,
            "created_by": db_project.created_by,
            "creator_name": creator.full_name if creator else None,
            "created_at": db_project.created_at,
            "updated_at": db_project.updated_at,
            "cloud_assets_count": cloud_assets_count,
            "sows_count": sows_count,
            "slas_count": slas_count,
            "knowledge_documents_count": knowledge_documents_count
        }
        
        return result
    
    @staticmethod
    def get_project_assets(db: Session, project_id: int) -> Dict[str, Any]:
        """获取项目所有关联资产"""
        db_project = ProjectService.get_project_by_id(db, project_id)
        if not db_project:
            raise NotFoundException("项目不存在")
        
        # 获取所有关联数据
        from app.models.cloud_asset import CloudAsset
        from app.models.sow import SOW
        from app.models.sla import SLA
        from app.models.knowledge import KnowledgeDocument
        
        cloud_assets = db.query(CloudAsset).filter(CloudAsset.project_id == project_id).all()
        sows = db.query(SOW).filter(SOW.project_id == project_id).all()
        slas = db.query(SLA).filter(SLA.project_id == project_id).all()
        knowledge_documents = db.query(KnowledgeDocument).filter(KnowledgeDocument.project_id == project_id).all()
        
        return {
            "project": db_project,
            "cloud_assets": cloud_assets,
            "sows": sows,
            "slas": slas,
            "knowledge_documents": knowledge_documents
        }
    
    @staticmethod
    def get_project_stats(db: Session) -> Dict[str, Any]:
        """获取项目统计信息"""
        # 按状态统计
        status_stats = db.query(
            Project.status,
            func.count(Project.id).label('count')
        ).group_by(Project.status).all()
        
        # 按部门统计
        department_stats = db.query(
            Project.department,
            func.count(Project.id).label('count')
        ).group_by(Project.department).all()
        
        # 按年份统计
        year_stats = db.query(
            func.year(Project.created_at).label('year'),
            func.count(Project.id).label('count')
        ).group_by(func.year(Project.created_at)).order_by(func.year(Project.created_at).desc()).all()
        
        total_projects = db.query(Project).count()
        active_projects = db.query(Project).filter(Project.status.in_([
            ProjectStatus.IN_PROGRESS, 
            ProjectStatus.TESTING, 
            ProjectStatus.ONLINE
        ])).count()
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "status_stats": [
                {"status": status.value, "count": count}
                for status, count in status_stats
            ],
            "department_stats": [
                {"department": dept, "count": count}
                for dept, count in department_stats
            ],
            "year_stats": [
                {"year": year, "count": count}
                for year, count in year_stats
            ]
        }
    
    @staticmethod
    def search_projects(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """搜索项目"""
        query = db.query(Project).filter(
            or_(
                Project.project_code.ilike(f"%{keyword}%"),
                Project.project_name.ilike(f"%{keyword}%"),
                Project.application_name.ilike(f"%{keyword}%"),
                Project.department.ilike(f"%{keyword}%"),
                Project.description.ilike(f"%{keyword}%")
            )
        ).order_by(Project.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_search_projects(db: Session, keyword: str) -> int:
        """统计搜索结果数量"""
        return db.query(Project).filter(
            or_(
                Project.project_code.ilike(f"%{keyword}%"),
                Project.project_name.ilike(f"%{keyword}%"),
                Project.application_name.ilike(f"%{keyword}%"),
                Project.department.ilike(f"%{keyword}%"),
                Project.description.ilike(f"%{keyword}%")
            )
        ).count()