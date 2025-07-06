import requests

CLAUDE_API_URL = "http://localhost:5000/claude"  # 调用你自己封装的Claude接口

prompts = [
    "Write a Python function to reverse a string.",
    "Create a simple Node.js server example.",
    "Explain what a Python generator is."
]

for prompt in prompts:
    resp = requests.post(CLAUDE_API_URL, json={"prompt": prompt})
    print(f"Prompt: {prompt}")
    print(f"Response: {resp.json()}")
