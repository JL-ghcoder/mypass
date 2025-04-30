import base64
import hashlib
import os
import json
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

DEFAULT_ENCRYPTED_KEY_FILE = os.path.join(os.path.dirname(__file__), 'encrypted_key.json')

def encrypt(data, key):
    """
    使用提供的密钥加密数据
    
    Args:
        data (str): 要加密的数据
        key (str): 加密密钥
        
    Returns:
        dict: 包含加密后的数据和初始化向量
    """
    # 创建一个32位的密钥 (使用SHA-256哈希密钥)
    key_hash = hashlib.sha256(key.encode()).digest()
    
    # 生成随机初始化向量
    iv = os.urandom(16)
    
    # 创建加密器
    cipher = Cipher(
        algorithms.AES(key_hash),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    # 填充数据为16字节的倍数 (AES块大小)
    pad_length = 16 - (len(data.encode()) % 16)
    padded_data = data.encode() + bytes([pad_length]) * pad_length
    
    # 加密数据
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return {
        "encrypted_data": base64.b64encode(encrypted_data).decode('utf-8'),
        "iv": base64.b64encode(iv).decode('utf-8')
    }

def decrypt(encrypted_data_b64, key, iv_b64):
    """
    使用提供的密钥解密数据
    
    Args:
        encrypted_data_b64 (str): Base64编码的加密数据
        key (str): 解密密钥
        iv_b64 (str): Base64编码的初始化向量
        
    Returns:
        str: 解密后的原始数据
    """
    # 创建一个32位的密钥 (使用SHA-256哈希密钥)
    key_hash = hashlib.sha256(key.encode()).digest()
    
    # 将IV和加密数据从Base64解码
    iv = base64.b64decode(iv_b64)
    encrypted_data = base64.b64decode(encrypted_data_b64)
    
    cipher = Cipher(
        algorithms.AES(key_hash),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    pad_length = padded_data[-1]
    data = padded_data[:-pad_length]
    
    return data.decode('utf-8')

def save_encrypted_data(data, filepath=DEFAULT_ENCRYPTED_KEY_FILE):
    """
    保存加密数据到文件
    
    Args:
        data (dict): 包含encrypted_data和iv的字典
        filepath (str): 保存的文件路径
        
    Returns:
        bool: 保存是否成功
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"    [错误] 保存文件失败: {str(e)}")
        return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
 __  __  _  _  ____   __    ___  ___      ____  _____  _____  __   
(  \/  )( \/ )(  _ \ /__\  / __)/ __) ___(_  _)(  _  )(  _  )(  )  
 )    (  \  /  )___//(__)\ \__ \\__ \(___) )(   )(_)(  )(_)(  )(__ 
(_/\/\_) (__) (__) (__)(__)(___/(___/     (__) (_____)(_____)(____)
    """
    print(banner)

def print_menu():

    menu = """
    请选择操作:
    1. 加密数据
    2. 退出
    
    选择: """
    return input(menu)

def get_input(prompt):
    """获取用户输入"""
    return input(prompt)

def main():

    while True:
        clear_screen()
        print_banner()
        choice = print_menu()
        
        if choice == '1':
            clear_screen()
            print_banner()
            print("\n    === 加密数据 ===\n")
            
            # 获取数据和密钥
            data = get_input("    请输入要加密的数据: ")
            if not data:
                print("\n    [错误] 数据不能为空!")
                input("\n    按回车键继续...")
                continue
                
            key = get_input("    请输入加密密钥: ")
            if not key:
                print("\n    [错误] 密钥不能为空!")
                input("\n    按回车键继续...")
                continue
            
            # 执行加密
            try:
                result = encrypt(data, key)
                
                print("\n    === 加密结果 ===\n")
                print(f"    加密数据: {result['encrypted_data']}")
                print(f"    初始化向量(IV): {result['iv']}")
                
                json_result = json.dumps(result, indent=4)
                print("\n    JSON格式:")
                print(f"    {json_result.replace(chr(10), chr(10)+'    ')}")
                
                # 保存到文件
                save_successful = save_encrypted_data(result)
                if save_successful:
                    print(f"\n    加密结果已保存到文件: {DEFAULT_ENCRYPTED_KEY_FILE}")
                
                print("\n    加密成功!")
            except Exception as e:
                print(f"\n    [错误] 加密失败: {str(e)}")
            
            input("\n    按回车键继续...")
            
        elif choice == '2':
            print("\n    感谢使用加密工具!")
            break
            
        else:
            print("\n    [错误] 无效的选择!")
            input("\n    按回车键继续...")

if __name__ == "__main__":
    main()