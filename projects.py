import json
import os
from user import User
from user import clear_console
from user import Admin
import tasks
from loguru import logger


def pr_cyan(skk): print("\033[36m {}\033[00m".format(skk))


def pr_green(skk): print("\033[32m {}\033[00m".format(skk))


def pr_red(skk): print("\033[31m {}\033[00m".format(skk))


logger.remove()
logger.add("logfile.log", rotation="500 MB", format="{time} - {level} - {file} - {message}")


def log_info(massage):
    logger.info(massage)


def log_warning(massage):
    logger.warning(massage)


def log_error(massage):
    logger.error(massage)


user_file_path = "user.json"
projects_file_path = "projects.json"
admin_file_path = "admin.json"


class Project:
    def __init__(self, project_title, project_id, leader: User):
        self.__project_title = project_title
        self.__project_id = project_id
        self.leader_username = leader.username
        self.members = []
        self.tasks = []

    def get_project_title(self):
        return self.__project_title

    def get_project_id(self):
        return self.__project_id

    def to_dict_and_save_to_file(self, file_path, leader: User):
        new_project_dict = {
            "project_title": self.__project_title,
            "project_id": self.__project_id,
            "leader": self.leader_username,
            "members": self.members,
            "tasks": self.tasks
        }

        projects_dicts = load_projects_from_file(file_path)  # List of dictionaries
        projects_dicts.append(new_project_dict)
        save_projects_to_file(file_path, projects_dicts)

        # Appending the new project to the object's projects_as_leader list
        leader.projects_as_leader.append(new_project_dict)

        # Save the new projects_as_leader list to file
        if isinstance(leader, Admin):  # Saving to 'admin.json'
            with open(admin_file_path, "r") as f:
                users_list = json.load(f)
                for iterate in range(len(users_list)):
                    if users_list[iterate]["username"] == leader.username:
                        users_list[iterate]["projects_as_leader"] = leader.projects_as_leader
            save_projects_to_file(admin_file_path, users_list)

        else:  # Saving to 'user.json'
            with open(user_file_path, "r") as f:
                users_list = json.load(f)
                for iterate in range(len(users_list)):
                    if users_list[iterate]["username"] == leader.username:
                        users_list[iterate]["projects_as_leader"] = leader.projects_as_leader
            save_projects_to_file(user_file_path, users_list)

        return leader


def save_projects_to_file(file_path, project_dict):
    with open(file_path, "w") as file_1:
        json.dump(project_dict, file_1, indent=4)


def load_projects_from_file(file_path):  # Returns a list
    try:
        with open(file_path, "r") as file_1:
            projects_1 = json.load(file_1)
    except FileNotFoundError:
        projects_1 = []
    return projects_1


projects_list = load_projects_from_file(projects_file_path)  # List of dictionaries

with open(admin_file_path, "r") as file:
    admin_list = json.load(file)
if len(admin_list) > 0:
    admin_projects_as_leader = admin_list[0]["projects_as_leader"]  # List of dictionaries
    admin_projects_as_member = admin_list[0]["projects_as_member"]  # List of dictionaries


def create_a_project(leader: User):  # Returns an object of Project. It has to be saved!
    project_title = input("The title of your project: ")  # Needs to be checked in the projects file
    project_id = input("The ID of your project: ")  # Needs to be checked in the projects file
    is_unique = True
    if isinstance(leader, Admin):
        #@
        with open(admin_file_path, "r") as f:
            admin_list_1 = json.load(f)
        if len(admin_list) > 0:
            admin_projects_as_leader_1 = admin_list_1[0]["projects_as_leader"]  # List of dictionaries
            admin_projects_as_member_1 = admin_list_1[0]["projects_as_member"]  # List of dictionaries
            is_unique = is_project_unique(admin_projects_as_leader_1, project_id)
            if is_unique:
                is_unique = is_project_unique(admin_projects_as_member, project_id)
    else:
        #@
        projects_list_1 = load_projects_from_file(projects_file_path)
        is_unique = is_project_unique(projects_list_1, project_id)
    if not is_unique:
        log_error("Error: This ID already exists for another project.")
        log_error("       Action failed!")
        pr_red("Error: This ID already exists for another project.")
        pr_red("       Action failed!")
        clear_console(2)
        return 1

    project_1 = Project(project_title, project_id, leader)
    clear_console(2)
    return project_1


