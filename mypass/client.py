import os
import sys
import json
import requests

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """                                                    
                                           (                     )  
    )    (               )                 )\ (     (         ( /(  
   (     )\ )  `  )   ( /(  (   (  ___ (  ((_))\   ))\  (     )\()) 
   )\  '(()/(  /(/(   )(_)) )\  )\|___|)\  _ ((_) /((_) )\ ) (_))/  
 _((_))  )(_))((_)_\ ((_)_ ((_)((_)   ((_)| | (_)(_))  _(_/( | |_   
| '  \()| || || '_ \)/ _` |(_-<(_-<  / _| | | | |/ -_)| ' \))|  _|  
|_|_|_|  \_, || .__/ \__,_|/__//__/  \__| |_| |_|\___||_||_|  \__|  
         |__/ |_|                                                   

    """
    print(banner)

def print_menu():

    menu = """
    请选择操作:
    1. 输入加密数据并解密
    2. 输入JSON格式的加密数据并解密
    3. 退出
    
    选择: """
    return input(menu)

def get_input(prompt):

    return input(prompt)

def request_decryption(server_url, encrypted_data, iv):
    """
    向远程服务器请求解密密钥
    
    Args:
        server_url (str): 服务器URL
        encrypted_data (str): 加密后的数据
        iv (str): 初始化向量
        
    Returns:
        str: 解密后的密钥或错误信息
    """
    try:
        # 准备请求数据
        data = {
            "encrypted_data": encrypted_data,
            "iv": iv
        }
        
        print("\n    正在向服务器发送解密请求...\n")
        
        response = requests.post(server_url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json().get("decrypted_key", "未知响应")
        else:
            error_msg = response.json().get("error", f"服务器返回错误代码: {response.status_code}")
            return f"错误: {error_msg}"
            
    except requests.exceptions.RequestException as e:
        return f"错误: 请求失败 - {str(e)}"
    except Exception as e:
        return f"错误: {str(e)}"

def decrypt_from_input():
    """从用户输入解密数据"""
    clear_screen()
    print_banner()
    print("\n    === 输入加密数据 ===\n")
    
    # 获取服务器URL
    server_url = get_input("    请输入服务器URL (默认: http://localhost:6666/decrypt): ")
    if not server_url:
        server_url = "http://localhost:6666/decrypt"
    
    # 获取加密数据
    encrypted_data = get_input("    请输入加密数据: ")
    if not encrypted_data:
        print("\n    [错误] 加密数据不能为空!")
        input("\n    按回车键继续...")
        return
    
    # 获取IV
    iv = get_input("    请输入初始化向量(IV): ")
    if not iv:
        print("\n    [错误] 初始化向量不能为空!")
        input("\n    按回车键继续...")
        return
    
    result = request_decryption(server_url, encrypted_data, iv)
    
    print("\n    === 解密结果 ===\n")
    
    if result.startswith("错误"):
        print(f"    {result}")
    else:
        print(f"    解密后的密钥: {result}")
    
    input("\n    按回车键继续...")

def decrypt_from_json():
    """从JSON解密数据"""
    clear_screen()
    print_banner()
    print("\n    === 输入JSON格式的加密数据 ===\n")
    
    # 获取服务器URL
    server_url = get_input("    请输入服务器URL (默认: http://localhost:6666/decrypt): ")
    if not server_url:
        server_url = "http://localhost:6666/decrypt"
    
    # 获取JSON数据
    print("\n    请输入JSON数据 (格式: {\"encrypted_data\": \"...\", \"iv\": \"...\"})")
    print("    输入完成后请按回车键两次:\n")
    
    lines = []
    while True:
        line = input("    ")
        if not line and lines and lines[-1] == "":
            break
        lines.append(line)
    
    json_text = "\n".join(lines).strip()
    
    if not json_text:
        print("\n    [错误] JSON数据不能为空!")
        input("\n    按回车键继续...")
        return
    
    try:

        data = json.loads(json_text)
        
        if "encrypted_data" not in data or "iv" not in data:
            print("\n    [错误] JSON必须包含'encrypted_data'和'iv'字段!")
            input("\n    按回车键继续...")
            return
        
        encrypted_data = data["encrypted_data"]
        iv = data["iv"]
        
        # 请求解密
        result = request_decryption(server_url, encrypted_data, iv)
        
        print("\n    === 解密结果 ===\n")
        
        if result.startswith("错误"):
            print(f"    {result}")
        else:
            print(f"    解密后的密钥: {result}")
        
    except json.JSONDecodeError:
        print("\n    [错误] 无效的JSON格式!")
    except Exception as e:
        print(f"\n    [错误] {str(e)}")
    
    input("\n    按回车键继续...")

def main():

    while True:
        clear_screen()
        print_banner()
        choice = print_menu()
        
        if choice == '1':
            decrypt_from_input()
            
        elif choice == '2':
            decrypt_from_json()
            
        elif choice == '3':
            print("\n    感谢使用解密客户端!")
            break
            
        else:
            print("\n    [错误] 无效的选择!")
            input("\n    按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n    操作已取消")
        print("    感谢使用解密客户端!")