from flask import Flask, request, jsonify, send_from_directory
import subprocess
import uuid
import json
import os
import datetime
import requests

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Claude 接口配置（示例）
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = "YOUR_CLAUDE_KEY"

DANGEROUS_INPUT_KEYWORDS = ['os.system', '__import__', 'subprocess', 'eval', 'exec']
DANGEROUS_OUTPUT_KEYWORDS = ['password', 'secret', 'confidential']

@app.route("/execute", methods=["POST"])
def execute_code():
    data = request.json
    user_code = data.get("code", "")

    # 1️⃣ 内容安全：检测危险输入
    if any(keyword in user_code for keyword in DANGEROUS_INPUT_KEYWORDS):
        return jsonify({"error": "Potentially dangerous code detected"}), 400

    trace_id = str(uuid.uuid4())
    trace_path = f"./traces/{trace_id}.json"
    os.makedirs("./traces", exist_ok=True)

    start_time = datetime.datetime.utcnow().isoformat()

    try:
        # 调用 sandbox_runner.py 在 Docker 中执行
        process = subprocess.run(
            ["docker", "run", "--rm", "-i", "kimi-sandbox"],
            input=user_code.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )
        stdout, stderr = process.stdout.decode(), process.stderr.decode()

        # 2️⃣ 内容安全：检测危险输出
        if any(keyword in stdout.lower() for keyword in DANGEROUS_OUTPUT_KEYWORDS):
            return jsonify({"error": "Unsafe output detected"}), 400

        trace_data = {
            "trace_id": trace_id,
            "start_time": start_time,
            "input": user_code,
            "stdout": stdout,
            "stderr": stderr,
            "status": "success" if process.returncode == 0 else "error"
        }

        with open(trace_path, "w") as f:
            json.dump(trace_data, f, indent=2)

        return jsonify(trace_data)

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Code execution timed out"}), 504


@app.route("/traces", methods=["GET"])
def list_traces():
    traces = []
    for file in os.listdir("./traces"):
        if file.endswith(".json"):
            traces.append(file.replace(".json", ""))
    return jsonify({"traces": traces})


@app.route("/trace/<trace_id>", methods=["GET"])
def get_trace(trace_id):
    trace_path = f"./traces/{trace_id}.json"
    if not os.path.exists(trace_path):
        return jsonify({"error": "Trace not found"}), 404

    with open(trace_path) as f:
        trace = json.load(f)
    return jsonify(trace)


@app.route("/claude", methods=["POST"])
def call_claude():
    prompt = request.json.get("prompt", "")
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    payload = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    return jsonify(response.json())


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"status": "ok", "filename": file.filename})


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
