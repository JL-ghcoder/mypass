# MyPass - 加密密码管理系统

一个终端界面的加密密码管理系统，用于安全地存储和获取敏感信息，如数据库密码、API密钥等。该系统使用AES-256-CBC加密算法，通过客户端-服务器架构提供安全的密码解密服务。

我的用法：
1. 运行encryption_service.py，设置一个解密密钥，将密码进行加密
2. 在一台服务器运行server.py，用于提供远程解密服务，并且输入正确的解密密钥进行解密
3. 在交易服务器上通过 mypass.getpass 来访问远端服务将加密的密码解密
4. 关闭 server.py

这样做可以确保全程不出现密码的明文，并且即使哪一台被黑也不会泄露出密码。

关闭解密服务后黑客只可能通过内存探针获取密码，但这基本上是不可能实现的。

即使两台服务器都被黑客同时黑掉，黑客也无法获取明文密码，并且只要解密密钥没有泄露，解密服务也无法完成解密工作。
 
## 安装

### 依赖项

```bash
pip install flask requests cryptography
```

## 使用方法

### 1. 加密数据

首先使用加密服务加密您的敏感数据：

```bash
python encryption_service.py
```

按照界面提示输入您的数据和加密密钥，加密结果将保存到`encrypted_key.json`文件。

### 2. 启动解密服务器

在需要提供解密服务的机器上运行：

```bash
python server.py
```

输入端口号和解密密钥（必须与加密时使用的密钥相同）。

### 3. 使用客户端解密

要手动解密数据，可以运行客户端：

```bash
python client.py
```

根据提示输入服务器URL和加密数据。

### 4. 在应用程序中使用

```python
from mypass.getpass import get_password

password1 = get_password(
    server_url="http://localhost:6666/decrypt", 
    key_file="encrypted_key.json"
)

password2 = get_password(
    server_url="http://localhost:6666/decrypt",
    encrypted_data="6BxemLxyiBXFwfMEetiXiQ==", 
    iv="6WhgnvA+zrAEiySRSpSH6w=="
)

password3 = get_password(
    encrypted_data="6BxemLxyiBXFwfMEetiXiQ==", 
    iv="6WhgnvA+zrAEiySRSpSH6w==",
    local_key="helloworld"
)

print("password1: ", password1)
print("password2: ", password2)
print("password3: ", password3)
```