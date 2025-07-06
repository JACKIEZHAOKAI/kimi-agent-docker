import json
import os
from datetime import datetime

TRACE_DIR = "./traces"

def save_trace(trace_id, step, input_data, output_data, status="success", error=None):
    os.makedirs(TRACE_DIR, exist_ok=True)
    trace_file = os.path.join(TRACE_DIR, f"{trace_id}.json")
    trace_data = []
    if os.path.exists(trace_file):
        with open(trace_file, "r") as f:
            trace_data = json.load(f)
    trace_data.append({
        "timestamp": datetime.utcnow().isoformat(),
        "step": step,
        "input": input_data,
        "output": output_data,
        "status": status,
        "error": error
    })
    with open(trace_file, "w") as f:
        json.dump(trace_data, f, indent=2)
