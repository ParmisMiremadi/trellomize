import json
import os
import re
import getpass
import time
import bcrypt
from loguru import logger


def pr_cyan(skk): print("\033[36m {}\033[00m".format(skk))


def pr_green(skk): print("\033[32m {}\033[00m".format(skk))


def pr_red(skk): print("\033[31m {}\033[00m".format(skk))


def clear_console(time1):
    time.sleep(time1)
    os.system("cls" if os.name == "nt" else "clear")


if not os.path.exists("user.json"):
    with open("user.json", "w") as file:
        json.dump([], file, indent=4)
    file.close()

if not os.path.exists("admin.json"):
    with open("admin.json", "w") as file:
        json.dump([], file, indent=4)
    file.close()


logger.remove()
logger.add("logfile.log", rotation="500 MB", format="{time} - {level} - {file} - {message}")


def log_info(massage):
    logger.info(massage)


def log_warning(massage):
    logger.warning(massage)


def log_error(massage):
    logger.error(massage)
 

class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.__password = password
        self.is_active = True
        self.is_admin = False
        self.projects_as_leader = []
        self.projects_as_member = []


class Admin(User):
    def __init__(self, email, username, password):
        super().__init__(email, username, password)
        self.email = ""
        self.is_active = ""
        self.is_admin = True


def is_valid_email(email):
    valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(valid_email, email)


def is_valid_username(username):
    return len(username)>=6


def is_valid_password(password):
    return len(password)>=8


def sign_up():
    os.system("cls")
    while True:
        email = input("Enter your email: ")
        if not is_valid_email(email):
            log_error("Error: Invalid email format!")
            pr_red("Error: Invalid email format!")
            clear_console(2)
        else:
            break

    while True:
        username = input("Enter your username: ")
        if not is_valid_username(username):
            log_error("Error: Invalid username format! username must be at list 6 characters.")
            pr_red("Error: Invalid username format! username must be at list 6 characters.")
        else:
            break
    
    while True:
        password = getpass.getpass("Enter your password: ")
        if not is_valid_password(password):
            log_error("Error: Invalid password format! password must be at list 8 characters.")
            pr_red("Error: Invalid password format! password must be at list 8 characters.")
        else:
            break
    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    string_password = encrypted_password.decode("utf8")
    user_obj = User(email, username, encrypted_password)

    with open("user.json", "r") as file_1:
        users_list = json.load(file_1)
    if len(users_list) > 0:
        for iterate in range(len(users_list)):
            if email == users_list[iterate]["email"] or username == users_list[iterate]["username"]:
                log_error("Error: The entered information is duplicate!")
                pr_red("Error: The entered information is duplicate!")
                return

    new_user_dict = {
        "email": email,
        "username": username,
        "password": string_password,
        "is_active": user_obj.is_active,
        "projects_as_leader": [],
        "projects_as_member": []
    }
    users_list.append(new_user_dict)

    with open("user.json", "w") as file_1:
        json.dump(users_list, file_1, indent=4)
        log_info("Your sign up as user was successful :)")
        pr_green("Your sign up as user was successful :)")
    return user_obj


def log_in():
    choice1 = "0"
    while choice1 != "1" and choice1 != "2":
        os.system("cls")
        print("1. Log in as user")
        print("2. Log in as admin")
        choice1 = input("Enter your choice: ")

        if choice1 == "1":    # 1. Log in as user
            os.system("cls")
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            true_bool = True

            with open("user.json", "r") as file_1:
                users_list = json.load(file_1)
                for iterate in range(len(users_list)):
                    username1 = users_list[iterate]["username"]

                    if username == username1:
                        string_password = users_list[iterate]["password"]

                        if bcrypt.checkpw(password.encode("utf-8"), string_password.encode("utf-8")):
                            is_active1 = users_list[iterate]["is_active"]

                            if bool(is_active1) != true_bool:
                                log_error("Error: You don't have access to your account!")
                                pr_red("Error: You don't have access to your account!")
                                return 0
                            else:
                                email1 = users_list[iterate]["email"]

                                log_info("Your log in as user was successful :)")
                                pr_green("Your log in as user was successful :)")
                                user_obj = User(email1, username, string_password)
                                user_obj.projects_as_leader = users_list[iterate]["projects_as_leader"]
                                user_obj.projects_as_member = users_list[iterate]["projects_as_member"]
                                return user_obj
                        else:
                            log_error("Error: The password is invalid!")
                            pr_red("Error: The password is invalid!")
                            return
                        
                log_error("Error: Username not found!")
                pr_red("Error: Username not found!")

        elif choice1 == "2":    # Log in as admin
            os.system("cls")
            admin_username = input("Enter your username: ")
            admin_password = getpass.getpass("Enter your password: ")

            with open("admin.json", "r") as file_1:
                admin_list = json.load(file_1)
                if len(admin_list) > 0:
                    admin_username1 = admin_list[0]["username"]

                    if admin_username == admin_username1:
                        admin_password1 = admin_list[0]["password"]

                        if bcrypt.checkpw(admin_password.encode("utf-8"), admin_password1.encode("utf-8")):
                            log_info("Your log in as admin was successful :)")
                            pr_green("Your log in as admin was successful :)")
                            admin_obj = Admin(" ", admin_username1, admin_password1)
                            admin_obj.projects_as_leader = admin_list[0]["projects_as_leader"]
                            admin_obj.projects_as_member = admin_list[0]["projects_as_member"]
                            return admin_obj
                        else:
                            log_error("Error: The password is invalid!")
                            pr_red("Error: The password is invalid!")
                            return

                log_error("Error: Username not found!")
                pr_red("Error: Username not found!")
                return 0
        else:
            pr_red("Error: Invalid choice! Please try again.")
            clear_console(2)

