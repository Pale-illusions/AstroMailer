# 基础镜像，选择 Python 版本
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将项目的 requirements.txt 文件复制到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有文件到容器中
COPY . .

# 设置容器环境变量（可以根据需要设置）
ENV TZ=Asia/Shanghai

# 设置容器启动时运行的命令
CMD ["python", "src/main.py"]