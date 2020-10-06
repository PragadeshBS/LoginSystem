try:
    import sys
    import LoginHandler as Login
    import CredentialsHandler as Ch
    import ValueInspector as Check
    from os import system, name
    from cryptography import *
    import cryptography
    from cryptography.fernet import Fernet
    with open("key.key", "r") as key_file:
        key = key_file.read()

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


    def sign_up():
        user_name = input("\nEnter a user name>>").strip()
        if (user_name.lower() == "back") or (user_name.lower() == "exit"):
            main()
        while Check.username(user_name) != 1:
            user_name = input("Try a different user name>>")
        else:
            if Ch.verify_username(user_name, "data.txt") == 1:
                print("User name already exists, sign in or use a different username")
                main()
        user_password = input("Enter a password>>").strip()
        if (user_password.lower() == "back") or (user_password.lower() == "exit"):
            main()
        while Check.password(user_password, user_name) != 1:
            user_password = input("Enter a password>>")
        else:
            Ch.write_credentials(user_name, user_password, "data.txt")
            Login.login_handler(user_name, user_password, "data.txt")


    def sign_in():
        user_name = input("\nEnter your user name>>").strip()
        if (user_name.lower() == "back") or (user_name.lower() == "exit"):
            main()
        if Ch.verify_username(user_name, "data.txt") == 1:
            while True:
                user_password = input("Enter your password>>").strip()
                if (user_password.lower() == "back") or (user_password.lower() == "exit"):
                    main()
                    break
                elif Ch.verify_credentials(user_name, user_password, "data.txt") == 1:
                    Login.login_handler(user_name, user_password, "data.txt")
                    break
                else:
                    print("Invalid password, try again...\n")
        elif (user_name == "back") or (user_name == "exit"):
            main()
        else:
            print(f"We could not find an account with the name {user_name}. Try signing up")
            main()


    def main():
        decrypt_file("data.txt")
        with open("data.txt", "r") as file:
            initials = file.read(17)
        encrypt_file("data.txt")
        if not initials == "%%%File secure---":
            print("Seems like some files are corrupt, data cannot be processed...")
            input("You may press 'Enter' to exit>>")
            sys.exit()
        while True:
            user_input = input("\nSign in(s) or Sign up(u)>>").lower().strip()
            if user_input == "s":
                sign_in()
            elif user_input == "u":
                sign_up()
            elif user_input == "exit":
                sys.exit()
            else:
                print("\nUse:\n'u' - sign up\n's' - sign in\n'exit' - quit the program")


    def logout():
        sys.exit()


    def clear():

        # for windows
        if name == 'nt':
            _ = system('cls')

            # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


    if __name__ == "__main__":
        main()

except FileNotFoundError:
    print("Looks like some files are missing, data cannot be processed...")
    input("You may press 'Enter' to exit>>")
    sys.exit()

except cryptography.fernet.InvalidToken:
    print("Seems like some files are corrupt, data cannot be processed...")
    input("You may press 'Enter' to exit>>")
    sys.exit()
