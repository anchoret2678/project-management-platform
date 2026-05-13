# 企业项目管理平台 - 后端服务

基于FastAPI开发的企业级项目管理平台后端服务。

## 功能特性

- ✅ 完整的用户认证和权限管理
- ✅ 项目全生命周期管理
- ✅ 云平台资产管理
- ✅ SOW工作说明书管理
- ✅ SLA服务等级协议管理
- ✅ 项目知识库管理
- ✅ 文件上传和在线预览
- ✅ Excel数据导出
- ✅ RESTful API设计
- ✅ 完整的异常处理

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: MySQL 8.0 + SQLAlchemy 2.0
- **认证**: JWT + bcrypt
- **文件处理**: python-multipart
- **Excel导出**: openpyxl + pandas
- **部署**: Docker + Docker Compose

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd project-management-platform/backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

确保MySQL服务已启动，然后执行数据库初始化：

```bash
# 创建数据库和表结构
mysql -u root -p < ../database/complete_schema.sql
```

### 3. 环境变量配置

复制环境变量模板并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接等信息。

### 4. 启动服务

```bash
# 开发模式（热重载）
python run.py

# 或使用uvicorn直接启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后，访问以下地址：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 5. 初始化管理员

首次启动后，需要初始化管理员账户：

```bash
# 使用API初始化管理员
curl -X POST http://localhost:8000/api/v1/auth/init-admin
```

或直接使用默认管理员账户登录：
- 用户名: admin
- 密码: admin123

## Docker部署

### 使用Docker Compose一键部署

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 单独构建Docker镜像

```bash
# 构建镜像
docker build -t pmp-backend .

# 运行容器
docker run -d \
  --name pmp-backend \
  -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://pmp_user:Pmp@123456@host.docker.internal:3306/project_management_platform \
  pmp-backend
```

## API文档

启动服务后，访问 `/docs` 查看完整的API文档，包括：
- 所有端点的详细说明
- 请求/响应示例
- 在线测试功能

## 项目结构

```
backend/
├── app/
│   ├── core/              # 核心配置
│   │   ├── config.py      # 应用配置
│   │   └── dependencies.py # 依赖注入
│   ├── database/          # 数据库配置
│   │   └── database.py    # 数据库连接
│   ├── models/            # 数据模型
│   │   ├── user.py        # 用户模型
│   │   ├── project.py     # 项目模型
│   │   ├── cloud_asset.py # 云资产模型
│   │   ├── sow.py         # SOW模型
│   │   ├── sla.py         # SLA模型
│   │   └── knowledge.py   # 知识库模型
│   ├── schemas/           # Pydantic模式
│   │   ├── user.py        # 用户模式
│   │   ├── project.py     # 项目模式
│   │   ├── cloud_asset.py # 云资产模式
│   │   ├── sow.py         # SOW模式
│   │   ├── sla.py         # SLA模式
│   │   └── knowledge.py   # 知识库模式
│   ├── routers/           # 路由
│   │   ├── auth.py        # 认证路由
│   │   ├── projects.py    # 项目路由
│   │   ├── cloud_assets.py # 云资产路由
│   │   ├── sows.py        # SOW路由
│   │   ├── slas.py        # SLA路由
│   │   └── knowledge.py   # 知识库路由
│   ├── services/          # 业务逻辑
│   │   ├── user_service.py     # 用户服务
│   │   ├── project_service.py  # 项目服务
│   │   ├── cloud_asset_service.py # 云资产服务
│   │   ├── sow_service.py      # SOW服务
│   │   ├── sla_service.py      # SLA服务
│   │   └── knowledge_service.py # 知识库服务
│   ├── utils/             # 工具类
│   │   ├── exceptions.py  # 异常处理
│   │   ├── security.py    # 安全工具
│   │   ├── file_handler.py # 文件处理
│   │   └── excel_export.py # Excel导出
│   ├── static/            # 静态文件
│   │   └── uploads/       # 上传文件目录
│   └── main.py            # 应用入口
├── database/              # 数据库脚本
│   ├── complete_schema.sql # 完整建表语句
│   └── ER_relationship.md # ER关系说明
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
├── run.py               # 启动脚本
├── Dockerfile           # Docker配置
├── docker-compose.yml   # Docker Compose配置
└── README.md            # 本文档
```

## 核心API端点

### 认证模块
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/register` - 用户注册（管理员）
- `GET /api/v1/auth/me` - 获取当前用户信息
- `POST /api/v1/auth/change-password` - 修改密码

