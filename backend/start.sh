#!/bin/bash

# 企业项目管理平台 - 启动脚本

set -e

echo "=========================================="
echo "启动企业项目管理平台后端服务"
echo "=========================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "复制环境变量模板..."
    cp .env.example .env
    echo "请编辑 .env 文件配置数据库连接等信息"
    exit 1
fi

# 检查数据库
echo "检查数据库连接..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
import pymysql
try:
    conn = pymysql.connect(
        host='localhost',
        user=os.getenv('DATABASE_URL').split('://')[1].split(':')[0],
        password=os.getenv('DATABASE_URL').split('://')[1].split(':')[1].split('@')[0],
        database=os.getenv('DATABASE_URL').split('/')[-1]
    )
    print('数据库连接成功')
    conn.close()
except Exception as e:
    print(f'数据库连接失败: {e}')
    exit(1)
"

# 创建上传目录
echo "创建上传目录..."
mkdir -p app/static/uploads/sows
mkdir -p app/static/uploads/docs

# 启动服务
echo "启动服务..."
echo "访问地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "按 Ctrl+C 停止服务"

python run.py