# 企业项目管理平台 - 部署指南

## 快速部署

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd project-management-platform

# 进入后端目录
cd backend
```

### 2. 数据库初始化

```bash
# 创建数据库（需要MySQL客户端）
mysql -u root -p < ../database/complete_schema.sql

# 或手动创建数据库
# 1. 登录MySQL: mysql -u root -p
# 2. 执行: source ../database/complete_schema.sql
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置以下信息：
# DATABASE_URL=mysql+pymysql://pmp_user:Pmp@123456@localhost:3306/project_management_platform
# SECRET_KEY=your-secret-key-change-in-production
```

### 4. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
# 给脚本添加执行权限
chmod +x start.sh

# 启动服务
./start.sh
```

#### 方式二：手动启动

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 创建上传目录
mkdir -p app/static/uploads/sows
mkdir -p app/static/uploads/docs

# 启动服务
python run.py
```

### 5. 验证部署

服务启动后，访问以下地址：
- 健康检查: http://localhost:8000/health
- API文档: http://localhost:8000/docs
- 前端界面: http://localhost:8080 (前端部署后)

## Docker部署

### 1. 使用Docker Compose（推荐）

```bash
# 启动所有服务（数据库 + 后端）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

### 2. 单独部署后端

```bash
# 构建镜像
docker build -t pmp-backend .

# 运行容器
docker run -d \
  --name pmp-backend \
  -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://pmp_user:Pmp@123456@host.docker.internal:3306/project_management_platform \
  -e SECRET_KEY=your-secret-key-change-in-production \
  -v ./app/static/uploads:/app/app/static/uploads \
  pmp-backend
```

## 生产环境部署

### 1. 安全配置

```bash
# 生成强密码作为SECRET_KEY
openssl rand -hex 32

# 修改 .env 文件
SECRET_KEY=生成的强密码
DEBUG=False
```

### 2. 数据库优化

```sql
-- 为常用查询字段添加索引
ALTER TABLE projects ADD INDEX idx_project_status (status);
ALTER TABLE cloud_assets ADD INDEX idx_asset_lifecycle (lifecycle);
ALTER TABLE sows ADD INDEX idx_sow_status (status);

-- 优化查询缓存
SET GLOBAL query_cache_size = 67108864;
SET GLOBAL query_cache_type = 1;
```

### 3. Nginx配置

创建 `nginx.conf` 文件：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 静态文件
    location /static/ {
        alias /app/app/static/;
        expires 30d;
    }
    
    # API代理
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 启用gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### 4. 系统服务（Systemd）

创建 `/etc/systemd/system/pmp-backend.service`：

```ini
[Unit]
Description=Project Management Platform Backend
After=network.target mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/pmp/backend
Environment="PATH=/opt/pmp/backend/venv/bin"
ExecStart=/opt/pmp/backend/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable pmp-backend
sudo systemctl start pmp-backend
sudo systemctl status pmp-backend
```

## 监控和维护

### 1. 日志查看

```bash
# 查看应用日志
tail -f /var/log/pmp-backend.log

# Docker容器日志
docker-compose logs -f backend

# Systemd服务日志
journalctl -u pmp-backend -f
```

### 2. 健康检查

```bash
# API健康检查
curl http://localhost:8000/health

# 数据库连接检查
mysql -u pmp_user -pPmp@123456 -e "SELECT 1" project_management_platform

# 磁盘空间检查
df -h /opt/pmp/backend/app/static/uploads
```

### 3. 备份和恢复

#### 数据库备份
```bash
# 备份数据库
mysqldump -u pmp_user -pPmp@123456 project_management_platform > backup_$(date +%Y%m%d).sql

# 恢复数据库
mysql -u pmp_user -pPmp@123456 project_management_platform < backup.sql
```

#### 文件备份
```bash
# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz app/static/uploads/

# 恢复上传文件
tar -xzf uploads_backup.tar.gz -C app/static/
```

## 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 检查MySQL服务状态
systemctl status mysql

# 检查连接信息
echo $DATABASE_URL

# 测试连接
mysql -u pmp_user -pPmp@123456 -h localhost -e "SELECT 1"
```

#### 2. 文件上传失败
```bash
# 检查目录权限
ls -la app/static/uploads/

# 设置正确权限
chown -R www-data:www-data app/static/uploads/
chmod -R 755 app/static/uploads/
```

#### 3. 服务启动失败
```bash
# 查看错误日志
journalctl -u pmp-backend --no-pager -n 50

# 检查端口占用
netstat -tlnp | grep :8000

# 检查依赖
pip list | grep -E "fastapi|sqlalchemy|pymysql"
```

### 性能优化

#### 1. 数据库优化
```sql
-- 分析慢查询
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Slow_queries';

-- 优化表
OPTIMIZE TABLE projects;
OPTIMIZE TABLE cloud_assets;
```

#### 2. 应用优化
```python
# 调整连接池大小
DATABASE_URL=mysql+pymysql://user:pass@host/db?pool_size=20&max_overflow=30

# 启用查询缓存
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
```

## 升级指南

### 1. 备份数据
```bash
# 备份数据库
mysqldump -u pmp_user -pPmp@123456 project_management_platform > upgrade_backup.sql

# 备份配置文件
cp .env .env.backup
cp docker-compose.yml docker-compose.yml.backup
```

### 2. 更新代码
```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade
```

### 3. 数据库迁移
```bash
# 如果有数据库迁移脚本
alembic upgrade head

# 或手动执行SQL
mysql -u pmp_user -pPmp@123456 project_management_platform < migrations/upgrade.sql
```

### 4. 重启服务
```bash
# Docker Compose
docker-compose down
docker-compose up -d --build

# Systemd
sudo systemctl restart pmp-backend
```

## 安全建议

### 1. 网络安全
- 使用HTTPS（Let's Encrypt免费证书）
- 配置防火墙规则
- 限制API访问IP
- 启用API速率限制

### 2. 数据安全
- 定期备份数据库
- 加密敏感数据
- 实施访问日志
- 监控异常访问

### 3. 应用安全
- 定期更新依赖包
- 扫描安全漏洞
- 实施输入验证
- 防止SQL注入

## 支持与联系

如有问题，请参考：
1. 查看日志文件
2. 检查文档
3. 提交Issue
4. 联系技术支持

邮箱: support@company.com
文档: https://docs.company.com/pmp