"""
认证 API 测试
"""

import pytest


class TestAuthAPI:
    """认证 API 测试类"""
    
    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
    
    def test_root_endpoint(self, client):
        """测试根路径"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_login_success(self, client, admin_user):
        """测试登录成功"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testadmin", "password": "admin123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "testadmin"
    
    def test_login_invalid_credentials(self, client):
        """测试登录失败 - 错误凭证"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testadmin", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
    
    def test_login_user_not_found(self, client):
        """测试登录失败 - 用户不存在"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent", "password": "password123"}
        )
        
        assert response.status_code == 401
    
    def test_get_current_user_unauthorized(self, client):
        """测试获取当前用户 - 未授权"""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    def test_get_current_user_authorized(self, auth_client):
        """测试获取当前用户 - 已授权"""
        response = auth_client.get("/api/v1/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testadmin"
    
    def test_register_user_admin_only(self, client, normal_user):
        """测试注册用户 - 需要管理员权限"""
        from app.utils.security import create_access_token
        from app.core.config import settings
        from datetime import timedelta
        
        # 使用普通用户令牌
        access_token = create_access_token(
            data={"sub": "testuser", "role": "user"},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        client.headers["Authorization"] = f"Bearer {access_token}"
        
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "password": "password123",
                "email": "newuser@test.com",
                "full_name": "新用户",
                "role": "user",
                "department": "测试部"
            }
        )
        
        assert response.status_code == 403  # 禁止访问
    
    def test_change_password(self, auth_client):
        """测试修改密码"""
        response = auth_client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "admin123",
                "new_password": "newpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "密码修改成功"
    
    def test_refresh_token(self, auth_client):
        """测试刷新令牌"""
        response = auth_client.post("/api/v1/auth/refresh-token")
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
