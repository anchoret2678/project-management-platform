"""
用户服务测试
"""

import pytest
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, PasswordChange
from app.utils.exceptions import NotFoundException, ConflictException, BadRequestException


class TestUserService:
    """用户服务测试类"""
    
    def test_get_user_by_id(self, db_session, admin_user):
        """测试根据ID获取用户"""
        user = UserService.get_user_by_id(db_session, admin_user.id)
        assert user is not None
        assert user.id == admin_user.id
        assert user.username == "testadmin"
    
    def test_get_user_by_id_not_found(self, db_session):
        """测试获取不存在的用户"""
        user = UserService.get_user_by_id(db_session, 9999)
        assert user is None
    
    def test_get_user_by_username(self, db_session, admin_user):
        """测试根据用户名获取用户"""
        user = UserService.get_user_by_username(db_session, "testadmin")
        assert user is not None
        assert user.username == "testadmin"
    
    def test_get_user_by_email(self, db_session, admin_user):
        """测试根据邮箱获取用户"""
        user = UserService.get_user_by_email(db_session, "admin@test.com")
        assert user is not None
        assert user.email == "admin@test.com"
    
    def test_create_user_success(self, db_session):
        """测试成功创建用户"""
        user_data = UserCreate(
            username="newuser",
            password="password123",
            email="newuser@test.com",
            full_name="新用户",
            role="user",
            department="测试部"
        )
        
        user = UserService.create_user(db_session, user_data)
        
        assert user is not None
        assert user.username == "newuser"
        assert user.email == "newuser@test.com"
    
    def test_create_user_duplicate_username(self, db_session, admin_user):
        """测试创建重复用户名的用户"""
        user_data = UserCreate(
            username="testadmin",  # 已存在
            password="password123",
            email="new@test.com",
            full_name="新用户",
            role="user",
            department="测试部"
        )
        
        with pytest.raises(ConflictException, match="用户名已存在"):
            UserService.create_user(db_session, user_data)
    
    def test_create_user_duplicate_email(self, db_session, admin_user):
        """测试创建重复邮箱的用户"""
        user_data = UserCreate(
            username="newuser2",
            password="password123",
            email="admin@test.com",  # 已存在
            full_name="新用户",
            role="user",
            department="测试部"
        )
        
        with pytest.raises(ConflictException, match="邮箱已存在"):
            UserService.create_user(db_session, user_data)
    
    def test_update_user(self, db_session, admin_user):
        """测试更新用户"""
        update_data = UserUpdate(
            full_name="更新后的名称",
            email="updated@test.com"
        )
        
        user = UserService.update_user(db_session, admin_user.id, update_data)
        
        assert user.full_name == "更新后的名称"
        assert user.email == "updated@test.com"
    
    def test_update_user_not_found(self, db_session):
        """测试更新不存在的用户"""
        update_data = UserUpdate(full_name="新名称")
        
        with pytest.raises(NotFoundException, match="用户不存在"):
            UserService.update_user(db_session, 9999, update_data)
    
    def test_delete_user(self, db_session):
        """测试删除用户"""
        from app.models.user import User
        
        # 创建测试用户
        user_data = UserCreate(
            username="deleteuser",
            password="password123",
            email="delete@test.com",
            full_name="删除测试",
            role="user",
            department="测试部"
        )
        user = UserService.create_user(db_session, user_data)
        
        # 删除用户
        result = UserService.delete_user(db_session, user.id)
        assert result is True
        
        # 验证用户已删除
        deleted_user = UserService.get_user_by_id(db_session, user.id)
        assert deleted_user is None
    
    def test_delete_user_not_found(self, db_session):
        """测试删除不存在的用户"""
        with pytest.raises(NotFoundException, match="用户不存在"):
            UserService.delete_user(db_session, 9999)
    
    def test_change_password_success(self, db_session, admin_user):
        """测试修改密码成功"""
        password_data = PasswordChange(
            current_password="admin123",
            new_password="newpassword123"
        )
        
        result = UserService.change_password(db_session, admin_user.id, password_data)
        assert result is True
        
        # 验证新密码有效
        from app.utils.security import verify_password
        user = UserService.get_user_by_id(db_session, admin_user.id)
        assert verify_password("newpassword123", user.password_hash)
    
    def test_change_password_wrong_current(self, db_session, admin_user):
        """测试修改密码时当前密码错误"""
        password_data = PasswordChange(
            current_password="wrongpassword",
            new_password="newpassword123"
        )
        
        with pytest.raises(BadRequestException, match="当前密码错误"):
            UserService.change_password(db_session, admin_user.id, password_data)
    
    def test_authenticate_user_success(self, db_session, admin_user):
        """测试用户认证成功"""
        user = UserService.authenticate_user(db_session, "testadmin", "admin123")
        assert user is not None
        assert user.username == "testadmin"
    
    def test_authenticate_user_invalid_credentials(self, db_session):
        """测试用户认证失败 - 错误凭证"""
        user = UserService.authenticate_user(db_session, "testadmin", "wrongpassword")
        assert user is None
    
    def test_authenticate_user_not_found(self, db_session):
        """测试用户认证失败 - 用户不存在"""
        user = UserService.authenticate_user(db_session, "nonexistent", "password123")
        assert user is None
    
    def test_toggle_user_status(self, db_session, admin_user):
        """测试切换用户状态"""
        # 初始状态为 True
        assert admin_user.is_active is True
        
        # 切换状态
        user = UserService.toggle_user_status(db_session, admin_user.id)
        assert user.is_active is False
        
        # 再次切换
        user = UserService.toggle_user_status(db_session, admin_user.id)
        assert user.is_active is True
    
    def test_get_users_list(self, db_session, admin_user, normal_user):
        """测试获取用户列表"""
        users = UserService.get_users(db_session, skip=0, limit=100)
        assert len(users) >= 2
    
    def test_count_users(self, db_session, admin_user, normal_user):
        """测试统计用户数量"""
        count = UserService.count_users(db_session)
        assert count >= 2
    
    def test_get_user_stats(self, db_session, admin_user, normal_user):
        """测试获取用户统计信息"""
        stats = UserService.get_user_stats(db_session)
        
        assert "total_users" in stats
        assert "active_users" in stats
        assert "admin_users" in stats
        assert "department_stats" in stats
        
        assert stats["total_users"] >= 2
