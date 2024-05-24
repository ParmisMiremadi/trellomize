import json
import argparse
import os
import bcrypt

if not os.path.exists("admin_1.json"):
    with open("admin_1.json", "w") as file:
        json.dump([], file, indent=4)
    file.close()


def create_admin(username, password):
    with open("admin_1.json", "r") as file_1:
        admin_list = json.load(file_1)
    if len(admin_list) > 0:
        username1 = admin_list[0]["username"]

        if username == username1:
            print("Error: The entered information is duplicate!")
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

    with open("admin_1.json", "w") as file_1:
        json.dump(new_admin_list, file_1, indent=4)
        print("The new admin was successfully registered :)")


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
