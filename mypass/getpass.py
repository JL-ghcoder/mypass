import os
import json
import requests
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

DEFAULT_SERVER_URL = "http://localhost:6666/decrypt"
DEFAULT_KEY_FILE = os.path.join(os.path.dirname(__file__), 'encrypted_key.json')

def load_encrypted_key(filepath=None):
    """
    从文件加载加密后的密钥
    
    Args:
        filepath (str, optional): 加密密钥文件路径
        
    Returns:
        dict: 包含encrypted_data和iv的字典，如果加载失败则返回None
    """
    try:

        if filepath is None:
            filepath = DEFAULT_KEY_FILE
            
        if not os.path.exists(filepath):
            print(f"错误: 加密密钥文件不存在: {filepath}")
            return None
            
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"错误: 无法加载加密密钥文件: {str(e)}")
        return None

def decrypt_locally(encrypted_data_b64, key, iv_b64):
    """
    在本地使用提供的密钥解密数据
    
    Args:
        encrypted_data_b64 (str): Base64编码的加密数据
        key (str): 解密密钥
        iv_b64 (str): Base64编码的初始化向量
        
    Returns:
        str: 解密后的原始数据，如果解密失败则返回None
    """
    try:

        key_hash = hashlib.sha256(key.encode()).digest()
        
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
    except Exception as e:
        print(f"错误: 本地解密失败: {str(e)}")
        return None

def request_remote_decryption(server_url, encrypted_data, iv):
    """
    向远程服务器请求解密
    
    Args:
        server_url (str): 服务器URL
        encrypted_data (str): 加密后的数据
        iv (str): 初始化向量
        
    Returns:
        str: 解密后的密钥，如果解密失败则返回None
    """
    try:

        data = {
            "encrypted_data": encrypted_data,
            "iv": iv
        }
        
        response = requests.post(server_url, json=data, timeout=10)
        
        if response.status_code == 200:
            return response.json().get("decrypted_key")
        else:
            error_msg = response.json().get("error", f"服务器返回错误代码: {response.status_code}")
            print(f"错误: {error_msg}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"错误: 请求失败 - {str(e)}")
        return None
    except Exception as e:
        print(f"错误: {str(e)}")
        return None

def get_password(server_url=None, encrypted_data=None, iv=None, key_file=None, local_key=None):
    """
    获取解密后的密码
    
    可以通过以下几种方式使用:
    1. 提供server_url、encrypted_data和iv直接请求解密
    2. 提供key_file从文件加载加密数据并请求解密
    3. 提供local_key、encrypted_data和iv在本地解密
    
    Args:
        server_url (str, optional): 解密服务器URL
        encrypted_data (str, optional): 加密后的数据
        iv (str, optional): 初始化向量
        key_file (str, optional): 加密密钥文件路径
        local_key (str, optional): 本地解密密钥
        
    Returns:
        str: 解密后的密码，如果解密失败则返回None
    """

    if server_url is None:
        server_url = DEFAULT_SERVER_URL
    
    if encrypted_data is None or iv is None:
        encrypted_key = load_encrypted_key(key_file)
        if encrypted_key is None:
            return None
        
        encrypted_data = encrypted_key.get("encrypted_data")
        iv = encrypted_key.get("iv")
    
    if encrypted_data is None or iv is None:
        print("错误: 缺少必要的加密数据或初始化向量")
        return None
    
    if local_key is not None:
        password = decrypt_locally(encrypted_data, local_key, iv)
        if password is not None:
            return password
        # 如果本地解密失败，尝试远程解密
    
    # 请求远程解密
    return request_remote_decryption(server_url, encrypted_data, iv)


    # 方法1: 使用默认配置从文件加载
    # password = get_password()
    # if password:
    #     print(f"解密后的密码: {password}")
    
    # 方法2: 指定文件路径
    # password = get_password(key_file="/path/to/my/encrypted_key.json")
    
    # 方法3: 指定加密数据和初始化向量
    # password = get_password(
    #     encrypted_data="WFsEHALbpAq1w3emXUBICw==",
    #     iv="NxBiKQPUN+Bm+iA/8mj0Zg=="
    # )
    
    # 方法4: 使用本地密钥解密
    # password = get_password(
    #     encrypted_data="WFsEHALbpAq1w3emXUBICw==",
    #     iv="NxBiKQPUN+Bm+iA/8mj0Zg==",
    #     local_key="happy"
    # )