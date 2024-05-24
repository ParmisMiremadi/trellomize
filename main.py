import json
import os
import re
import getpass
import time
import bcrypt


def pr_cyan(skk): print("\033[36m {}\033[00m" .format(skk))
def pr_green(skk): print("\033[32m {}\033[00m" .format(skk))
def pr_red(skk): print("\033[31m {}\033[00m" .format(skk))


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
        self.be_active = True
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
    user_obj = User(email, username, encrypted_password)

    with open("user.json", "r") as file:
        for line in file:
            email1 = line.strip().split(" ; ")[0]
            username1 = line.strip().split(" ; ")[1]

            if email == email1 or username == username1:
                pr_red("Error: The entered information is duplicate!")
                return
    with open("user.json", "a") as file:
        file.write(f"{email} ; {username} ; {encrypted_password.decode("utf-8")} ; {user_obj.be_active} ; {user_obj.projects_as_leader} ; {user_obj.projects_as_member}\n")
        pr_green("Your sign in was successful :)")
    return user_obj


def log_in():
    os.system("cls")
    print("1. Log in as user")
    print("2. Log in as admin")
    choice1 = input("Enter your choice: ")
    
    if choice1 == "1":
        os.system("cls")
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        with open("user.json", "r") as file:
            for line in file:
                username1 = line.strip().split(" ; ")[1]
                
                if username == username1:
                    password1 = line.strip().split(" ; ")[2]
            
                    if bcrypt.checkpw(password.encode("utf-8"), password1.encode("utf-8")):
                        be_active1 = line.strip().split(" ; ")[3]
                        true_bool = True
                        
                        if bool(be_active1) != true_bool:
                            pr_red("Error: You don't have access to your account!")
                            return
                        else:
                            email1 = line.strip().split(" ; ")[0]
                            
                            pr_green("Your log in was successful :)")
                            user_obj = User(email1, username1, password1)
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

                if admin_username == admin_username1:
                    admin_password1 = line.strip().split(" ; ")[1]

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

