FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# 手动写入阿里云 Debian 源并安装依赖
RUN echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
        build-essential \
        nodejs \
        npm \
    && ln -s /usr/bin/nodejs /usr/bin/node \
    && pip install --no-cache-dir matplotlib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY sandbox_runner.py /sandbox_runner.py

ENTRYPOINT ["python", "/sandbox_runner.py"]