def is_project_unique(projects_list_1: list[dict], new_project_id):
    for iterator in range(len(projects_list_1)):
        if projects_list_1[iterator]["project_id"] == new_project_id:
            return False
    return True


def show_list_of_projects_and_choose(user_obj: User):  # If Back, returns 0; else returns a Project obj
    projects_as_leader_list = user_obj.projects_as_leader
    projects_as_member_list = user_obj.projects_as_member

    it_leader = len(projects_as_leader_list)
    it_member = len(projects_as_member_list)
    ch = -1
    it = 0
    while ch not in range(it_member + it_leader + 1):
        print("0. Back")
        print("Your projects as the leader:")
        if it_leader > 0:
            for it in range(it_leader):
                pr_cyan(f"    {it + 1}. {projects_as_leader_list[it].get("project_title")}")
        else:
            pr_cyan("    No projects as leader.")
        it = 0
        print("\nYour projects as a member:")
        if it_member > 0:
            for it in range(it_member):
                pr_cyan(f"    {it_leader + it + 1}. {projects_as_member_list[it]["project_title"]}")
        else:
            pr_cyan("    No projects as a member.")

        try:
            ch = int(input("\nEnter your choice: "))
        except ValueError:
            pr_red("Error: Invalid choice! Please try again.")
            clear_console(2)
        else:
            if isinstance(ch, int) and (ch < 0 or ch > (it_leader + it_member)):
                pr_red("Error: Invalid choice! Please try again.")
                clear_console(2)

            elif ch == 0:  # Going back
                print("Going back...")
                clear_console(2)
                return 0

            elif it_leader > 0 and 1 <= ch <= it_leader:  # Valid choice: Choosing a project
                clear_console(0)
                my_project = Project(projects_as_leader_list[ch - 1]["project_title"],
                                     projects_as_leader_list[ch - 1]["project_id"], user_obj)
                my_project.tasks = projects_as_leader_list[ch - 1]["tasks"]
                return my_project

            elif it_member > 0 and it_leader < ch <= (it_member + it_leader):  # Valid choice: Choosing a project
                clear_console(0)
                with open(projects_file_path, "r") as f:
                    all_projects = json.load(f)

                for it in range(len(all_projects)):
                    if all_projects[it]["project_id"] == projects_as_member_list[ch - it_leader - 1]["project_id"]:
                        leader_username = all_projects[it]["leader"]
                        with open(user_file_path, "r") as f_1:
                            all_users = json.load(f_1)

                        for iterate in range(len(all_users)):
                            if all_users[iterate]["username"] == leader_username:
                                leader_dict = all_users[iterate]
                                leader_obj = User(leader_dict["email"],
                                                  leader_dict["username"], leader_dict["password"])

                                my_project = Project(projects_as_member_list[ch - it_leader - 1]["project_title"],
                                                     projects_as_member_list[ch - it_leader - 1]["project_id"],
                                                     leader_obj)
                                my_project.tasks = all_projects[it]["tasks"]
                                return my_project

                        with open(admin_file_path, "r") as f_1:
                            admin_list_1 = json.load(f_1)

                        if admin_list_1[0]["username"] == leader_username:
                            leader_dict = admin_list_1[0]
                            leader_obj = User(leader_dict["email"],
                                              leader_dict["username"], leader_dict["password"])
                            my_project = Project(projects_as_member_list[ch - it_leader - 1]["project_title"],
                                                 projects_as_member_list[ch - it_leader - 1]["project_id"], leader_obj)
                            my_project.tasks = projects_as_member_list[ch - it_leader - 1]["tasks"]
                            return my_project


