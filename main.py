import json
import os
import re
import getpass
import time
import bcrypt


def pr_cyan(skk): print("\033[36m {}\033[00m".format(skk))


def pr_green(skk): print("\033[32m {}\033[00m".format(skk))


def pr_red(skk): print("\033[31m {}\033[00m".format(skk))


def clear_console(time1):
    time.sleep(time1)
    os.system("cls" if os.name == "nt" else "clear")


if not os.path.exists("user.json"):
    open("user.json", "w").close()

if not os.path.exists("admin.json"):
    open("admin.json", "w").close()


class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.__password = password
        self.is_active = True
        self.is_admin = False
        self.projects_as_leader = []
        self.projects_as_member = []


class Admin:
    def __init__(self, admin_username, admin_password):
        self.admin_username = admin_username
        self.__admin_password = admin_password
        self.is_admin = True
        self.projects_as_leader = []
        self.projects_as_member = []


def is_valid_email(email):
    valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(valid_email, email)


def sign_up():
    os.system("cls")
    while True:
        email = input("Enter your email: ")
        if not is_valid_email(email):
            pr_red("Error: Invalid email format!")
            clear_console(2)
        else:
            break

    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    string_password = encrypted_password.decode('utf8')
    user_obj = User(email, username, encrypted_password)

    try:
        with open('user.json', 'r') as file:
            users_list = json.load(file)
    except FileNotFoundError:
        print(f'File not found: user.json\nCreating file...')
        clear_console(2)
        users_list = []

    new_user_dict = {
        'email': email,
        'username': username,
        'password': string_password,
        'is_active': user_obj.is_active,
        'projects_as_leader': [],
        'projects_as_member': []
    }
    users_list.append(new_user_dict)
    with open('user.json', 'w') as file:
        json.dump(users_list, file, indent=4)
        pr_green("Your sign in was successful :)")
    return user_obj


def log_in(users_list: list[dict]):
    os.system("cls")
    print("1. Log in as user")
    print("2. Log in as admin")
    choice1 = input("Enter your choice: ")

    if choice1 == "1":
        os.system("cls")
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        true_bool = True

        with open('user.json', 'r') as file:
            users_list = json.load(file)
            for iterate in range(len(users_list)):
                if users_list[iterate]['username'] == username:
                    email1 = users_list[iterate]['email']
                    is_active1 = users_list[iterate]['is_active']
                    string_password = users_list[iterate]['password']
                    if bcrypt.checkpw(password.encode("utf-8"), string_password.encode("utf-8")):
                        if bool(is_active1) != true_bool:
                            pr_red("Error: You don't have access to your account!")
                            return
                        else:
                            pr_green("Your log in was successful :)")
                            user_obj = User(email1, username, string_password)
                            user_obj.projects_as_leader = users_list[iterate]['projects_as_leader']
                            user_obj.projects_as_member = users_list[iterate]['projects_as_member']
                            return user_obj
                    else:
                        pr_red("Error: The password is invalid!")
                        return
            pr_red("Error: Username not found!")

    elif choice1 == "2":
        os.system("cls")
        admin_username = input("Enter your username: ")
        admin_password = getpass.getpass("Enter your password: ")

        with open("admin.json", "r") as file:
            for line in file:
                admin_username1 = line.strip().split(" ; ")[0]
                admin_password1 = line.strip().split(" ; ")[1]

                if admin_username == admin_username1:
                    if bcrypt.checkpw(admin_password.encode("utf-8"), admin_password1.encode("utf-8")):
                        pr_green("Your log in was successful :)")
                        admin_obj = Admin(admin_username1, admin_password1)
                        return admin_obj
                    else:
                        pr_red("Error: The password is invalid!")
                        return
            pr_red("Error: Username not found!")

    else:
        pr_red("Error: Invalid value!")
