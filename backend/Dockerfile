# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 复制应用代码
COPY . .

# 创建上传目录
RUN mkdir -p app/static/uploads/sows app/static/uploads/docs

# 设置权限
RUN chmod -R 755 app/static/uploads

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "run.py"]