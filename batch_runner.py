import requests
import uuid

prompts = [
    "print('Hello from Prompt 1')",
    "print('Hello from Prompt 2')",
    "print('Hello from Prompt 3')",
]

for idx, code in enumerate(prompts):
    trace_id = str(uuid.uuid4())
    print(f"🚀 Running prompt {idx+1} with trace_id={trace_id}...")
    response = requests.post(
        "http://localhost:5000/execute",
        json={"code": code, "trace_id": trace_id}
    )
    print(response.json())
