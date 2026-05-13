from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.utils.security import verify_token, check_permission
from app.utils.exceptions import UnauthorizedException, ForbiddenException


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if not user:
        raise UnauthorizedException("用户不存在")
    if not user.is_active:
        raise UnauthorizedException("用户已被禁用")
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise UnauthorizedException("用户已被禁用")
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """要求管理员权限"""
    if current_user.role != "admin":
        raise ForbiddenException("需要管理员权限")
    return current_user


def require_user_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """要求用户或管理员权限"""
    return current_user


class PermissionChecker:
    """权限检查器"""
    
    def __init__(self, required_role: str = "user"):
        self.required_role = required_role
    
    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if not check_permission(current_user.role, self.required_role):
            raise ForbiddenException(f"需要{self.required_role}权限")
        return current_user


# 权限依赖
admin_only = PermissionChecker("admin")
user_or_admin = PermissionChecker("user")


def get_pagination_params(
    page: int = 1,
    page_size: int = 10
):
    """获取分页参数"""
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 1
    if page_size > 100:
        page_size = 100
    
    return {
        "skip": (page - 1) * page_size,
        "limit": page_size,
        "page": page,
        "page_size": page_size
    }


def get_search_params(
    keyword: str = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    """获取搜索参数"""
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "sort_order": sort_order
    }