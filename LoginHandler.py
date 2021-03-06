import main as root
import DataHandler as Dh
import CredentialsHandler as Ch
import ValueInspector as Check
import sys


def login_handler(current_user, current_user_password, file_name, relaunch=False, pwd_changed=0, delete=0, clear_data=0):
    root.clear()
    if not relaunch:
        print(f"\nYou are now logged in as {current_user}")
    if clear_data == 1:
        print("Your data has been successfully removed")
    elif clear_data == -1:
        print("No changes were made to your data")
    if pwd_changed == 1:
        print("Your password has been successfully changed")
    elif pwd_changed == -1:
        print("Passwords did not match, password could not be changed")
    elif pwd_changed == -2:
        print("Incorrect password, password could not be changed")
    if delete == -1:
        print("Incorrect password, your account has not been deleted")
    old_data = Dh.read_data(current_user, current_user_password, file_name)
    if (old_data == "") and not relaunch:
        print("\nEnter any data that you want to store.")
        print("Only those who have your username and password can access this data.")
        print("Make sure that you remember your password.")
        print("You cannot retrieve your data once you forget your password.")
        print("\nThere is currently no data stored in your account.")
    elif (old_data == "") and relaunch:
        print("\nCurrently there is no data in your account")
    else:
        print("\nHere is the data stored in your account...\n")
        print(old_data)
    print("\nUse...")
    if old_data == "":
        print("'a' - add data to your account")
    else:
        print("'add' - append new data to your existing data")
        print("'m' - modify your data")
        print("'c' - clear your data")
    print("'ch' - change your password")
    print("'exit' - logout and exit")
    print("'s' - logout and sign in/sign up with a different account")
    print("'delete' - delete your account\n")
    while True:
        user_input = input(" >>").lower().strip()
        if (old_data != "") and (user_input == "add"):
            append_data = input("Enter data to add >>")
            while Check.data(append_data) != 1:
                append_data = input("Enter new data >>")
            else:
                Dh.append_data(current_user, current_user_password, file_name, append_data)
                login_handler(current_user, current_user_password, file_name, True)
        elif (user_input == "m") or (user_input == "a"):
            new_data = input("Enter new data >>")
            while Check.data(new_data) != 1:
                new_data = input("Enter new data >>")
            else:
                Dh.write_data(current_user, current_user_password, new_data, file_name)
                login_handler(current_user, current_user_password, file_name, True)
            break
        elif user_input == "ch":
            confirmation = input("Enter your current password to proceed >>")
            if confirmation == current_user_password:
                new_pwd = input("\nEnter new password >>")
                while (Check.password(new_pwd, current_user) != 1) or (new_pwd == current_user_password):
                    if new_pwd == current_user_password:
                        print("Your new password is similar to your current password, try a different one")
                    new_pwd = input("Enter new password >>")
                else:
                    confirm_new_pwd = input("Re-enter your new password >>")
                    if confirm_new_pwd == new_pwd:
                        Ch.change_password(current_user, current_user_password, new_pwd, file_name)
                        login_handler(current_user, new_pwd, file_name, True, 1)
                    else:
                        login_handler(current_user, current_user_password, file_name, True, -1)
            else:
                login_handler(current_user, current_user_password, file_name, True, -2)
        elif user_input == "delete":
            print("\nYou are about to PERMANENTLY DELETE your account and related data, are you sure?")
            confirmation = input("Enter your password to proceed >>")
            if confirmation == current_user_password:
                Ch.remove_credentials(current_user, current_user_password, file_name)
                root.clear()
                print("Your account and related data have been successfully deleted")
                root.main()
            else:
                login_handler(current_user, current_user_password, file_name, True, delete=-1)
        elif user_input == "c":
            confirmation = input("This will clear all your data, are you sure? (y/n) >>").lower().strip()
            if (confirmation == "y") or (confirmation == "yes"):
                Dh.write_data(current_user, current_user_password, "", file_name)
                login_handler(current_user, current_user_password, file_name, True, clear_data=1)
                break
            elif (confirmation == "n") or (confirmation == "no"):
                login_handler(current_user, current_user_password, file_name, True, clear_data=-1)
                break
            else:
                print("That was not expected, your data was not cleared")
                continue
        elif user_input == "exit":
            sys.exit()
        elif user_input == "s":
            root.clear()
            print("You have been successfully logged out of your account")
            root.main()
            break
        else:
            print(f"{user_input} is not a recognised command")
