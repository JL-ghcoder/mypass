from mypass.getpass import get_password

password3 = get_password(
    encrypted_data="", 
    iv="",
    local_key=""
)

print("password3: ", password3)