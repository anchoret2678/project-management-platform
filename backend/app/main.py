from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database.database import engine, Base
from app.routers import auth, projects, cloud_assets, sla, knowledge, sows
from app.utils.exceptions import CustomHTTPException
import logging

# 导入所有模型，确保 SQLAlchemy 正确注册关系映射
from app.models import (
    User, UserRole,
    SOW, SOWStatus,
    SLA, SLAStatus,
    CloudResource, CloudResourceStatus,
    CloudAsset, CloudProvider, LifecycleStatus,
    KnowledgeCategory, KnowledgeDocument, AccessLevel,
    Project, ProjectStatus,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="企业级项目管理平台API",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 全局异常处理
@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )

# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

# 注册路由
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(projects.router, prefix=settings.API_V1_PREFIX)
app.include_router(cloud_assets.router, prefix=settings.API_V1_PREFIX)
app.include_router(sla.router, prefix=settings.API_V1_PREFIX)
app.include_router(sows.router, prefix=settings.API_V1_PREFIX)
app.include_router(knowledge.router, prefix=settings.API_V1_PREFIX)

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info(f"启动 {settings.PROJECT_NAME} v{settings.VERSION}")
    
    # 创建数据库表（仅开发环境）
    if settings.DEBUG:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"数据库表创建失败: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info(f"关闭 {settings.PROJECT_NAME}")

# 根路径重定向到文档
@app.get("/")
async def root():
    return {
        "message": f"欢迎使用{settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs": "/docs" if settings.DEBUG else None,
        "api_prefix": settings.API_V1_PREFIX
    }