def options_for_my_project(user: User, my_project: Project):  # Called in the main program in the 2nd menu
    clear_console(2)
    ch = "-1"  # 1. Members  2. Tasks  3. Delete project  4. Back
    while ch != "0":
        clear_console(1)
        pr_cyan(f"{my_project.get_project_title()}"" project")
        print("1. Members\n2. Tasks\n3. Delete project\n4. Back")
        ch = input("Enter your choice: ")

        if ch == "1":  # 1. Members
            my_project_members(user, my_project)

        elif ch == "2":  # 2. Tasks
            user, my_project = tasks.show_tasks_and_options(user, my_project)

        elif ch == "3":  # 3. Delete project
            project_title = my_project.get_project_title()
            user, my_project = delete_project(user, my_project)  # Delete project
            if my_project.get_project_id() == "":
                log_info(f"Project {project_title} has been deleted!")
                pr_green(f"Project {project_title} has been deleted!")
            print("Going Back...")
            clear_console(2)
            return user, my_project

        elif ch == "4":  # 4. Back
            print("Going Back...")
            clear_console(2)
            return user, my_project

        else:
            pr_red("Error: Invalid choice! Please try again.")


def activate_users(users_list: [dict]):
    true_bool = True
    inactive_users = []
    for iterate in range(len(users_list)):
        if users_list[iterate]["is_active"] == true_bool:
            pass
        else:
            inactive_users.append(users_list[iterate])
    if len(inactive_users) == 0:
        print("    No inactive users.")
        print("    Going back...")
        clear_console(3)
        return
    else:
        which_user = 0
        while which_user < 1 or which_user > (len(inactive_users) + 1):
            clear_console(2)
            print("Choose a user to activate their account:")
            for iterate in range(len(inactive_users)):
                pr_cyan(f"{iterate + 1}. {inactive_users[iterate]["username"]}")
            print(f" {len(inactive_users) + 1}. Back")
            try:
                which_user = int(input())
            except ValueError:
                pr_red("Error: Invalid choice! Please try again.")
                which_user = 0
            else:
                if isinstance(which_user, int) and 0 < which_user <= len(inactive_users):
                    this_username = inactive_users[which_user - 1]["username"]
                    for iterate in range(len(users_list)):
                        if users_list[iterate]["username"] == this_username:
                            users_list[iterate]["is_active"] = true_bool

                    save_projects_to_file(user_file_path, users_list)
                    log_info(f"{this_username}'s account has been activated.")
                    pr_green(f"{this_username}'s account has been activated.")
                    print("Going back...")
                    clear_console(3)

                elif isinstance(which_user, int) and which_user == len(inactive_users) + 1:
                    print("Going back...")
                    clear_console(2)

                else:
                    pr_red("Error: Invalid choice! Please try again.")
                    which_user = 0


def deactivate_users(users_list: [dict]):
    true_bool = True
    active_users = []
    for iterate in range(len(users_list)):
        if users_list[iterate]["is_active"] != true_bool:
            pass
        else:
            active_users.append(users_list[iterate])
    if len(active_users) == 0:
        print("    No active users.")
        print("    Going back...")
        clear_console(3)
        return
    else:
        which_user = 0
        while which_user < 1 or which_user > (len(active_users) + 1):
            clear_console(2)
            print("Choose a user to deactivate their account:")
            for iterate in range(len(active_users)):
                pr_cyan(f"{iterate + 1}. {active_users[iterate]['username']}")
            print(f" {len(active_users) + 1}. Back")
            try:
                which_user = int(input())
            except ValueError:
                pr_red("Error: Invalid choice! Please try again.")
                which_user = 0
            else:
                if isinstance(which_user, int) and 0 < which_user <= len(active_users):
                    this_username = active_users[which_user - 1]["username"]
                    for iterate in range(len(users_list)):
                        if users_list[iterate]["username"] == this_username:
                            users_list[iterate]["is_active"] = False

                    save_projects_to_file(user_file_path, users_list)
                    log_info(f"{this_username}'s account has been deactivated.")
                    pr_green(f"{this_username}'s account has been deactivated.")
                    print("Going back...")
                    clear_console(3)

                elif isinstance(which_user, int) and which_user == len(active_users) + 1:
                    print("Going back...")
                    clear_console(2)

                else:
                    pr_red("Error: Invalid choice! Please try again.")
                    which_user = 0


