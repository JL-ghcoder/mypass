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