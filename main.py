import json
import random
import os
import time
import user
from user import User as User
from user import clear_console as clear_console
from user import log_in
from user import sign_up
import projects_and_tasks
from projects_and_tasks import Project as Project


def pr_cyan(skk): print("\033[36m {}\033[00m".format(skk))


def pr_green(skk): print("\033[32m {}\033[00m".format(skk))


def pr_red(skk): print("\033[31m {}\033[00m".format(skk))


if not os.path.exists('projects.json'):
    with open('projects.json', 'w') as file:
        json.dump([], file, indent=4)
    file.close()

user = User("", "", "")
projects_file_path = 'projects.json'
projects_list = projects_and_tasks.projects_list
my_project = Project("", "", user)
users_list = projects_and_tasks.load_projects_from_file('user.json')

if len(projects_and_tasks.admin_list) > 0:
    admin_projects_as_leader = projects_and_tasks.admin_projects_as_leader  # List of dictionaries
    admin_projects_as_member = projects_and_tasks.admin_projects_as_member  # List of dictionaries

########################################################################################

run = True
true_bool = True
while run == true_bool:
    choice = "0"  # 1. sign up  2. Log in
    while choice != "1" and choice != "2":
        clear_console(2)
        print("1. Sign up")
        print("2. Log in")
        choice = input("Enter your choice: ")
        os.system("cls")

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
        pr_red("Error: Invalid input! Please try again.")
        clear_console(2)

    elif isinstance(user, int) and user == 0:
        print('Exiting program...')
        clear_console(2)
        pr_red('Exit code: 1')
        run = not true_bool

    elif user.is_admin != true_bool:
        choice_1 = "0"  # 1. New project  2. My projects  3. Exit
        while choice_1 != "3":
            print('Choose one of the following options.')
            pr_cyan('1. New project\n 2. My projects\n 3. Exit\n')
            choice_1 = (input())
            clear_console(1.5)

            if choice_1 == "1":    # 1. New project
                project_object = projects_and_tasks.create_a_project(user)
                if isinstance(project_object, Project):
                    user = project_object.to_dict_and_save_to_file(projects_file_path, user)
                    time.sleep(1)
                    pr_green('Creating a new project')
                    clear_console(1)
                    pr_green('Creating a new project.')
                    clear_console(1)
                    pr_green('Creating a new project..')
                    clear_console(1)
                    pr_green('Creating a new project...')
                    clear_console(1)
                    # List of dictionaries:
                    projects_list = projects_and_tasks.load_projects_from_file(projects_file_path)
                    print("\033[36m {}\033[32m {}\033[36m {}\033[00m".format
                          ("Project created successfully.\nYou are now the "
                           "leader of the project", f'{project_object.get_project_title()}', '.'))
                    print("\033[36m {}\033[32m {}\033[00m".format
                          ('Project ID: ', f'{project_object.get_project_id()}'))

                else:
                    pass

            elif choice_1 == "2":    # 2. My projects
                clear_console(2)
                if isinstance(projects_and_tasks.show_list_of_projects_and_choose(user), Project):
                    print(f"2 __ The user: {user.username}")  #.
                    print(f"2 __ The leader: {my_project.leader_username}")  #.
                    my_project = projects_and_tasks.show_list_of_projects_and_choose(user)
                    print(f"3 __ The user: {user.username}")  #.
                    print(f"3 __ The leader: {my_project.leader_username}")  #.
                    user, my_project = projects_and_tasks.options_for_my_project(user, my_project)
                    print(f"4 __ The user: {user.username}")  #.
                    print(f"4 __ The leader: {my_project.leader_username}")  #.
                else:
                    choice_1 = "0"

            elif choice_1 == "3":    # 3. Exit
                clear_console(1)
                pr_green('Exiting program...')
                clear_console(2)
                pr_green('Exit code: 0')
                run = not true_bool

            else:
                print('Invalid choice.\nPlease try again.')

    elif user.is_admin == true_bool:
        ch_1 = "-1"  # 1. New project  2. My projects  3. Activate users 4. Deactivate users 5. Exit
        while ch_1 != "0":
            print('Choose one of the following options.')
            pr_cyan('1. New project\n 2. My projects\n 3. Activate users\n 4. Deactivate users\n 5. Exit\n')
            ch_1 = input()

            if ch_1 == "1":  # 1. New project
                project_object = projects_and_tasks.create_a_project(user)
                if isinstance(project_object, Project):
                    user = project_object.to_dict_and_save_to_file(projects_file_path, user)
                    time.sleep(1)
                    pr_green('Creating a new project')
                    clear_console(1)
                    pr_green('Creating a new project.')
                    clear_console(1)
                    pr_green('Creating a new project..')
                    clear_console(1)
                    pr_green('Creating a new project...')
                    clear_console(1)
                    projects_list = projects_and_tasks.load_projects_from_file(
                        projects_file_path)  # List of dictionaries
                    print("\033[36m {}\033[32m {}\033[36m {}\033[00m".format
                          ("Project created successfully.\nYou are now the "
                           "leader of the project", f'{project_object.get_project_title()}', '.'))
                    print("\033[36m {}\033[32m {}\033[00m".format
                          ('Project ID: ', f'{project_object.get_project_id()}'))

            elif ch_1 == "2":  # 2. My projects
                if isinstance(projects_and_tasks.show_list_of_projects_and_choose(user), Project):
                    my_project = projects_and_tasks.show_list_of_projects_and_choose(user)
                    user, project_object = projects_and_tasks.options_for_my_project(user, my_project)
                else:
                    ch_1 = 0

            elif ch_1 == "3":  # 3. Activate users
                projects_and_tasks.activate_users(users_list)

            elif ch_1 == "4":  # 4. Deactivate users
                projects_and_tasks.deactivate_users(users_list)

            elif ch_1 == "5":  # 5. Exit
                clear_console(1)
                pr_green('Exiting program...')
                clear_console(2)
                pr_green('Exit code: 0')
                ch_1 = "0"
                run = not true_bool

            else:
                pr_red("Error: Invalid value!")
                ch_1 = "-1"
