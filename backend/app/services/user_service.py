from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, PasswordChange
from app.utils.security import get_password_hash, verify_password
from app.utils.exceptions import NotFoundException, ConflictException, BadRequestException


class UserService:
    """用户服务"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        keyword: Optional[str] = None,
        role: Optional[str] = None,
        department: Optional[str] = None
    ) -> List[User]:
        """获取用户列表"""
        query = db.query(User)
        
        if keyword:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{keyword}%"),
                    User.full_name.ilike(f"%{keyword}%"),
                    User.email.ilike(f"%{keyword}%")
                )
            )
        
        if role:
            query = query.filter(User.role == role)
        
        if department:
            query = query.filter(User.department.ilike(f"%{department}%"))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_users(
        db: Session,
        keyword: Optional[str] = None,
        role: Optional[str] = None,
        department: Optional[str] = None
    ) -> int:
        """统计用户数量"""
        query = db.query(User)
        
        if keyword:
            query = query.filter(
                or_(
                    User.username.ilike(f"%{keyword}%"),
                    User.full_name.ilike(f"%{keyword}%"),
                    User.email.ilike(f"%{keyword}%")
                )
            )
        
        if role:
            query = query.filter(User.role == role)
        
        if department:
            query = query.filter(User.department.ilike(f"%{department}%"))
        
        return query.count()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        if UserService.get_user_by_username(db, user_data.username):
            raise ConflictException("用户名已存在")
        
        # 检查邮箱是否已存在
        if UserService.get_user_by_email(db, user_data.email):
            raise ConflictException("邮箱已存在")
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            password_hash=hashed_password,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            department=user_data.department,
            phone=user_data.phone
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """更新用户"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise NotFoundException("用户不存在")
        
        # 更新字段
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """删除用户"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise NotFoundException("用户不存在")
        
        # 检查是否有项目关联
        from app.models.project import Project
        project_count = db.query(Project).filter(
            (Project.manager_id == user_id) | (Project.created_by == user_id)
        ).count()
        
        if project_count > 0:
            raise BadRequestException("用户有关联项目，无法删除")
        
        db.delete(db_user)
        db.commit()
        return True
    
    @staticmethod
    def change_password(db: Session, user_id: int, password_data: PasswordChange) -> bool:
        """修改密码"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise NotFoundException("用户不存在")
        
        # 验证当前密码
        if not verify_password(password_data.current_password, db_user.password_hash):
            raise BadRequestException("当前密码错误")
        
        # 更新密码
        db_user.password_hash = get_password_hash(password_data.new_password)
        db.commit()
        return True
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def toggle_user_status(db: Session, user_id: int) -> User:
        """切换用户状态"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            raise NotFoundException("用户不存在")
        
        db_user.is_active = not db_user.is_active
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_stats(db: Session) -> dict:
        """获取用户统计信息"""
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        admin_users = db.query(User).filter(User.role == "admin").count()
        
        # 按部门统计
        department_stats = db.query(
            User.department,
            db.func.count(User.id).label('count')
        ).filter(User.department.isnot(None)).group_by(User.department).all()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "admin_users": admin_users,
            "department_stats": [
                {"department": dept, "count": count}
                for dept, count in department_stats
            ]
        }