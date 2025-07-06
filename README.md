# Agent Sandbox Environment

本项目实现了一个支持 Python 和 NodeJS 的沙箱执行平台，提供：
✅ Docker 沙箱环境  
✅ 进程管理、输入输出内容安全检测  
✅ Trace 记录和可视化  
✅ Claude API 调用并 Trace 保存  
✅ 文件上传/下载管理  
✅ 模拟混合云调度接口  
✅ WebSocket 实时代码执行支持  


## 📁 项目目录结构

```
.
├── app.py # Flask API: /execute, /claude, /upload, /download, /schedule, WebSocket
├── batch_runner.py # 批量执行 PromptSet 示例
├── trace_viewer.py # Trace 简易可视化页面
├── trace_store.py # Trace 文件管理
├── sandbox_runner.py # Docker 内执行脚本
├── Dockerfile # 沙箱镜像构建文件
├── traces/ # Trace 存储目录
├── uploads/ # 文件上传目录
```


## ✅ 功能亮点

- **Docker 沙箱执行**：在安全容器中隔离执行 Python/NodeJS 代码。
- **输入输出内容安全检测**：防止执行危险代码及输出敏感内容。
- **Trace 系统**：每次执行会生成唯一 trace_id 并保存输入、输出、状态。
- **Claude API 调用**：支持调用 Claude 3 并把结果 Trace 保存到本地。
- **混合云调度**：通过 `/schedule` 模拟将执行任务分配到多个节点。
- **文件管理**：支持文件上传和下载接口。
- **WebSocket**：通过 Socket.IO 实时代码执行结果回传。


## ✅ 安全容器设计

- 使用 `--network none` 禁用网络；
- 使用 `--security-opt no-new-privileges` 限制容器权限；
- 可在生产中进一步通过 seccomp/AppArmor 等增强隔离。

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
     -d '{"code":"print(\"Hello from Kimi Sandbox\")"}' \
     http://localhost:5000/execute
```

---

### 4️⃣ 批量执行 PromptSet

```bash
python batch_runner.py
```


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

✅ 接口说明
POST /execute：执行 Python/NodeJS 代码

GET /traces：获取所有 Trace 列表

GET /trace/<trace_id>：查看指定 Trace 详情

POST /claude：调用 Claude 接口，自动保存结果 Trace

POST /upload：上传文件

GET /download/<filename>：下载文件

POST /schedule：将执行任务调度到其他节点执行

WebSocket execute_code：通过 WebSocket 实时代码执行


⚠️ 注意
在生产环境中使用时应进一步对 Docker 沙箱进行安全加固。

混合云调度接口 /schedule 为示例演示，真实项目需完善调度中心、心跳检测、负载均衡等。
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
