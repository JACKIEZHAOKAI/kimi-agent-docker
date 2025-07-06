# Agent Sandbox Environment

一个支持安全执行 Python / NodeJS 代码的 AI Agent 沙箱环境，内置 Trace 记录和可视化页面，支持批量运行 PromptSet 并自动保存每次执行的输入输出。

---

## ✅ 功能概述

- 🐳 **Docker 沙箱**：使用 `kimi-sandbox` 镜像隔离执行 Python/NodeJS 代码，支持 matplotlib imshow base64 输出。
- ⚙️ **Flask API**：提供 `/execute` HTTP 接口，可提交代码并返回 stdout/stderr。
- 🔍 **Trace 记录**：每次执行生成唯一 trace_id，记录输入/输出/异常到本地 JSON 文件。
- 📊 **Trace 可视化**：浏览器访问 `/traces` 查看所有记录，并可进入每条 Trace 查看详细执行步骤。
- 📝 **批量执行**：通过 `batch_runner.py` 一次性执行多条 PromptSet 并追踪结果。
- 🚀 **自动提交**：通过 `submit.py` 自动执行 git add/commit/push。

---

## 📁 项目目录结构

```
.
├── app.py # Flask API 接口
├── batch_runner.py # 批量执行 PromptSet
├── trace_viewer.py # Trace 可视化页面
├── trace_store.py # Trace 存储模块
├── sandbox_runner.py # Docker 内执行脚本
├── submit.py # 自动提交到 GitHub
├── Dockerfile # 构建 kimi-sandbox 镜像
└── traces/ # Trace 记录目录
```

---

## 🚀 使用方法

### 1️⃣ 构建沙箱镜像

在项目根目录执行：
```bash
docker build -t kimi-sandbox .
```

---

### 2️⃣ 启动 Flask API

```bash
python app.py
```

或使用可视化 Trace 页面：
```bash
python trace_viewer.py
```

默认监听 [http://localhost:5000](http://localhost:5000)。

---

### 3️⃣ 单次调用

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"code":"print(\\"hello\\")"}' \
     http://localhost:5000/execute
```

---

### 4️⃣ 批量执行 PromptSet

```bash
python batch_runner.py
```

---

### 5️⃣ 查看 Trace

浏览器访问：
```
http://localhost:5000/traces
```

点击每个 trace_id 查看详细执行过程。

---

## 🌀 自动提交脚本

你的 \`submit.py\` 可在本地自动完成代码提交和推送：
```bash
python submit.py
```

功能：
- 检测 GitHub 是否可达；
- 自动设置代理（127.0.0.1:8119 socks5）；
- 执行 git add、随机 commit message、push。

你可以根据需要修改代理或 git 分支名。

---

## ⚠️ 注意事项

- 每次修改 \`sandbox_runner.py\` 后，都需要重新执行：
  ```bash
  docker build -t kimi-sandbox .
  ```
- 如果只是改动 Flask 端（app.py / trace_store.py 等），不需要重建镜像。

---

## 📦 依赖

- Docker
- Python 3.x
- pip install colorama（仅 submit.py 需要）

---

🔗 项目完整流程见上方说明，欢迎使用与改进！
EOF
# kimi-agent-docker
