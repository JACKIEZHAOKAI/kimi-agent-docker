import os             # 用于读取环境变量 (支持从 Docker run 传入 USER_CODE / LANG)
import sys
import base64         # 用于把 matplotlib 图片转换成 base64 输出 (题目 1.b.i)
import io
import subprocess     # 用于管理 NodeJS 代码执行进程 (题目 1.a: 进程管理)
import matplotlib.pyplot as plt

# 处理 Python 代码执行
def run_python(user_code):
    local_vars = {}
    try:
        exec(user_code, {}, local_vars)    # 在独立变量环境里执行用户代码 (题目 1.b: Python Interpreter)
        if 'imshow_data' in local_vars:    # 如果用户代码中定义了 imshow_data
            buf = io.BytesIO()
            plt.imshow(local_vars['imshow_data'])   # 显示图片
            plt.savefig(buf, format='png')         # 保存到内存
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')  # 转 base64 (题目 1.b.i)
            print("===BEGIN_IMAGE_BASE64===")
            print(img_base64)
            print("===END_IMAGE_BASE64===")
    except Exception as e:
        print(f"[ERROR]: {e}")

# 处理 NodeJS 代码执行
def run_node(user_code):
    try:
        # 使用 subprocess 启动 NodeJS 进程 (题目 1.c: NodeJS Interpreter)
        process = subprocess.Popen(
            ['node', '-e', user_code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # communicate + 超时处理 (题目 1.a: 避免 stdin 阻塞/无响应)
        out, err = process.communicate(timeout=5)
        print("===BEGIN_STDOUT===")
        print(out.decode())
        print("===END_STDOUT===")
        if err:
            print("===BEGIN_STDERR===")
            print(err.decode())
            print("===END_STDERR===")
    except subprocess.TimeoutExpired:
        process.kill()  # 超时后终止进程 (题目 1.a)
        print("[ERROR]: NodeJS code execution timed out.")
    except Exception as e:
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    print("请在启动 Docker 时通过环境变量 USER_CODE 传入代码")
    code = os.environ.get("USER_CODE", "print('Hello from sandbox!')")
    lang = os.environ.get("LANG", "py").lower()   # 根据 LANG 环境变量决定 Python 还是 NodeJS

    if lang == "js":
        run_node(code)      # 执行 NodeJS Interpreter
    else:
        run_python(code)    # 执行 Python Interpreter
