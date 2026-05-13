from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.sla import SLA, SLAStatus
from app.models.project import Project
from app.models.user import User
from app.schemas.sla import SLACreate, SLAUpdate, SLAQueryParams
from app.utils.exceptions import NotFoundException, ConflictException, BadRequestException


class SLAService:
    """SLA服务"""
    
    @staticmethod
    def get_sla_by_id(db: Session, sla_id: int) -> Optional[SLA]:
        """根据ID获取SLA"""
        return db.query(SLA).filter(SLA.id == sla_id).first()
    
    @staticmethod
    def get_sla_by_name(db: Session, agreement_name: str) -> Optional[SLA]:
        """根据协议名称获取SLA"""
        return db.query(SLA).filter(SLA.agreement_name == agreement_name).first()
    
    @staticmethod
    def get_slas(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        query_params: Optional[SLAQueryParams] = None
    ) -> List[SLA]:
        """获取SLA列表"""
        query = db.query(SLA)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(SLA.project_id == query_params.project_id)
            
            if query_params.agreement_name:
                query = query.filter(SLA.agreement_name.ilike(f"%{query_params.agreement_name}%"))
            
            if query_params.status:
                query = query.filter(SLA.status == query_params.status)
            
            if query_params.availability_min:
                query = query.filter(SLA.availability >= query_params.availability_min)
            
            if query_params.availability_max:
                query = query.filter(SLA.availability <= query_params.availability_max)
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        SLA.agreement_name.ilike(f"%{query_params.keyword}%"),
                        SLA.penalty_terms.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        # 按创建时间倒序排序
        query = query.order_by(SLA.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_slas(
        db: Session,
        query_params: Optional[SLAQueryParams] = None
    ) -> int:
        """统计SLA数量"""
        query = db.query(SLA)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(SLA.project_id == query_params.project_id)
            
            if query_params.agreement_name:
                query = query.filter(SLA.agreement_name.ilike(f"%{query_params.agreement_name}%"))
            
            if query_params.status:
                query = query.filter(SLA.status == query_params.status)
            
            if query_params.availability_min:
                query = query.filter(SLA.availability >= query_params.availability_min)
            
            if query_params.availability_max:
                query = query.filter(SLA.availability <= query_params.availability_max)
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        SLA.agreement_name.ilike(f"%{query_params.keyword}%"),
                        SLA.penalty_terms.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        return query.count()
    
    @staticmethod
    def create_sla(
        db: Session, 
        sla_data: SLACreate, 
        created_by: int
    ) -> SLA:
        """创建SLA"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == sla_data.project_id).first()
        if not project:
            raise BadRequestException("项目不存在")
        
        # 创建SLA
        db_sla = SLA(
            **sla_data.dict(),
            created_by=created_by
        )
        
        db.add(db_sla)
        db.commit()
        db.refresh(db_sla)
        return db_sla
    
    @staticmethod
    def update_sla(db: Session, sla_id: int, sla_data: SLAUpdate) -> SLA:
        """更新SLA"""
        db_sla = SLAService.get_sla_by_id(db, sla_id)
        if not db_sla:
            raise NotFoundException("SLA不存在")
        
        # 更新字段
        update_data = sla_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sla, field, value)
        
        db.commit()
        db.refresh(db_sla)
        return db_sla
    
    @staticmethod
    def delete_sla(db: Session, sla_id: int) -> bool:
        """删除SLA"""
        db_sla = SLAService.get_sla_by_id(db, sla_id)
        if not db_sla:
            raise NotFoundException("SLA不存在")
        
        db.delete(db_sla)
        db.commit()
        return True
    
    @staticmethod
    def get_sla_stats(db: Session) -> Dict[str, Any]:
        """获取SLA统计信息"""
        # 按状态统计
        status_stats = db.query(
            SLA.status,
            db.func.count(SLA.id).label('count')
        ).group_by(SLA.status).all()
        
        # 计算平均可用率
        avg_availability_result = db.query(db.func.avg(SLA.availability)).scalar()
        avg_availability = avg_availability_result or 0
        
        # 按项目统计
        project_stats = db.query(
            Project.project_name,
            db.func.count(SLA.id).label('count')
        ).join(SLA, SLA.project_id == Project.id).group_by(Project.project_name).order_by(db.func.count(SLA.id).desc()).limit(10).all()
        
        total_slas = db.query(SLA).count()
        active_slas = db.query(SLA).filter(SLA.status == SLAStatus.ACTIVE).count()
        
        return {
            "total_slas": total_slas,
            "active_slas": active_slas,
            "avg_availability": round(avg_availability, 2),
            "status_stats": [
                {"status": status.value, "count": count}
                for status, count in status_stats
            ],
            "project_stats": [
                {"project_name": project_name, "count": count}
                for project_name, count in project_stats
            ]
        }
    
    @staticmethod
    def get_slas_by_project(db: Session, project_id: int) -> List[SLA]:
        """获取项目的所有SLA"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException("项目不存在")
        
        return db.query(SLA).filter(SLA.project_id == project_id).all()
    
    @staticmethod
    def search_slas(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[SLA]:
        """搜索SLA"""
        query = db.query(SLA).filter(
            or_(
                SLA.agreement_name.ilike(f"%{keyword}%"),
                SLA.penalty_terms.ilike(f"%{keyword}%")
            )
        ).order_by(SLA.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_search_slas(db: Session, keyword: str) -> int:
        """统计搜索SLA数量"""
        return db.query(SLA).filter(
            or_(
                SLA.agreement_name.ilike(f"%{keyword}%"),
                SLA.penalty_terms.ilike(f"%{keyword}%")
            )
        ).count()
    
    @staticmethod
    def update_sla_status(db: Session, sla_id: int, status: SLAStatus) -> SLA:
        """更新SLA状态"""
        db_sla = SLAService.get_sla_by_id(db, sla_id)
        if not db_sla:
            raise NotFoundException("SLA不存在")
        
        db_sla.status = status
        db.commit()
        db.refresh(db_sla)
        return db_sla