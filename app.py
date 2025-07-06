from flask import Flask, request, jsonify
import subprocess
import uuid
from trace_store import save_trace

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute():
    user_code = request.json.get("code", "")
    lang = request.json.get("lang", "py")
    trace_id = request.json.get("trace_id", str(uuid.uuid4()))

    # 记录输入
    save_trace(trace_id, "start", {"code": user_code, "lang": lang}, None)

    try:
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-e", f"USER_CODE={user_code}",
                "-e", f"LANG={lang}",
                "kimi-sandbox"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        # 记录输出
        save_trace(trace_id, "execution", {"code": user_code}, {"stdout": result.stdout, "stderr": result.stderr})
        return jsonify({
            "trace_id": trace_id,
            "stdout": result.stdout,
            "stderr": result.stderr,
        })

    except subprocess.TimeoutExpired as e:
        save_trace(trace_id, "execution", {"code": user_code}, None, status="error", error="timeout")
        return jsonify({"trace_id": trace_id, "error": "execution timeout"}), 500
    except Exception as e:
        save_trace(trace_id, "execution", {"code": user_code}, None, status="error", error=str(e))
        return jsonify({"trace_id": trace_id, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
