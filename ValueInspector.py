import main as root


def password(input_password, user_name):
    input_password = input_password.lower()
    user_name = user_name.lower()
    if len(input_password) < 6:
        print("\nPassword should be longer than 5 characters")
    elif len(input_password) > 30:
        print("\nPassword should not be longer than 30 characters")
    else:
        if input_password.isdigit():
            print("Password should be a mix of alpha numeric characters\n")
        elif (input_password in user_name) or (input_password == user_name):
            print("\nUser name and password cannot be similar")
        else:
            return 1


def username(user_name):
    user_name = user_name.lower()
    length = len(user_name)
    if length < 3:
        print("\nUser name should be at least 3 characters long")
    elif length > 20:
        print("\nUser name cannot be longer than 20 characters")
    else:
        if user_name.isdigit():
            print("\nUser name should be a mix of alpha numeric characters")
        elif (user_name == "exit") or (user_name == "back"):
            root.main()
        else:
            return 1


def data(value):
    value = value.lower()
    if len(value) > 200:
        print("\nData cannot be longer than 200 characters")
    elif (value == "exit") or (value == "back"):
        root.main()
    else:
        return 1
