from mypass.getpass import get_password

password1 = get_password(
    server_url="http://localhost:6666/decrypt", 
    key_file="encrypted_key.json"
)

password2 = get_password(
    server_url="http://localhost:6666/decrypt",
    encrypted_data="xxx", 
    iv="xxx"
)

password3 = get_password(
    encrypted_data="xxx", 
    iv="xxx",
    local_key="xxx"
)

print("password1: ", password1)
print("password2: ", password2)
print("password3: ", password3)