### 项目管理
- `GET /api/v1/projects/` - 获取项目列表（分页）
- `GET /api/v1/projects/{id}` - 获取项目详情
- `POST /api/v1/projects/` - 创建项目（管理员）
- `PUT /api/v1/projects/{id}` - 更新项目（管理员）
- `DELETE /api/v1/projects/{id}` - 删除项目（管理员）
- `GET /api/v1/projects/{id}/assets` - 获取项目所有关联资产
- `GET /api/v1/projects/export/excel` - 导出项目数据到Excel

### 云资产管理
- `GET /api/v1/cloud-assets/` - 获取云资产列表
- `POST /api/v1/cloud-assets/` - 创建云资产
- `PUT /api/v1/cloud-assets/{id}` - 更新云资产
- `DELETE /api/v1/cloud-assets/{id}` - 删除云资产
- `GET /api/v1/cloud-assets/export/excel` - 导出云资产数据

### SOW管理
- `GET /api/v1/sows/` - 获取SOW列表
- `POST /api/v1/sows/` - 创建SOW（含文件上传）
- `PUT /api/v1/sows/{id}` - 更新SOW
- `DELETE /api/v1/sows/{id}` - 删除SOW
- `GET /api/v1/sows/{id}/download` - 下载SOW文件
- `GET /api/v1/sows/{id}/preview` - 预览SOW文件

### SLA管理
- `GET /api/v1/slas/` - 获取SLA列表
- `POST /api/v1/slas/` - 创建SLA
- `PUT /api/v1/slas/{id}` - 更新SLA
- `DELETE /api/v1/slas/{id}` - 删除SLA
- `GET /api/v1/slas/stats` - 获取SLA统计信息

### 知识库管理
- `GET /api/v1/knowledge/categories` - 获取知识库分类
- `POST /api/v1/knowledge/categories` - 创建分类
- `GET /api/v1/knowledge/documents` - 获取文档列表
- `POST /api/v1/knowledge/documents` - 创建文档
- `PUT /api/v1/knowledge/documents/{id}` - 更新文档
- `DELETE /api/v1/knowledge/documents/{id}` - 删除文档
- `GET /api/v1/knowledge/search` - 搜索文档

## 权限控制

- **管理员 (admin)**: 所有操作权限
- **普通用户 (user)**: 只读权限，可查看所有数据
- **文件上传**: 支持SOW文档和知识库附件上传
- **文件预览**: 支持图片和PDF在线预览

## 开发指南

### 添加新模块

1. 在 `app/models/` 创建数据模型
2. 在 `app/schemas/` 创建Pydantic模式
3. 在 `app/services/` 创建业务逻辑
4. 在 `app/routers/` 创建API路由
5. 在 `app/main.py` 注册路由

### 数据库迁移

```bash
# 安装alembic
pip install alembic

# 初始化迁移环境
alembic init migrations

# 创建迁移脚本
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head
```

### 测试

```bash
# 安装测试依赖
pip install pytest httpx

# 运行测试
pytest
```

## 部署建议

### 生产环境配置

1. **修改SECRET_KEY**: 使用强密码生成器生成
2. **禁用DEBUG模式**: 设置 `DEBUG=False`
3. **配置数据库连接池**: 调整连接参数
4. **启用HTTPS**: 配置SSL证书
5. **设置文件存储**: 使用云存储服务（如S3、OSS）
6. **配置监控告警**: 监控服务健康状态

### 性能优化

1. **数据库索引**: 为常用查询字段添加索引
2. **查询优化**: 使用selective loading避免N+1查询
3. **缓存策略**: 使用Redis缓存热点数据
4. **CDN加速**: 静态文件使用CDN分发
5. **负载均衡**: 多实例部署

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否运行
   - 验证连接字符串配置
   - 检查防火墙设置

2. **文件上传失败**
   - 检查上传目录权限
   - 验证文件大小限制
   - 确认文件类型是否允许

3. **JWT认证失败**
   - 检查SECRET_KEY配置
   - 验证令牌是否过期
   - 确认用户状态是否激活

### 日志查看

```bash
# 查看应用日志
docker-compose logs backend

# 查看数据库日志
docker-compose logs mysql

# 实时查看日志
docker-compose logs -f backend
```

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件至: admin@company.com