import json
import os
import re
import getpass
import time
import bcrypt

if not os.path.exists("user.json"):
    open("user.json", "w").close()


class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.__password = password
        self.be_active = True
        self.projects_as_leader = []
        self.projects_as_member = []


def clear_console(time1):
    time.sleep(time1)
    os.system("cls" if os.name == "nt" else "clear")


def is_valid_email(email):
    valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(valid_email, email)


def sign_up():
    while True:
        email = input("Enter your email: ")
        if not is_valid_email(email):
            print("Error: Invalid email format!")
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
                print("Error: The entered information is duplicate!")
                return
    with open("user.json", "a") as file:
        file.write(f"{email} ; {username} ; {encrypted_password.decode("utf-8")} ; {user_obj.be_active} ; {user_obj.projects_as_leader} ; {user_obj.projects_as_member}\n")
        print("Your sign in was successful :)")
    return user_obj


def log_in():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    with open("user.json", "r") as file:
        for line in file:
            username1 = line.strip().split(" ; ")[1]
            password1 = line.strip().split(" ; ")[2]
            be_active1 = line.strip().split(" ; ")[3]
            true_bool = True
            if username == username1:
                if bcrypt.checkpw(password.encode("utf-8"), password1.encode("utf-8")):
                    if bool(be_active1) != true_bool:
                        print("Error: You don't have access to your account!")
                        return
                    else:
                        print("Your log in was successful :)")
                        user_obj = User(line.strip().split(" ; ")[0], username1, password1)
                        return user_obj
                else:
                    print("Error: The password is invalid!")
                    return
        print("Error: Username not found!")