def my_project_members(user: User, my_project: Project):
    ch = "0"
    while ch != "1" or ch != "2" or ch != "3":  # 1. Add members  2. Remove members  3. Back
        os.system("cls")
        print(f"\nMembers of project {my_project.get_project_title()}:")
        this_project = dict
        with open(projects_file_path, "r") as f:
            all_projects = json.load(f)
        project_members = []
        for it in range(len(all_projects)):
            if all_projects[it]["project_id"] == my_project.get_project_id():
                project_members = all_projects[it]["members"]
        my_project.members = project_members

        if len(project_members) == 0:
            pr_cyan("    No members")

        elif len(all_projects) > 0:
            for iterate in range(len(all_projects)):
                if all_projects[iterate]["project_id"] == my_project.get_project_id():
                    for it in range(len(all_projects[iterate]["members"])):
                        pr_cyan(all_projects[iterate]["members"][it])

        else:
            print("    No projects")

        print("\n1. Add members\n2. Remove members\n3. Back")
        ch = input("Enter your choice: ")

        if ch == "1":  # 1. Add members
            is_leader = False
            for iterate in range(len(user.projects_as_leader)):
                if user.projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                    user, my_project = add_members(user, my_project)
                    is_leader = True
                    break

            if not is_leader:
                clear_console(0)
                log_error(f"As a member of project {my_project.get_project_title()},"
                          f" you can not add any members to it.")
                pr_red(f"As a member of project {my_project.get_project_title()},"
                       f" you can not add any members to it.")
                print("Going Back...")
                clear_console(2)

        elif ch == "2":  # 2. Remove members
            is_leader = False
            for iterate in range(len(user.projects_as_leader)):
                if user.projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                    user, my_project = remove_members(user, my_project)
                    is_leader = True
                    break

            if not is_leader:
                clear_console(0)
                log_error(f"As a member of project {my_project.get_project_title()},"
                          f" you can not remove any members from it.")
                pr_red(f"As a member of project {my_project.get_project_title()},"
                       f" you can not remove any members from it.")
                print("Going Back...")
                clear_console(2)

        elif ch == "3":  # 3. Back
            print("Going Back...")
            clear_console(2)
            return user, my_project
        
        else:
            pr_red("Error: Invalid choice! Please try again.")
            clear_console(2)


