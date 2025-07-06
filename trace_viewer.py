from flask import Flask, request, jsonify, render_template_string
import subprocess
import uuid
import os
import json
from trace_store import save_trace, TRACE_DIR

app = Flask(__name__)

# 现有 /execute 接口省略...

@app.route("/traces")
def list_traces():
    files = [f for f in os.listdir(TRACE_DIR) if f.endswith(".json")]
    files.sort(reverse=True)
    html = "<h1>Trace List</h1><ul>"
    for f in files:
        html += f'<li><a href="/trace/{f.replace(".json", "")}">{f}</a></li>'
    html += "</ul>"
    return html

@app.route("/trace/<trace_id>")
def view_trace(trace_id):
    trace_file = os.path.join(TRACE_DIR, f"{trace_id}.json")
    if not os.path.exists(trace_file):
        return f"Trace {trace_id} not found.", 404

    with open(trace_file, "r") as f:
        data = json.load(f)

    html = f"<h1>Trace Detail: {trace_id}</h1>"
    html += '<a href="/traces">Back to List</a><br><br>'
    for step in data:
        html += f"<h3>Step: {step['step']}</h3>"
        html += f"<b>Timestamp:</b> {step['timestamp']}<br>"
        html += f"<b>Status:</b> {step['status']}<br>"
        if step["error"]:
            html += f"<b>Error:</b> <pre>{step['error']}</pre>"
        html += f"<b>Input:</b> <pre>{json.dumps(step['input'], indent=2)}</pre>"
        if step["output"]:
            html += f"<b>Output:</b> <pre>{json.dumps(step['output'], indent=2)}</pre>"
        html += "<hr>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
