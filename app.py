from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import subprocess
import uuid
import json
import os
import datetime
import requests
import re
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = "YOUR_CLAUDE_KEY"

# 内容安全增强检测
def has_dangerous_patterns(text):
    patterns = [
        r'os\.system', r'__import__', r'subprocess', r'eval\(', r'exec\(',
        r'(rm|del)\s', r'curl\s', r'wget\s'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

@app.route("/execute", methods=["POST"])
def execute_code():
    user_code = request.json.get("code", "")
    if has_dangerous_patterns(user_code):
        return jsonify({"error": "Potentially dangerous code detected"}), 400

    trace_id = str(uuid.uuid4())
    trace_path = f"./traces/{trace_id}.json"
    os.makedirs("./traces", exist_ok=True)
    start_time = datetime.datetime.utcnow().isoformat()

    try:
        process = subprocess.run(
            [
                "docker", "run", "--rm", "--network", "none",
                "--security-opt", "no-new-privileges", "-i", "kimi-sandbox"
            ],
            input=user_code.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )
        stdout, stderr = process.stdout.decode(), process.stderr.decode()

        if has_dangerous_patterns(stdout):
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
    traces = [f.replace(".json", "") for f in os.listdir("./traces") if f.endswith(".json")]
    return jsonify({"traces": traces})

@app.route("/trace/<trace_id>", methods=["GET"])
def get_trace(trace_id):
    path = f"./traces/{trace_id}.json"
    if not os.path.exists(path):
        return jsonify({"error": "Trace not found"}), 404
    with open(path) as f:
        return jsonify(json.load(f))

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

    result = response.json()
    trace_id = str(uuid.uuid4())
    trace_data = {
        "trace_id": trace_id,
        "start_time": datetime.datetime.utcnow().isoformat(),
        "prompt": prompt,
        "claude_response": result
    }
    os.makedirs("./traces", exist_ok=True)
    with open(f"./traces/{trace_id}.json", "w") as f:
        json.dump(trace_data, f, indent=2)

    return jsonify(trace_data)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"status": "ok", "filename": file.filename})

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/schedule", methods=["POST"])
def schedule_task():
    user_code = request.json.get("code", "")
    nodes = ["node1.example.com", "node2.example.com"]
    selected_node = random.choice(nodes)
    response = requests.post(f"http://{selected_node}:5000/execute", json={"code": user_code})
    return jsonify(response.json()), response.status_code

@socketio.on("execute_code")
def handle_execute_code(data):
    user_code = data["code"]
    try:
        process = subprocess.run(
            [
                "docker", "run", "--rm", "--network", "none",
                "--security-opt", "no-new-privileges", "-i", "kimi-sandbox"
            ],
            input=user_code.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15
        )
        stdout, stderr = process.stdout.decode(), process.stderr.decode()
        emit("execution_result", {"stdout": stdout, "stderr": stderr})
    except subprocess.TimeoutExpired:
        emit("execution_result", {"error": "Code execution timed out"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
