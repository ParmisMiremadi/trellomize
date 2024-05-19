import json
import argparse
import os

if not os.path.exists("admin.json"):
    open("admin.json", "w").close()

def create_admin(username, password):
    with open("admin.json", "r") as file:
        for line in file:
            username1 = line.strip().split(",")[0]

            if username == username1:
                print("Error: The entered information is duplicate!")
                return
    with open("admin.json", "a") as file:
        file.write(f"{username},{password}\n")
        print("The new admin was successfully registered :)")

def main():
    parser = argparse.ArgumentParser(description="Create system admin")
    subparsers = parser.add_subparsers(dest="command", help="command help")
    parser_print = subparsers.add_parser("create-admin", help="Create system admin")
    parser_print.add_argument("--username", help="Username of the admin", required=True)
    parser_print.add_argument("--password", help="Password of the admin", required=True)
    args = parser.parse_args()

    if args.command =="create-admin" :
        create_admin(args.username, args.password)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
