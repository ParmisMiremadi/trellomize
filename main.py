import json
import os
from user import User as User
from user import clear_console as clear_console
from user import log_in
from user import sign_up
import projects
from projects import Project as Project


def pr_cyan(skk): print("\033[36m {}\033[00m".format(skk))


def pr_green(skk): print("\033[32m {}\033[00m".format(skk))


def pr_red(skk): print("\033[31m {}\033[00m".format(skk))


if not os.path.exists("projects.json"):
    with open("projects.json", "w") as file:
        json.dump([], file, indent=4)
    file.close()

user = User("", "", "")
projects_file_path = "projects.json"
projects_list = projects.projects_list
my_project = Project("", "", user)
users_list = projects.load_projects_from_file("user.json")

if len(projects.admin_list) > 0:
    admin_projects_as_leader = projects.admin_projects_as_leader  # List of dictionaries
    admin_projects_as_member = projects.admin_projects_as_member  # List of dictionaries

########################################################################################

run = True
true_bool = True
while run == true_bool:
    choice = "0"  # 1. sign up  2. Log in
    while choice != "1" and choice != "2":
        print("1. Sign up")
        print("2. Log in")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = sign_up()
            clear_console(2)
        elif choice == "2":
            user = log_in()
            clear_console(2)
        else:
            pr_red("Error: Invalid choice! Please try again.")
            clear_console(2)

    if user is None:
        if isinstance(user, float) and user == 1.72:
            pr_red("Error: Your sign up was unsuccessful! Please try again.")
            clear_console(2)

        elif isinstance(user, float) and user == 3.14:
            pr_red("Error: Your log in was unsuccessful! Please try again.")
            clear_console(2)

    elif user.is_admin != true_bool:
        choice_1 = "0"  # 1. New project  2. My projects  3. Exit
        while choice_1 != "3":
            print("Choose one of the following options.")
            print("1. New project\n2. My projects\n3. Exit")
            choice_1 = input("Enter your choice: ")

            if choice_1 == "1":  # 1. New project
                os.system("cls")
                project_object = projects.create_a_project(user)
                if isinstance(project_object, Project):
                    user = project_object.to_dict_and_save_to_file(projects_file_path, user)
                    pr_green("Creating a new project")
                    clear_console(1)
                    pr_green("Creating a new project.")
                    clear_console(1)
                    pr_green("Creating a new project..")
                    clear_console(1)
                    pr_green("Creating a new project...")
                    clear_console(1)
                    # List of dictionaries:
                    projects_list = projects.load_projects_from_file(projects_file_path)
                    print("\033[36m {}\033[32m {}\033[36m {}\033[00m".format
                          ("Project created successfully.\n You are now the "
                           "leader of the project", f"{project_object.get_project_title()}", "."))
                    print("\033[36m {}\033[32m {}\033[00m".format
                          ("Project ID:", f"{project_object.get_project_id()}"))
                    clear_console(5)
                else:
                    pass

            elif choice_1 == "2":  # 2. My projects
                os.system("cls")
                if isinstance(projects.show_list_of_projects_and_choose(user), Project):
                    my_project = projects.show_list_of_projects_and_choose(user)
                    user, my_project = projects.options_for_my_project(user, my_project)
                else:
                    choice_1 = "0"

            elif choice_1 == "3":  # 3. Exit
                os.system("cls")
                pr_green("Exiting program...")
                clear_console(2)
                pr_green("Exit code: 0")
                run = not true_bool

            else:
                pr_red("Error: Invalid choice! Please try again.")
                clear_console(2)

    elif user.is_admin == true_bool:
        ch_1 = "-1"  # 1. New project  2. My projects  3. Activate users 4. Deactivate users 5. Exit
        while ch_1 != "0":
            print("Choose one of the following options.")
            print("1. New project\n2. My projects\n3. Activate users\n4. Deactivate users\n5. Exit")
            ch_1 = input("Enter your choice: ")

            if ch_1 == "1":  # 1. New project
                os.system("cls")
                project_object = projects.create_a_project(user)
                if isinstance(project_object, Project):
                    user = project_object.to_dict_and_save_to_file(projects_file_path, user)
                    pr_green("Creating a new project")
                    clear_console(1)
                    pr_green("Creating a new project.")
                    clear_console(1)
                    pr_green("Creating a new project..")
                    clear_console(1)
                    pr_green("Creating a new project...")
                    clear_console(1)
                    projects_list = projects.load_projects_from_file(
                        projects_file_path)  # List of dictionaries
                    print("\033[36m {}\033[32m {}\033[36m {}\033[00m".format
                          ("Project created successfully.\n You are now the "
                           "leader of the project", f"{project_object.get_project_title()}", "."))
                    print("\033[36m {}\033[32m {}\033[00m".format
                          ("Project ID:", f"{project_object.get_project_id()}"))
                    clear_console(5)

                else:
                    pass

            elif ch_1 == "2":  # 2. My projects
                os.system("cls")
                if isinstance(projects.show_list_of_projects_and_choose(user), Project):
                    my_project = projects.show_list_of_projects_and_choose(user)
                    user, project_object = projects.options_for_my_project(user, my_project)
                else:
                    ch_1 = 0

            elif ch_1 == "3":  # 3. Activate users
                os.system("cls")
                projects.activate_users(users_list)

            elif ch_1 == "4":  # 4. Deactivate users
                os.system("cls")
                projects.deactivate_users(users_list)

            elif ch_1 == "5":  # 5. Exit
                os.system("cls")
                pr_green("Exiting program...")
                clear_console(2)
                pr_green("Exit code: 0")
                ch_1 = "0"
                run = not true_bool

            else:
                pr_red("Error: Invalid choice! Please try again.")
                clear_console(2)
                ch_1 = "-1"

    else:
        print("Exiting program...")
        clear_console(2)
        pr_red("Exit code: 1")
        run = not true_bool
