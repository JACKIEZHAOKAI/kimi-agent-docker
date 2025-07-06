import subprocess
import random
import logging
import os
import socket
from colorama import init, Fore

# 初始化彩色输出
init(autoreset=True)

def is_github_accessible():
    """检查是否能直连 GitHub"""
    try:
        socket.create_connection(("github.com", 443), timeout=3)
        print(Fore.GREEN + "✅ GitHub is accessible without proxy.")
        return True
    except OSError:
        print(Fore.YELLOW + "⚠️ GitHub not accessible. Trying with proxy...")
        return False

def enable_proxy():
    """为当前进程设置 socks5 代理环境变量"""
    os.environ['https_proxy'] = 'socks5h://127.0.0.1:8119'
    os.environ['http_proxy'] = 'socks5h://127.0.0.1:8119'
    print(Fore.CYAN + "🌐 Proxy environment variables have been set.")

def run_command(command):
    """执行 shell 命令并打印输出"""
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        print(Fore.GREEN + output)
        return output
    except subprocess.CalledProcessError as e:
        print(Fore.RED + e.output)
        return e.output

def git_commit_push():
    """执行 git add、commit、push"""
    if not is_github_accessible():
        enable_proxy()

    # 查看状态
    run_command('git status')

    # 添加所有更改
    run_command('git add -A')

    # 使用随机 commit message
    commit_message = f'"Update Kimi Agent {random.randint(1000, 9999)}"'
    run_command(f'git commit -m {commit_message}')

    # 推送到 origin main
    run_command('git push origin main')

if __name__ == "__main__":
    git_commit_push()
