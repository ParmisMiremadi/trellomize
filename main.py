import json
import os
import re
import getpass
import time
import bcrypt
 
if not os.path.exists("user.json"):
    open("user.json", "w").close()

def clear_consoule(time1):
    time.sleep(time1)
    os.system("cls" if os.name == "nt" else "clear")

def is_valid_email(email):
    valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(valid_email, email)

def signup():
    email = input("Enter your email: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    encrypted_password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    be_active = True

    if not is_valid_email(email):
        print("Error: Invalid email format!")
        return
    else:
        with open("user.json", "r") as file:
            for line in file:
                email1 = line.strip().split(",")[0]
                username1 = line.strip().split(",")[1]

                if email == email1 or username == username1:
                    print("Error: The entered information is duplicate!")
                    return   
        with open("user.json", "a") as file:
            file.write(f"{email},{username},{encrypted_password.decode("utf-8")},{be_active}\n")
            print("Sign in successful :)")

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    be_active = True
    
    with open("user.json", "r") as file:
        for line in file:
            username1 = line.strip().split(",")[1]
            password1 = line.strip().split(",")[2]
            be_active1 = line.strip().split(",")[3]
            
            if username == username1:
                if bcrypt.checkpw(password.encode("utf-8"), password1.encode("utf-8")):
                    if be_active != bool(be_active1):
                        print("Error: You don't have access to your account!")
                        return
                    else:
                        print("Log in successful :)")
                        return
                else:
                    print("Error: The password is invalid!")
                    return
        print("Error: Username not found!")

while True:
    print("1. Sign up")
    print("2. Log in")
    choice = input("Enter your choice: ")
    os.system("cls")

    if choice == "1":
        signup()
        clear_consoule(2)
    elif choice == "2":
        login()
        clear_consoule(2)
    else:
        print("Error: Invalid choice! Please try again.")
        clear_consoule(2)
       
