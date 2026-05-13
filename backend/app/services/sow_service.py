from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.sow import SOW, SOWStatus
from app.models.project import Project
from app.models.user import User
from app.schemas.sow import SOWCreate, SOWUpdate, SOWQueryParams
from app.utils.exceptions import NotFoundException, ConflictException, BadRequestException
from app.utils.file_handler import FileHandler
import os


class SOWService:
    """SOW服务"""
    
    @staticmethod
    def get_sow_by_id(db: Session, sow_id: int) -> Optional[SOW]:
        """根据ID获取SOW"""
        return db.query(SOW).filter(SOW.id == sow_id).first()
    
    @staticmethod
    def get_sow_by_number(db: Session, sow_number: str) -> Optional[SOW]:
        """根据SOW编号获取SOW"""
        return db.query(SOW).filter(SOW.sow_number == sow_number).first()
    
    @staticmethod
    def get_sows(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        query_params: Optional[SOWQueryParams] = None
    ) -> List[SOW]:
        """获取SOW列表"""
        query = db.query(SOW)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(SOW.project_id == query_params.project_id)
            
            if query_params.sow_number:
                query = query.filter(SOW.sow_number.ilike(f"%{query_params.sow_number}%"))
            
            if query_params.title:
                query = query.filter(SOW.title.ilike(f"%{query_params.title}%"))
            
            if query_params.status:
                query = query.filter(SOW.status == query_params.status)
            
            if query_params.version:
                query = query.filter(SOW.version.ilike(f"%{query_params.version}%"))
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        SOW.title.ilike(f"%{query_params.keyword}%"),
                        SOW.description.ilike(f"%{query_params.keyword}%"),
                        SOW.sow_number.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        # 按创建时间倒序排序
        query = query.order_by(SOW.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_sows(
        db: Session,
        query_params: Optional[SOWQueryParams] = None
    ) -> int:
        """统计SOW数量"""
        query = db.query(SOW)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(SOW.project_id == query_params.project_id)
            
            if query_params.sow_number:
                query = query.filter(SOW.sow_number.ilike(f"%{query_params.sow_number}%"))
            
            if query_params.title:
                query = query.filter(SOW.title.ilike(f"%{query_params.title}%"))
            
            if query_params.status:
                query = query.filter(SOW.status == query_params.status)
            
            if query_params.version:
                query = query.filter(SOW.version.ilike(f"%{query_params.version}%"))
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        SOW.title.ilike(f"%{query_params.keyword}%"),
                        SOW.description.ilike(f"%{query_params.keyword}%"),
                        SOW.sow_number.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        return query.count()
    
    @staticmethod
    def create_sow(
        db: Session, 
        sow_data: SOWCreate, 
        file_info: Dict[str, Any],
        created_by: int
    ) -> SOW:
        """创建SOW"""
        # 检查SOW编号是否已存在
        if SOWService.get_sow_by_number(db, sow_data.sow_number):
            raise ConflictException("SOW编号已存在")
        
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == sow_data.project_id).first()
        if not project:
            raise BadRequestException("项目不存在")
        
        # 创建SOW
        db_sow = SOW(
            **sow_data.dict(),
            file_path=file_info["file_path"],
            file_size=file_info["file_size"],
            file_type=file_info["file_type"],
            created_by=created_by
        )
        
        db.add(db_sow)
        db.commit()
        db.refresh(db_sow)
        return db_sow
    
    @staticmethod
    def update_sow(db: Session, sow_id: int, sow_data: SOWUpdate) -> SOW:
        """更新SOW"""
        db_sow = SOWService.get_sow_by_id(db, sow_id)
        if not db_sow:
            raise NotFoundException("SOW不存在")
        
        # 更新字段
        update_data = sow_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sow, field, value)
        
        db.commit()
        db.refresh(db_sow)
        return db_sow
    
    @staticmethod
    def delete_sow(db: Session, sow_id: int) -> bool:
        """删除SOW"""
        db_sow = SOWService.get_sow_by_id(db, sow_id)
        if not db_sow:
            raise NotFoundException("SOW不存在")
        
        # 删除文件
        if db_sow.file_path and os.path.exists(db_sow.file_path):
            os.remove(db_sow.file_path)
        
        db.delete(db_sow)
        db.commit()
        return True
    
    @staticmethod
    def get_sow_stats(db: Session) -> Dict[str, Any]:
        """获取SOW统计信息"""
        # 按状态统计
        status_stats = db.query(
            SOW.status,
            db.func.count(SOW.id).label('count')
        ).group_by(SOW.status).all()
        
        # 按项目统计
        project_stats = db.query(
            Project.project_name,
            db.func.count(SOW.id).label('count')
        ).join(SOW, SOW.project_id == Project.id).group_by(Project.project_name).order_by(db.func.count(SOW.id).desc()).limit(10).all()
        
        total_sows = db.query(SOW).count()
        approved_sows = db.query(SOW).filter(SOW.status == SOWStatus.APPROVED).count()
        
        # 按年份统计
        year_stats = db.query(
            db.func.year(SOW.created_at).label('year'),
            db.func.count(SOW.id).label('count')
        ).group_by(db.func.year(SOW.created_at)).order_by(db.func.year(SOW.created_at).desc()).all()
        
        return {
            "total_sows": total_sows,
            "approved_sows": approved_sows,
            "status_stats": [
                {"status": status.value, "count": count}
                for status, count in status_stats
            ],
            "project_stats": [
                {"project_name": project_name, "count": count}
                for project_name, count in project_stats
            ],
            "year_stats": [
                {"year": year, "count": count}
                for year, count in year_stats
            ]
        }
    
    @staticmethod
    def get_sows_by_project(db: Session, project_id: int) -> List[SOW]:
        """获取项目的所有SOW"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException("项目不存在")
        
        return db.query(SOW).filter(SOW.project_id == project_id).all()
    
    @staticmethod
    def search_sows(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[SOW]:
        """搜索SOW"""
        query = db.query(SOW).filter(
            or_(
                SOW.title.ilike(f"%{keyword}%"),
                SOW.description.ilike(f"%{keyword}%"),
                SOW.sow_number.ilike(f"%{keyword}%")
            )
        ).order_by(SOW.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_search_sows(db: Session, keyword: str) -> int:
        """统计搜索SOW数量"""
        return db.query(SOW).filter(
            or_(
                SOW.title.ilike(f"%{keyword}%"),
                SOW.description.ilike(f"%{keyword}%"),
                SOW.sow_number.ilike(f"%{keyword}%")
            )
        ).count()
    
    @staticmethod
    def update_sow_status(db: Session, sow_id: int, status: SOWStatus) -> SOW:
        """更新SOW状态"""
        db_sow = SOWService.get_sow_by_id(db, sow_id)
        if not db_sow:
            raise NotFoundException("SOW不存在")
        
        db_sow.status = status
        db.commit()
        db.refresh(db_sow)
        return db_sow
    
    @staticmethod
    def get_sow_file_info(db: Session, sow_id: int) -> Dict[str, Any]:
        """获取SOW文件信息"""
        db_sow = SOWService.get_sow_by_id(db, sow_id)
        if not db_sow:
            raise NotFoundException("SOW不存在")
        
        file_exists = os.path.exists(db_sow.file_path) if db_sow.file_path else False
        
        return {
            "sow_id": db_sow.id,
            "sow_number": db_sow.sow_number,
            "title": db_sow.title,
            "file_path": db_sow.file_path,
            "file_size": db_sow.file_size,
            "file_type": db_sow.file_type,
            "file_exists": file_exists,
            "downloadable": file_exists
        }