#!/usr/bin/env python3
"""
OrcaAgent 开发服务器
提供热加载功能的简单HTTP服务器
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器，添加CORS支持和缓存控制"""
    
    def end_headers(self):
        # 添加CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        
        # 禁用缓存以支持热加载
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        
        super().end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server(port=8000, auto_open=True):
    """启动开发服务器"""
    
    # 确保在正确的目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 检查index.html是否存在
    if not Path('index.html').exists():
        print("❌ 错误: 找不到 index.html 文件")
        print("请确保在正确的项目目录中运行此脚本")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print("🚀 OrcaAgent 开发服务器启动成功!")
            print(f"📱 本地访问: {server_url}")
            print(f"🌐 网络访问: http://{get_local_ip()}:{port}")
            print("📝 文件监控: 手动刷新浏览器查看更改")
            print("⏹️  按 Ctrl+C 停止服务器")
            print("-" * 50)
            
            # 自动打开浏览器
            if auto_open:
                print("🌍 正在打开浏览器...")
                webbrowser.open(server_url)
            
            # 启动服务器
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 端口 {port} 已被占用，尝试使用端口 {port + 1}")
            start_server(port + 1, auto_open)
        else:
            print(f"❌ 启动服务器时出错: {e}")

def get_local_ip():
    """获取本地IP地址"""
    import socket
    try:
        # 连接到一个远程地址来获取本地IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "localhost"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OrcaAgent 开发服务器")
    parser.add_argument("-p", "--port", type=int, default=8000, help="服务器端口 (默认: 8000)")
    parser.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    
    args = parser.parse_args()
    
    start_server(args.port, not args.no_open)