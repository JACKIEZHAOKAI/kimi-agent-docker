from flask import Flask, jsonify, render_template_string
import os
import json

app = Flask(__name__)

@app.route("/traces")
def list_traces():
    traces = []
    for file in os.listdir("./traces"):
        if file.endswith(".json"):
            traces.append(file.replace(".json", ""))
    html = "<h1>Trace List</h1><ul>"
    for t in traces:
        html += f"<li><a href='/trace/{t}'>{t}</a></li>"
    html += "</ul>"
    return html

@app.route("/trace/<trace_id>")
def get_trace(trace_id):
    path = f"./traces/{trace_id}.json"
    if not os.path.exists(path):
        return "Trace not found", 404
    with open(path) as f:
        trace = json.load(f)
    return render_template_string(
        "<h1>Trace {{trace_id}}</h1><pre>{{trace}}</pre>",
        trace_id=trace_id, trace=json.dumps(trace, indent=2)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