def add_members(leader: User, my_project: Project):
    ch = "-1"
    while ch != "0":
        clear_console(2)
        project_members = my_project.members
        adding_possible = []

        with open(user_file_path, "r") as read_file:
            user_list = json.load(read_file)

        with open(admin_file_path, "r") as read_admin:
            admin_list_1 = json.load(read_admin)

        if len(user_list) > 0:
            for iterate in range(len(user_list)):
                if user_list[iterate]["username"] not in project_members:
                    if user_list[iterate]["username"] != leader.username:
                        adding_possible.append(user_list[iterate]["username"])
            if not isinstance(leader, Admin):
                if len(admin_list_1) > 0:
                    if admin_list_1[0]["username"] not in project_members:
                        adding_possible.append(admin_list_1[0]["username"])

            if len(adding_possible) > 0:
                print(f"Choose one of the following users to add them"
                      f" to project {my_project.get_project_title()}:")
                for iterate in range(len(adding_possible)):
                    pr_cyan(f"    {iterate + 1}. {adding_possible[iterate]}")
                print(f"     {len(adding_possible) + 1}. Back")
                try:
                    ch = int(input())
                except ValueError:
                    pr_red("Error: Invalid choice! Please try again.")
                else:
                    if isinstance(ch, int) and 1 <= ch <= (len(adding_possible)):
                        username_to_add = adding_possible[ch - 1]
                        # Adding user to member list + adding project to projects_as_member list
                        project_members.append(username_to_add)
                        my_project.members = project_members  # Updating the object
                        # Saving the new members list to 'projects.json' file
                        with open(projects_file_path, "r") as read_projects:
                            all_projects = json.load(read_projects)
                        if len(all_projects) > 0:
                            for iterate in range(len(all_projects)):
                                if all_projects[iterate]["project_id"] == my_project.get_project_id():
                                    all_projects[iterate]["members"] = project_members

                            with open(projects_file_path, "w") as write:  # Updating the projects file
                                json.dump(all_projects, write, indent=4)

                            if username_to_add in project_members:
                                for iterate in range(len(all_projects)):
                                    if all_projects[iterate]["project_id"] == my_project.get_project_id():
                                        the_project_dict = all_projects[iterate]

                                        for it in range(len(user_list)):
                                            # Adding project for the new member in file 'user.json'
                                            if user_list[it]["username"] == username_to_add:
                                                user_list[it]["projects_as_member"].append(the_project_dict)
                                                with open(user_file_path, "w") as write:
                                                    json.dump(user_list, write, indent=4)
                                            # Updating project's members for the leader in file 'user.json'
                                            if user_list[it]["username"] == leader.username:
                                                leader_projects_as_leader = user_list[it]["projects_as_leader"]
                                                for i in range(len(leader_projects_as_leader)):
                                                    if (leader_projects_as_leader[i]["project_id"] ==
                                                            my_project.get_project_id()):
                                                        leader_projects_as_leader[i]["members"] = my_project.members
                                            # Updating project's members for other members in file 'user.json'
                                            projects_as_member = user_list[it]["projects_as_member"]
                                            if projects_as_member:
                                                for i in range(len(projects_as_member)):
                                                    if (projects_as_member[i]["project_id"]
                                                            == my_project.get_project_id()):
                                                        projects_as_member[i]["members"] = my_project.members
                                                user_list[it]["projects_as_member"] = projects_as_member

                                            with open(user_file_path, "w") as f:
                                                json.dump(user_list, f, indent=4)

                                        # Three cases concerning the admin: 1. Admin is the new member
                                        # 2. Admin is the leader 3. Admin is merely a member of the project
                                        if admin_list_1:  # 1. Admin is the new member
                                            projects_as_member = admin_list_1[0]["projects_as_member"]
                                            if projects_as_member:
                                                for i in range(len(projects_as_member)):
                                                    if (projects_as_member[i]["project_id"]
                                                            == my_project.get_project_id()):
                                                        projects_as_member[i]["members"] = my_project.members

                                                admin_list_1[0]["projects_as_member"] = projects_as_member
                                            if admin_list_1[0]["username"] == username_to_add:
                                                admin_list_1[0]["projects_as_member"].append(all_projects[iterate])

                                            # 2. Admin is the leader
                                            if admin_list_1[0]["username"] == leader.username:
                                                leader_projects_as_leader = admin_list_1[0]["projects_as_leader"]
                                                if leader_projects_as_leader:
                                                    for i in range(len(leader_projects_as_leader)):
                                                        if (leader_projects_as_leader[i]["project_id"] ==
                                                                my_project.get_project_id()):
                                                            leader_projects_as_leader[i]["members"] = my_project.members
                                                    admin_list_1[0]["projects_as_leader"] = leader_projects_as_leader
                                                admin_list_1[0]["projects_as_member"] = projects_as_member

                                            with open(admin_file_path, "w") as write:
                                                json.dump(admin_list_1, write, indent=4)
                                        break  # Break the loop after finding the unique project from file

                        adding_possible.pop(ch - 1)
                        return leader, my_project
                    elif isinstance(ch, int) and ch == len(adding_possible) + 1:
                        print("Going back...")
                        clear_console(2)
                        return leader, my_project
                    else:
                        pr_red("Error: Invalid choice! Please try again.")
                        ch = "-1"

            else:
                print("    No users to add")
                clear_console(2)
                return leader, my_project

        else:
            print("    No users to add")
            clear_console(2)
            return leader, my_project


