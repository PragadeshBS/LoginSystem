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


def write_data(username, password, data, file_name):
    decrypt_file(file_name)
    username = username.lower()
    with open(file_name, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        replace_string = username + " : " + password + " %%% -- "
        length = len(replace_string)
        output_string = username + " : " + password + " %%% -- " + data + " --end\n"
        for line in lines:
            if line[:length] != replace_string:
                file.write(line)
        file.write(output_string)
        file.truncate()
    encrypt_file(file_name)
    return 1


def append_data(username, password, file_name, data_to_append, file_encrypted=True):
    if file_encrypted:
        decrypt_file(file_name)
    username = username.lower()
    existing_data = read_data(username, password, file_name, False)
    old_string = username + " : " + password + " %%% -- " + existing_data + " --end"
    length = len(old_string)
    new_string = username + " : " + password + " %%% -- " + existing_data + " " + data_to_append + " --end\n"
    with open(file_name, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if line[:length] != old_string:
                file.write(line)
        file.write(new_string)
        file.truncate()
    if file_encrypted:
        encrypt_file(file_name)
    return 1


def read_data(username, password, file_name, file_encrypted=True):
    if file_encrypted:
        decrypt_file(file_name)
    username = username.lower()
    with open(file_name, "r") as file:
        lines = file.readlines()
    if file_encrypted:
        encrypt_file(file_name)
    initial_string = username + " : " + password + " %%% -- "
    initial_length = len(initial_string)
    length = len(initial_string) + 7
    for line in lines:
        if line[:initial_length] == initial_string:
            if len(line) == length:
                return ""
            else:
                line_length = len(line)
                return line[initial_length:initial_length+line_length-length]
