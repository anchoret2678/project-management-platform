from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from app.models.knowledge import AccessLevel


# 基础模式
class KnowledgeCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0


# 创建分类
class KnowledgeCategoryCreate(KnowledgeCategoryBase):
    pass


# 更新分类
class KnowledgeCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None


# 分类响应
class KnowledgeCategoryResponse(KnowledgeCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children_count: int = 0
    documents_count: int = 0
    
    class Config:
        from_attributes = True


# 文档基础模式
class KnowledgeDocumentBase(BaseModel):
    project_id: int
    category_id: int
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: bool = True
    access_level: AccessLevel = AccessLevel.INTERNAL


# 创建文档
class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    pass


# 更新文档
class KnowledgeDocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None
    access_level: Optional[AccessLevel] = None


# 文档响应
class KnowledgeDocumentResponse(KnowledgeDocumentBase):
    id: int
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    view_count: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    project_name: Optional[str] = None
    category_name: Optional[str] = None
    creator_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# 查询参数
class KnowledgeQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None
    access_level: Optional[AccessLevel] = None
    keyword: Optional[str] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"


# 文档详情
class KnowledgeDocumentDetail(KnowledgeDocumentResponse):
    download_url: Optional[str] = None
    related_documents: List[KnowledgeDocumentResponse] = []


# 搜索响应
class KnowledgeSearchResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[KnowledgeDocumentResponse]