def remove_members(leader: User, my_project: Project):
    ch = "-1"
    while ch != "0":
        with open(projects_file_path, "r") as f:
            all_projects = json.load(f)

        with open(user_file_path, "r") as f:
            all_users = json.load(f)

        with open(admin_file_path, "r") as f:
            admin_list_1 = json.load(f)
        clear_console(1)
        print(f"Choose one of the following members to remove them"
              f" from project {my_project.get_project_title()}:")

        if len(my_project.members) > 0:
            for iterate in range(len(my_project.members)):
                pr_cyan(f"    {iterate + 1}. {my_project.members[iterate]}")
            print(f"     {len(my_project.members) + 1}. Back")

            try:
                choice = int(input())
            except ValueError:
                pr_red("Error: Invalid choice! Please try again.")
            else:
                if isinstance(choice, int) and 1 <= choice <= (len(my_project.members)):
                    username_to_remove = my_project.members[choice - 1]
                    # Updating the project object
                    my_project.members.pop(my_project.members.index(username_to_remove))
                    # Remove the user from the project's members (projects.json)
                    for it in range(len(all_projects)):
                        if all_projects[it]["project_id"] == my_project.get_project_id():
                            all_projects[it]["members"] = my_project.members
                            break
                    with open(projects_file_path, "w") as f:
                        json.dump(all_projects, f, indent=4)
                    # Updating leader's object
                    for it in range(len(leader.projects_as_leader)):
                        if leader.projects_as_leader[it]["project_id"] == my_project.get_project_id():
                            leader.projects_as_leader[it]["members"] = my_project.members
                            break
                    # Implementing changes in 'user.json'
                    for it in range(len(all_users)):
                        if all_users[it]["username"] == username_to_remove:  # Updating the removed member in file
                            user_projects_as_member = all_users[it]["projects_as_member"]
                            for iterate in range(len(user_projects_as_member)):
                                if user_projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                                    user_projects_as_member.pop(iterate)
                                    all_users[it]["projects_as_member"] = user_projects_as_member
                                    break

                        if all_users[it]["username"] == leader.username:  # Updating the leader in file
                            leader_projects_as_leader = all_users[it]["projects_as_leader"]
                            for iterate in range(len(leader_projects_as_leader)):
                                if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                                    leader_projects_as_leader[iterate]["members"] = my_project.members
                                    all_users[it]["projects_as_leader"] = leader_projects_as_leader
                                    break
                        projects_as_member = all_users[it]["projects_as_member"]
                        if projects_as_member:
                            for i in range(len(projects_as_member)):  # Updating other members
                                if projects_as_member[i]["project_id"] == my_project.get_project_id():
                                    projects_as_member[i]["members"] = my_project.members
                                    all_users[it]["projects_as_member"] = projects_as_member
                                    break

                    # Three cases concerning the admin: 1. Admin is the removed member
                    # 2. Admin is the leader 3. Admin is merely a member of the project
                    if admin_list_1:
                        projects_as_member = admin_list_1[0]["projects_as_member"]
                        if admin_list_1[0]["username"] == username_to_remove:  # 1. Admin is the removed member
                            for iterate in range(len(projects_as_member)):
                                if projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                                    projects_as_member.pop(iterate)
                                    admin_list_1[0]["projects_as_member"] = projects_as_member
                                    break

                        if admin_list_1[0]["username"] == leader.username:  # 2. Admin is the leader
                            leader_projects_as_leader = admin_list_1[0]["projects_as_leader"]
                            for iterate in range(len(leader_projects_as_leader)):
                                if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                                    leader_projects_as_leader[iterate]["members"] = my_project.members
                                    admin_list_1[0]["projects_as_leader"] = leader_projects_as_leader
                                    break

                        if projects_as_member:  # 3. Admin is merely a member of the project
                            for iterate in range(len(projects_as_member)):
                                if projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                                    projects_as_member[iterate]["members"] = my_project.members
                                    admin_list_1[0]["projects_as_member"] = projects_as_member

                    with open(user_file_path, "w") as w:
                        json.dump(all_users, w, indent=4)

                    with open(admin_file_path, "w") as w:
                        json.dump(admin_list_1, w, indent=4)

                    clear_console(2)
                    return leader, my_project

                elif choice == len(my_project.members) + 1:  # Back
                    print("Going Back...")
                    clear_console(2)
                    return leader, my_project

                else:
                    pr_red("Error: Invalid choice! Please try again.")

        else:
            print("    No members to remove")
            clear_console(2)
            return leader, my_project


