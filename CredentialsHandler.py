import DataHandler as Dh
from cryptography.fernet import Fernet
key = "ftxTJgmXgp6A3LLm5MltUZS6NlnJiiis70RyNM8xRIA="

f = Fernet(key)


def encrypt_file(file_name):
    with open(file_name, "r") as file_r:
        insecure_content = file_r.read()
    secure_content = encrypt(insecure_content)
    with open(file_name, "wb") as file_w:
        file_w.write(secure_content)


def decrypt_file(file_name):
    with open(file_name, "rb") as file_r:
        secure_content = file_r.read()
    insecure_content = decrypt(secure_content)
    with open(file_name, "w") as file_w:
        file_w.write(insecure_content)


def encrypt(message):
    encoded_message = message.encode()
    encrypted = f.encrypt(encoded_message)
    return encrypted


def decrypt(message):
    decrypted = f.decrypt(message)
    output = decrypted.decode()
    return output


def change_password(username, old_password, new_password, file_name):
    decrypt_file("data.txt")
    username = username.lower()
    with open(file_name, "r+") as file:
        data = Dh.read_data(username, old_password, file_name, False)
        old_string = username + " : " + old_password + " %%% -- " + data + " --end\n"
        new_string = username + " : " + new_password + " %%% -- " + data + " --end\n"
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line != old_string:
                file.write(line)
        file.write(new_string)
        file.truncate()
    encrypt_file("data.txt")


def write_credentials(username, password, file_name):
    decrypt_file("data.txt")
    username = username.lower()
    with open(file_name, "a") as file:
        output_string = username + " : " + password + " %%% -- " + " --end\n"
        file.write(output_string)
    encrypt_file("data.txt")
    print("Your account was created successfully")


def remove_credentials(username, password, file_name):
    decrypt_file("data.txt")
    username = username.lower()
    with open(file_name, "r+") as file:
        replace_string = username + " : " + password + " %%% -- "
        length = len(replace_string)
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line[:length] != replace_string:
                file.write(line)
        file.truncate()
    encrypt_file("data.txt")


def verify_username(username, file_name):
    decrypt_file("data.txt")
    username = username.lower()
    with open(file_name, "r") as file:
        lines = file.readlines()
    encrypt_file("data.txt")
    initial_string = username + " : "
    initial_length = len(initial_string)
    for line in lines:
        if line[:initial_length] == initial_string:
            return 1
    else:
        return 0


def verify_credentials(username, password, file_name):
    decrypt_file("data.txt")
    username = username.lower()
    with open(file_name, "r") as file:
        lines = file.readlines()
    encrypt_file("data.txt")
    user_string = username + " : " + password + " %%% -- "
    initial_length = len(user_string)
    for line in lines:
        if line[:initial_length] == user_string:
            return 1
    else:
        return 0
