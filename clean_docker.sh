#!/bin/bash
echo "🚀 清理所有已停止容器..."
docker container prune -f

echo "🧹 清理所有悬空镜像..."
docker image prune -f

echo "✅ Docker 清理完成！当前镜像列表："
docker images

