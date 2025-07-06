FROM python:3.10-slim

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
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
