import os
import sys
import json
import logging
import threading
import time
from flask import Flask, request, jsonify
from encryption_service import decrypt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """                                                                                                                        
    )    (               )                   (   (     )      (   (    
   (     )\ )  `  )   ( /(  (   (  ___ (    ))\  )(   /((    ))\  )(   
   )\  '(()/(  /(/(   )(_)) )\  )\|___|)\  /((_)(()\ (_))\  /((_)(()\  
 _((_))  )(_))((_)_\ ((_)_ ((_)((_)   ((_)(_))   ((_)_)((_)(_))   ((_) 
| '  \()| || || '_ \)/ _` |(_-<(_-<   (_-</ -_) | '_|\ V / / -_) | '_| 
|_|_|_|  \_, || .__/ \__,_|/__//__/   /__/\___| |_|   \_/  \___| |_|   
         |__/ |_|                                                      

    """
    print(banner)

def create_server(encryption_key):
    """创建Flask服务器实例"""
    server = Flask(__name__)
    server.encryption_key = encryption_key
    
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    @server.route('/decrypt', methods=['POST'])
    def decrypt_key():
        """处理解密请求"""
        try:
            # 从请求中获取加密的数据和IV
            data = request.json
            logger.info(f"收到解密请求")
            
            if not data or 'encrypted_data' not in data or 'iv' not in data:
                logger.error("请求缺少必要参数")
                return jsonify({"error": "缺少必要的参数"}), 400
            
            encrypted_data = data.get('encrypted_data')
            iv = data.get('iv')
            
            # 使用服务器的主密钥解密数据
            decrypted_key = decrypt(encrypted_data, server.encryption_key, iv)
            logger.info(f"解密成功，密码长度: {len(decrypted_key)} 字符")
            
            print(f"\n    [新请求] 解密成功，密码长度: {len(decrypted_key)} 字符")
            
            # 返回解密后的密钥
            return jsonify({"decrypted_key": decrypted_key})
        
        except Exception as e:
            logger.error(f"解密出错: {str(e)}")
            print(f"\n    [错误] 解密失败: {str(e)}")
            return jsonify({"error": "解密失败"}), 500
    
    return server

def run_server_thread(port, encryption_key, stop_event):
    """在线程中运行服务器"""
    server = create_server(encryption_key)
    
    from werkzeug.serving import make_server
    
    # 创建服务器
    srv = make_server('0.0.0.0', port, server)
    srv.daemon_threads = True
    
    # 设置服务器的轮询间隔
    srv.service_timeout = 1
    
    clear_screen()
    print_banner()
    print(f"\n    服务器已启动，监听端口: {port}")
    print(f"    解密密钥: {encryption_key}")
    print("\n    [状态] 等待连接...")
    print("\n    按Ctrl+C停止服务器")
    
    # 运行服务器直到被停止
    try:
        while not stop_event.is_set():
            srv.handle_request()
    except KeyboardInterrupt:
        pass

def main():
    """主函数"""
    clear_screen()
    print_banner()
    
    # 获取端口
    while True:
        try:
            port_str = input("\n    请输入服务器端口 (1024-65535): ")
            port = int(port_str)
            if 1024 <= port <= 65535:
                break
            print("    [错误] 端口必须在1024-65535之间")
        except ValueError:
            print("    [错误] 请输入有效的端口号")
    
    # 获取解密密钥
    while True:
        encryption_key = input("\n    请输入解密密钥: ")
        if encryption_key:
            break
        print("    [错误] 密钥不能为空")
    
    # 创建停止事件
    stop_event = threading.Event()
    
    try:
        # 运行服务器
        run_server_thread(port, encryption_key, stop_event)
    except KeyboardInterrupt:
        
        stop_event.set()
        print("\n\n    正在停止服务器...")
        time.sleep(1)
        print("    服务器已停止")
    
    print("\n    感谢使用解密服务器!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n    操作已取消")
        print("    感谢使用解密服务器!")