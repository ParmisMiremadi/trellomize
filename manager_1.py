import json
import argparse
import os
import bcrypt
from loguru import logger


def pr_cyan(skk): print("\033[36m {}\033[00m".format(skk))


def pr_green(skk): print("\033[32m {}\033[00m".format(skk))


def pr_red(skk): print("\033[31m {}\033[00m".format(skk))


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


def create_admin(username, password):
    with open("admin.json", "r") as file_1:
        admin_list = json.load(file_1)
    if len(admin_list) > 0:
        username1 = admin_list[0]["username"]

        if username == username1:
            log_error("Error: The entered information is duplicate!")
            pr_red("Error: The entered information is duplicate!")
            return

    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    string_password = encrypted_password.decode("utf8")

    new_admin_dict = {
        "email": "",
        "username": username,
        "password": string_password,
        "is_active": "",
        "projects_as_leader": [],
        "projects_as_member": []
    }
    new_admin_list = [new_admin_dict]

    with open("admin.json", "w") as file_1:
        json.dump(new_admin_list, file_1, indent=4)
        log_info("Your sign up as admin was successful :)")
        pr_green("Your sign up as admin was successful :)")



def main():
    parser = argparse.ArgumentParser(description="Create system admin")
    subparsers = parser.add_subparsers(dest="command", help="command help")
    parser_print = subparsers.add_parser("create-admin", help="Create system admin")
    parser_print.add_argument("--username", help="Username of the admin", required=True)
    parser_print.add_argument("--password", help="Password of the admin", required=True)
    args = parser.parse_args()

    if args.command == "create-admin":
        create_admin(args.username, args.password)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
