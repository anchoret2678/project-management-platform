"""
pytest 配置文件
提供测试夹具和共享配置
"""

import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, get_db
from app.main import app

# 测试数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """创建测试数据库会话"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 清理数据库
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db(db_session):
    """覆盖 get_db 依赖"""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    return _override_get_db


@pytest.fixture(scope="function")
def client(override_get_db):
    """创建测试客户端"""
    from fastapi.testclient import TestClient
    
    app.dependency_overrides[get_db] = override_get_db
    
    test_client = TestClient(app)
    yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    """创建管理员用户"""
    from app.models.user import User
    from app.utils.security import get_password_hash
    
    user = User(
        username="testadmin",
        password_hash=get_password_hash("admin123"),
        email="admin@test.com",
        full_name="测试管理员",
        role="admin",
        department="IT部",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def normal_user(db_session):
    """创建普通用户"""
    from app.models.user import User
    from app.utils.security import get_password_hash
    
    user = User(
        username="testuser",
        password_hash=get_password_hash("user123"),
        email="user@test.com",
        full_name="测试用户",
        role="user",
        department="开发部",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(client, admin_user):
    """获取管理员访问令牌"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testadmin", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_client(client, admin_token):
    """带认证的测试客户端"""
    client.headers["Authorization"] = f"Bearer {admin_token}"
    return client
