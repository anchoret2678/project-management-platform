from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.knowledge import Knowledge, KnowledgeCategory
from app.models.project import Project
from app.models.user import User
from app.schemas.knowledge import KnowledgeCreate, KnowledgeUpdate, KnowledgeQueryParams
from app.utils.exceptions import NotFoundException, BadRequestException
from app.utils.file_handler import FileHandler
import os


class KnowledgeService:
    """知识库服务"""
    
    @staticmethod
    def get_knowledge_by_id(db: Session, knowledge_id: int) -> Optional[Knowledge]:
        """根据ID获取知识库文档"""
        return db.query(Knowledge).filter(Knowledge.id == knowledge_id).first()
    
    @staticmethod
    def get_knowledge_by_title(db: Session, document_title: str) -> Optional[Knowledge]:
        """根据标题获取知识库文档"""
        return db.query(Knowledge).filter(Knowledge.document_title == document_title).first()
    
    @staticmethod
    def get_knowledges(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        query_params: Optional[KnowledgeQueryParams] = None
    ) -> List[Knowledge]:
        """获取知识库列表"""
        query = db.query(Knowledge)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(Knowledge.project_id == query_params.project_id)
            
            if query_params.category:
                query = query.filter(Knowledge.category == query_params.category)
            
            if query_params.document_title:
                query = query.filter(Knowledge.document_title.ilike(f"%{query_params.document_title}%"))
            
            # 标签搜索
            if query_params.tags:
                for tag in query_params.tags.split(','):
                    query = query.filter(Knowledge.tags.ilike(f"%{tag.strip()}%"))
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        Knowledge.document_title.ilike(f"%{query_params.keyword}%"),
                        Knowledge.description.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        # 按创建时间倒序排序
        query = query.order_by(Knowledge.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_knowledges(
        db: Session,
        query_params: Optional[KnowledgeQueryParams] = None
    ) -> int:
        """统计知识库数量"""
        query = db.query(Knowledge)
        
        if query_params:
            # 应用过滤条件
            if query_params.project_id:
                query = query.filter(Knowledge.project_id == query_params.project_id)
            
            if query_params.category:
                query = query.filter(Knowledge.category == query_params.category)
            
            if query_params.document_title:
                query = query.filter(Knowledge.document_title.ilike(f"%{query_params.document_title}%"))
            
            # 标签搜索
            if query_params.tags:
                for tag in query_params.tags.split(','):
                    query = query.filter(Knowledge.tags.ilike(f"%{tag.strip()}%"))
            
            # 关键词搜索
            if query_params.keyword:
                query = query.filter(
                    or_(
                        Knowledge.document_title.ilike(f"%{query_params.keyword}%"),
                        Knowledge.description.ilike(f"%{query_params.keyword}%")
                    )
                )
        
        return query.count()
    
    @staticmethod
    def create_knowledge(
        db: Session, 
        knowledge_data: KnowledgeCreate, 
        file_info: Dict[str, Any],
        created_by: int
    ) -> Knowledge:
        """创建知识库文档"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == knowledge_data.project_id).first()
        if not project:
            raise BadRequestException("项目不存在")
        
        # 创建知识库文档
        db_knowledge = Knowledge(
            **knowledge_data.dict(),
            file_path=file_info.get("file_path"),
            file_size=file_info.get("file_size"),
            file_type=file_info.get("file_type"),
            created_by=created_by
        )
        
        db.add(db_knowledge)
        db.commit()
        db.refresh(db_knowledge)
        return db_knowledge
    
    @staticmethod
    def update_knowledge(db: Session, knowledge_id: int, knowledge_data: KnowledgeUpdate) -> Knowledge:
        """更新知识库文档"""
        db_knowledge = KnowledgeService.get_knowledge_by_id(db, knowledge_id)
        if not db_knowledge:
            raise NotFoundException("知识库文档不存在")
        
        # 更新字段
        update_data = knowledge_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_knowledge, field, value)
        
        db.commit()
        db.refresh(db_knowledge)
        return db_knowledge
    
    @staticmethod
    def delete_knowledge(db: Session, knowledge_id: int) -> bool:
        """删除知识库文档"""
        db_knowledge = KnowledgeService.get_knowledge_by_id(db, knowledge_id)
        if not db_knowledge:
            raise NotFoundException("知识库文档不存在")
        
        # 删除文件
        if db_knowledge.file_path and os.path.exists(db_knowledge.file_path):
            os.remove(db_knowledge.file_path)
        
        db.delete(db_knowledge)
        db.commit()
        return True
    
    @staticmethod
    def get_knowledge_stats(db: Session) -> Dict[str, Any]:
        """获取知识库统计信息"""
        # 按分类统计
        category_stats = db.query(
            Knowledge.category,
            db.func.count(Knowledge.id).label('count')
        ).group_by(Knowledge.category).all()
        
        # 按项目统计
        project_stats = db.query(
            Project.project_name,
            db.func.count(Knowledge.id).label('count')
        ).join(Knowledge, Knowledge.project_id == Project.id).group_by(Project.project_name).order_by(db.func.count(Knowledge.id).desc()).limit(10).all()
        
        total_knowledges = db.query(Knowledge).count()
        
        # 按年份统计
        year_stats = db.query(
            db.func.year(Knowledge.created_at).label('year'),
            db.func.count(Knowledge.id).label('count')
        ).group_by(db.func.year(Knowledge.created_at)).order_by(db.func.year(Knowledge.created_at).desc()).all()
        
        return {
            "total_knowledges": total_knowledges,
            "category_stats": [
                {"category": category.value, "count": count}
                for category, count in category_stats
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
    def get_knowledges_by_project(db: Session, project_id: int) -> List[Knowledge]:
        """获取项目的所有知识库文档"""
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException("项目不存在")
        
        return db.query(Knowledge).filter(Knowledge.project_id == project_id).all()
    
    @staticmethod
    def search_knowledges(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Knowledge]:
        """搜索知识库文档"""
        query = db.query(Knowledge).filter(
            or_(
                Knowledge.document_title.ilike(f"%{keyword}%"),
                Knowledge.description.ilike(f"%{keyword}%")
            )
        ).order_by(Knowledge.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_search_knowledges(db: Session, keyword: str) -> int:
        """统计搜索知识库文档数量"""
        return db.query(Knowledge).filter(
            or_(
                Knowledge.document_title.ilike(f"%{keyword}%"),
                Knowledge.description.ilike(f"%{keyword}%")
            )
        ).count()
    
    @staticmethod
    def get_knowledge_file_info(db: Session, knowledge_id: int) -> Dict[str, Any]:
        """获取知识库文档文件信息"""
        db_knowledge = KnowledgeService.get_knowledge_by_id(db, knowledge_id)
        if not db_knowledge:
            raise NotFoundException("知识库文档不存在")
        
        file_exists = os.path.exists(db_knowledge.file_path) if db_knowledge.file_path else False
        
        return {
            "knowledge_id": db_knowledge.id,
            "document_title": db_knowledge.document_title,
            "file_path": db_knowledge.file_path,
            "file_size": db_knowledge.file_size,
            "file_type": db_knowledge.file_type,
            "file_exists": file_exists,
            "downloadable": file_exists
        }