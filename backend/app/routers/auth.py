from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, PasswordChange
from app.services.user_service import UserService
from app.utils.security import create_access_token, get_password_hash
from app.core.config import settings
from app.core.dependencies import get_current_user, admin_only
from app.models.user import User
from app.utils.exceptions import UnauthorizedException, BadRequestException

router = APIRouter(prefix="/auth", tags=["认证"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    form_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """用户登录"""
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException("用户名或密码错误")
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # 返回统一响应格式
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value if hasattr(user.role, 'value') else user.role,
                "department": user.department,
                "phone": user.phone,
                "is_active": user.is_active,
            }
        }
    }


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """注册新用户（仅管理员）"""
    return UserService.create_user(db, user_data)


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role.value if hasattr(current_user.role, 'value') else current_user.role,
            "department": current_user.department,
            "phone": current_user.phone,
            "is_active": current_user.is_active,
        }
    }


@router.put("/me", response_model=UserResponse)
async def update_current_user_info(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新当前用户信息"""
    return UserService.update_user(db, current_user.id, user_data)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """修改密码"""
    success = UserService.change_password(db, current_user.id, password_data)
    return {"message": "密码修改成功"}


@router.post("/refresh-token", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """刷新访问令牌"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username, "role": current_user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": current_user
    }


@router.get("/users/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """获取用户统计信息（仅管理员）"""
    return UserService.get_user_stats(db)


@router.post("/init-admin")
async def init_admin_user(db: Session = Depends(get_db)):
    """初始化管理员用户（仅第一次部署时使用）"""
    # 检查是否已有管理员
    admin = UserService.get_user_by_username(db, settings.ADMIN_USERNAME)
    if admin:
        raise BadRequestException("管理员用户已存在")
    
    # 创建管理员用户
    admin_data = UserCreate(
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_PASSWORD,
        email=settings.ADMIN_EMAIL,
        full_name="系统管理员",
        role="admin",
        department="IT部"
    )
    
    admin_user = UserService.create_user(db, admin_data)
    return {
        "message": "管理员用户创建成功",
        "user": admin_user
    }