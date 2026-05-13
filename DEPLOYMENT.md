# 企业项目管理平台 - 部署文档

## 目录
- [本地开发部署](#本地开发部署)
- [服务器生产部署](#服务器生产部署)
- [环境变量配置](#环境变量配置)
- [常见问题](#常见问题)

---

## 本地开发部署

### 前置要求
- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- pip (Python包管理器)
- npm (Node.js包管理器)

### 1. 克隆项目

```bash
cd /Users/time/Documents/Kiro/project-management-platform
```

### 2. 数据库配置

#### 2.1 启动 MySQL

```bash
# 使用 Docker 启动 MySQL（推荐）
docker run -d \
  --name pmp-mysql \
  -e MYSQL_ROOT_PASSWORD=root123456 \
  -e MYSQL_DATABASE=project_management_platform \
  -e MYSQL_USER=pmp_user \
  -e MYSQL_PASSWORD=Pmp@123456 \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  -v $(pwd)/database/complete_schema.sql:/docker-entrypoint-initdb.d/init.sql \
  --restart always \
  mysql:8.0 \
  --default-authentication-plugin=mysql_native_password
```

#### 2.2 验证数据库连接

```bash
mysql -h localhost -u pmp_user -pPmp@123456 project_management_platform
```

### 3. 后端部署

#### 3.1 创建虚拟环境

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate
```

#### 3.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 3.3 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件
vim .env
```

**推荐的本地开发配置：**

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://pmp_user:Pmp@123456@localhost:3306/project_management_platform

# JWT配置
SECRET_KEY=your-local-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
DEBUG=True
ALLOWED_HOSTS=["*"]
UPLOAD_DIR=./app/static/uploads
MAX_UPLOAD_SIZE=10485760

# 管理员初始账号
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_EMAIL=admin@company.com
```

#### 3.4 初始化管理员账号

```bash
# 启动后端服务
python run.py
```

首次启动时，系统会自动创建管理员账号（如果不存在）。

#### 3.5 访问 API 文档

```
http://localhost:8000/docs
```

### 4. 前端部署

#### 4.1 安装依赖

```bash
cd ../frontend

# 安装依赖
npm install
```

#### 4.2 配置环境变量

前端环境变量已配置在 `.env` 文件中：

```env
VITE_APP_TITLE=企业项目管理平台
VITE_API_BASE_URL=/api
```

#### 4.3 启动开发服务器

```bash
npm run dev
```

访问 `http://localhost:5173`（或终端显示的端口）。

---

## 服务器生产部署

### 方案一：Docker Compose 部署（推荐）

#### 1. 准备服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo apt install docker-compose -y

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2. 配置环境变量

```bash
cd backend

# 创建生产环境配置文件
cp .env.example .env
vim .env
```

**生产环境配置示例：**

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://pmp_user:StrongPassword123@localhost:3306/project_management_platform

# JWT配置
SECRET_KEY=your-super-secret-key-with-at-least-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 应用配置
DEBUG=False
ALLOWED_HOSTS=["your-domain.com","www.your-domain.com"]
UPLOAD_DIR=./app/static/uploads
MAX_UPLOAD_SIZE=10485760

# 管理员账号
ADMIN_USERNAME=admin
ADMIN_PASSWORD=StrongAdminPassword123
ADMIN_EMAIL=admin@company.com
```

#### 3. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 4. 访问应用

```
http://your-server-ip
```

### 方案二：手动部署（无 Docker）

#### 1. 安装依赖

```bash
# 安装 MySQL
sudo apt install mysql-server -y

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 安装 Python 依赖
sudo apt install python3-pip python3-venv python3-dev libmysqlclient-dev -y
```

#### 2. 配置 MySQL

```bash
# 启动 MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# 运行安全配置
sudo mysql_secure_installation

# 创建数据库和用户
sudo mysql <<EOF
CREATE DATABASE project_management_platform;
CREATE USER 'pmp_user'@'localhost' IDENTIFIED BY 'Pmp@123456';
GRANT ALL PRIVILEGES ON project_management_platform.* TO 'pmp_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# 导入数据库结构
mysql -u pmp_user -pPmp@123456 project_management_platform < database/complete_schema.sql
```

#### 3. 部署后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件（参考上面的生产配置）

# 创建上传目录
mkdir -p app/static/uploads

# 创建 systemd 服务
sudo tee /etc/systemd/system/pmp-backend.service > /dev/null <<EOF
[Unit]
Description=Project Management Platform Backend
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/project-management-platform/backend
Environment="PATH=/path/to/project-management-platform/backend/venv/bin"
Environment="DATABASE_URL=mysql+pymysql://pmp_user:Password@localhost:3306/project_management_platform"
Environment="SECRET_KEY=your-secret-key"
ExecStart=/path/to/project-management-platform/backend/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start pmp-backend
sudo systemctl enable pmp-backend
```

#### 4. 部署前端

```bash
cd ../frontend

# 安装依赖
npm install

# 构建生产版本
npm run build

# 安装并配置 Nginx
sudo apt install nginx -y

# 配置 Nginx
sudo tee /etc/nginx/sites-available/pmp > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    root /path/to/project-management-platform/frontend/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /path/to/project-management-platform/backend/app/static;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/pmp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 环境变量配置

### 后端环境变量 (.env)

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `DATABASE_URL` | 数据库连接字符串 | `mysql+pymysql://pmp_user:Pmp@123456@localhost:3306/project_management_platform` | 是 |
| `SECRET_KEY` | JWT 密钥（至少32字符） | `your-secret-key-change-in-production` | 是 |
| `ALGORITHM` | JWT 算法 | `HS256` | 否 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 过期时间（分钟） | `30` | 否 |
| `DEBUG` | 调试模式 | `True` | 否 |
| `ALLOWED_HOSTS` | 允许的主机列表 | `["*"]` | 否 |
| `UPLOAD_DIR` | 上传文件目录 | `./app/static/uploads` | 否 |
| `MAX_UPLOAD_SIZE` | 最大上传大小（字节） | `10485760` (10MB) | 否 |
| `ADMIN_USERNAME` | 管理员用户名 | `admin` | 否 |
| `ADMIN_PASSWORD` | 管理员密码 | `admin123` | 否 |
| `ADMIN_EMAIL` | 管理员邮箱 | `admin@company.com` | 否 |

### 前端环境变量 (.env)

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `VITE_APP_TITLE` | 应用标题 | `企业项目管理平台` | 否 |
| `VITE_API_BASE_URL` | API 基础路径 | `/api` | 否 |

---

## 常见问题

### 1. 数据库连接失败

**问题：** `Can't connect to MySQL server on 'localhost'`

**解决方案：**
```bash
# 检查 MySQL 服务状态
sudo systemctl status mysql

# 重启 MySQL
sudo systemctl restart mysql

# 检查端口
netstat -tlnp | grep 3306
```

### 2. 端口被占用

**问题：** `Address already in use`

**解决方案：**
```bash
# 查找占用端口的进程
lsof -i :8000
lsof -i :3306

# 杀死进程
kill -9 <PID>
```

### 3. 权限问题

**问题：** 上传文件失败或无法写入

**解决方案：**
```bash
# 确保上传目录存在且有写权限
mkdir -p backend/app/static/uploads
chmod -R 755 backend/app/static/uploads
chown -R www-data:www-data backend/app/static/uploads
```

### 4. Token 过期

**问题：** 登录后操作提示未授权

**解决方案：**
- 增加 `ACCESS_TOKEN_EXPIRE_MINUTES` 值
- 实现 Token 刷新机制

### 5. 静态文件 404

**问题：** 前端构建后静态资源无法加载

**解决方案：**
```bash
# 检查 Nginx 配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 检查文件权限
ls -la frontend/dist/
```

### 6. 数据库初始化失败

**问题：** 表不存在或结构不正确

**解决方案：**
```bash
# 手动导入数据库结构
mysql -u pmp_user -pPmp@123456 project_management_platform < database/complete_schema.sql

# 或在后端启动时自动创建（仅开发环境）
# 确保 DEBUG=True
```

### 7. 防火墙配置

**问题：** 外部无法访问服务

**解决方案：**
```bash
# 开放端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3306/tcp

# 检查防火墙状态
sudo ufw status
```

### 8. 日志查看

**后端日志：**
```bash
# Docker 部署
docker-compose logs -f backend

# 手动部署
tail -f /var/log/pmp-backend.log
```

**前端日志：**
```bash
# 浏览器开发者工具
F12 -> Console
```

---

## 备份与恢复

### 数据库备份

```bash
# 备份
mysqldump -u pmp_user -pPmp@123456 project_management_platform > backup.sql

# 恢复
mysql -u pmp_user -pPmp@123456 project_management_platform < backup.sql
```

### 文件备份

```bash
# 备份上传文件
tar -czf uploads_backup.tar.gz backend/app/static/uploads/

# 恢复
tar -xzf uploads_backup.tar.gz -C backend/
```

---

## 更新与升级

### 拉取最新代码

```bash
cd /path/to/project-management-platform
git pull origin main
```

### 更新依赖

```bash
# 后端
cd backend
pip install -r requirements.txt --upgrade

# 前端
cd ../frontend
npm update
```

### 数据库迁移

```bash
cd backend
alembic upgrade head
```

### 重启服务

```bash
# Docker 部署
docker-compose restart

# 手动部署
sudo systemctl restart pmp-backend
sudo systemctl restart nginx
```

---

## 监控与维护

### 健康检查

```bash
# 后端健康检查
curl http://localhost:8000/health

# 数据库连接
mysqladmin -u pmp_user -pPmp@123456 ping
```

### 性能优化建议

1. **数据库优化**
   - 添加索引
   - 定期清理日志
   - 优化查询

2. **缓存**
   - 使用 Redis 缓存
   - 浏览器缓存静态资源

3. **CDN**
   - 使用 CDN 加速静态资源

4. **负载均衡**
   - 多实例部署
   - 使用 Nginx 负载均衡

---

## 联系支持

如有问题，请检查：
1. 所有服务是否正常运行
2. 环境变量是否正确配置
3. 数据库连接是否正常
4. 防火墙和安全组设置
5. 日志文件中的错误信息