def delete_project(user: User, my_project: Project):
    clear_console(2)
    if user.username != my_project.leader_username:  # The user is not the leader
        log_info(f"As a member of project {my_project.get_project_title()}, you can not delete it!")
        pr_red(f"As a member of project {my_project.get_project_title()}, you can not delete it!")
        clear_console(2)
        return user, my_project
    else:  # The user is the leader
        ch = "0"
        while ch != "y" or ch != "Y" or ch != "n" or ch != "N":
            clear_console(2)
            print(f"Are you sure about deleting project {my_project.get_project_title()}?")
            ch = input("Enter y for yes and n for no: ")
            if ch == "n" or ch == "N":
                clear_console(2)
                return user, my_project
            elif ch == "y" or ch == "Y":
                # Updating leader object
                leader_projects_as_leader = user.projects_as_leader
                for iterate in range(len(leader_projects_as_leader)):
                    if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                        leader_projects_as_leader.pop(iterate)
                        user.projects_as_leader = leader_projects_as_leader
                        break

                # Removing project from projects file
                with open(projects_file_path, "r") as f:
                    all_projects = json.load(f)

                for iterate in range(len(all_projects)):
                    if all_projects[iterate]["project_id"] == my_project.get_project_id():
                        all_projects.pop(iterate)
                        with open(projects_file_path, "w") as f:
                            json.dump(all_projects, f, indent=4)
                        break

                # Implementing changes in 'user.json'
                with open(user_file_path, "r") as f:
                    all_users = json.load(f)

                for it in range(len(all_users)):
                    # Updating the leader in file
                    if all_users[it]["username"] == my_project.leader_username:
                        leader_projects_as_leader = all_users[it]["projects_as_leader"]
                        for iterate in range(len(leader_projects_as_leader)):
                            if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                                leader_projects_as_leader.pop(iterate)
                                all_users[it]["projects_as_leader"] = leader_projects_as_leader
                                break

                    # Updating other members of the project in file
                    projects_as_member = all_users[it]["projects_as_member"]
                    if projects_as_member:
                        for i in range(len(projects_as_member)):
                            if projects_as_member[i]["project_id"] == my_project.get_project_id():
                                projects_as_member.pop(i)
                                all_users[it]["projects_as_member"] = projects_as_member
                                break

                with open(user_file_path, "w") as w:
                    json.dump(all_users, w, indent=4)

                # Cases involving the admin
                with open(admin_file_path, "r") as f:
                    admin_list_1 = json.load(f)

                if admin_list_1:
                    # Admin is the leader
                    if admin_list_1[0]["username"] == my_project.leader_username:
                        leader_projects_as_leader = admin_list_1[0]["projects_as_leader"]
                        for iterate in range(len(leader_projects_as_leader)):
                            if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                                leader_projects_as_leader.pop(iterate)
                                admin_list_1[0]["projects_as_leader"] = leader_projects_as_leader
                                break

                    # Admin is merely a member of the project
                    projects_as_member = admin_list_1[0]["projects_as_member"]
                    if projects_as_member:
                        for iterate in range(len(projects_as_member)):
                            if projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                                projects_as_member.pop(iterate)
                                admin_list_1[0]["projects_as_member"] = projects_as_member

                    with open(admin_file_path, "w") as w:
                        json.dump(admin_list_1, w, indent=4)

                # Updating the project object
                my_project = Project("", "", User("", "", ""))
                return user, my_project

            else:
                pr_red("Error: Invalid choice! Please try again.")
