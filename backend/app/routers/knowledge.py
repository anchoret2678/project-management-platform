from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.knowledge import (
    KnowledgeCreate, KnowledgeUpdate, KnowledgeResponse, 
    KnowledgeQueryParams
)
from app.services.knowledge_service import KnowledgeService
from app.core.dependencies import get_current_user, admin_only, user_or_admin
from app.models.user import User
from app.utils.file_handler import FileHandler
from app.utils.exceptions import NotFoundException
import os

router = APIRouter(prefix="/knowledge", tags=["知识库管理"])


@router.get("/", response_model=List[KnowledgeResponse])
async def get_knowledge(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    project_id: int = Query(None, description="项目ID"),
    category: str = Query(None, description="分类"),
    tags: str = Query(None, description="标签"),
    keyword: str = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取知识库列表（分页）"""
    # 构建查询参数
    query_params = KnowledgeQueryParams(
        page=page,
        page_size=page_size,
        project_id=project_id,
        category=category,
        tags=tags,
        keyword=keyword
    )
    
    # 如果有关键词，使用搜索功能
    if keyword:
        knowledges = KnowledgeService.search_knowledges(db, keyword, (page-1)*page_size, page_size)
        total = KnowledgeService.count_search_knowledges(db, keyword)
    else:
        knowledges = KnowledgeService.get_knowledges(db, (page-1)*page_size, page_size, query_params)
        total = KnowledgeService.count_knowledges(db, query_params)
    
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": knowledges
    }


@router.get("/{knowledge_id}", response_model=KnowledgeResponse)
async def get_knowledge_item(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取知识库文档详情"""
    knowledge = KnowledgeService.get_knowledge_by_id(db, knowledge_id)
    if not knowledge:
        raise NotFoundException("知识库文档不存在")
    return knowledge


@router.post("/", response_model=KnowledgeResponse)
async def create_knowledge(
    document_title: str = Form(..., description="文档标题"),
    description: str = Form(None, description="描述"),
    project_id: int = Form(..., description="项目ID"),
    category: str = Form(..., description="分类"),
    tags: str = Form(None, description="标签"),
    file: UploadFile = File(None, description="上传文件"),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """创建知识库文档（仅管理员）"""
    file_info = {}
    
    if file:
        # 保存文件
        file_path = await FileHandler.save_file(file, "knowledge")
        file_info = {
            "file_path": file_path,
            "file_name": file.filename,
            "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            "file_type": file.content_type or "unknown"
        }
    
    from app.schemas.knowledge import KnowledgeCreate
    knowledge_data = KnowledgeCreate(
        document_title=document_title,
        description=description,
        project_id=project_id,
        category=category,
        tags=tags,
        file_path=file_info.get("file_path"),
        file_name=file_info.get("file_name"),
        file_size=file_info.get("file_size"),
        file_type=file_info.get("file_type")
    )
    
    return KnowledgeService.create_knowledge(db, knowledge_data, file_info, current_user.id)


@router.put("/{knowledge_id}", response_model=KnowledgeResponse)
async def update_knowledge(
    knowledge_id: int,
    knowledge_data: KnowledgeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """更新知识库文档（仅管理员）"""
    return KnowledgeService.update_knowledge(db, knowledge_id, knowledge_data)


@router.delete("/{knowledge_id}")
async def delete_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """删除知识库文档（仅管理员）"""
    success = KnowledgeService.delete_knowledge(db, knowledge_id)
    return {"message": "知识库文档删除成功"}


@router.get("/project/{project_id}")
async def get_knowledges_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取项目的所有知识库文档"""
    knowledges = KnowledgeService.get_knowledges_by_project(db, project_id)
    return {
        "project_id": project_id,
        "total": len(knowledges),
        "items": knowledges
    }


@router.get("/stats/summary")
async def get_knowledge_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取知识库统计信息"""
    return KnowledgeService.get_knowledge_stats(db)


@router.get("/category-stats")
async def get_category_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """获取知识库分类统计"""
    stats = KnowledgeService.get_knowledge_stats(db)
    return {
        "category_stats": stats.get("category_stats", []),
        "total_knowledges": stats.get("total_knowledges", 0)
    }


@router.get("/{knowledge_id}/download")
async def download_knowledge_file(
    knowledge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_or_admin)
):
    """下载知识库文档"""
    from fastapi.responses import FileResponse
    from app.utils.file_handler import FileHandler
    
    knowledge = KnowledgeService.get_knowledge_by_id(db, knowledge_id)
    if not knowledge or not knowledge.file_path:
        raise NotFoundException("文件不存在")
    
    if not os.path.exists(knowledge.file_path):
        raise NotFoundException("文件不存在")
    
    return FileResponse(
        path=knowledge.file_path,
        filename=knowledge.file_name or os.path.basename(knowledge.file_path),
        media_type=knowledge.file_type or "application/octet-stream"
    )