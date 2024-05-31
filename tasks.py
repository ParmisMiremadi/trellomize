import json
import uuid
from enum import Enum
from user import User
import time
from user import clear_console
from user import pr_red, pr_green, pr_cyan
from user import Admin
from rich.console import Console
from rich.table import Table


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

        with open(projects_file_path, "r") as file:
            projects_dicts = json.load(file)  # List of dictionaries
        projects_dicts.append(new_project_dict)
        with open(projects_file_path, "w") as file:
            json.dump(projects_dicts, file, indent=4)

        # Appending the new project to the object's projects_as_leader list
        leader.projects_as_leader.append(new_project_dict)

        # Save the new projects_as_leader list to file
        if isinstance(leader, Admin):  # Saving to 'admin.json'
            with open(admin_file_path, "r") as f:
                admin_list = json.load(f)
                for iterate in range(len(admin_list)):
                    if admin_list[iterate]["username"] == leader.username:
                        admin_list[iterate]["projects_as_leader"] = leader.projects_as_leader
            with open(admin_file_path, "w") as file:
                json.dump(admin_list, file, indent=4)

        else:  # Saving to 'user.json'
            with open(user_file_path, "r") as f:
                users_list = json.load(f)
                for iterate in range(len(users_list)):
                    if users_list[iterate]["username"] == leader.username:
                        users_list[iterate]["projects_as_leader"] = leader.projects_as_leader
            with open(user_file_path, "w") as file:
                json.dump(users_list, file, indent=4)

        return leader


user_file_path = "user.json"
projects_file_path = "projects.json"
admin_file_path = "admin.json"


class Priority(str, Enum):
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH",
    CRITICAL = "CRITICAL"


class Status(str, Enum):
    BACKLOG = "BACKLOG",
    TODO = "TODO",
    DOING = "DOING",
    DONE = "DONE",
    ARCHIVED = "ARCHIVED"


class Task:
    def __init__(self, my_project: Project):
        self.project_id = my_project.get_project_id()
        self.__task_id = str(uuid.uuid1())
        self.task_title = ""
        self.description = ""
        self.start_date = time.ctime(time.time())
        self.due_date = time.ctime(time.time() + 24 * 60 * 60)
        self.assignees = []
        self.priority = Priority.LOW
        self.status = Status.BACKLOG
        self.comments = []

    def get_task_id(self):
        return self.__task_id

    def set_task_id(self, task_id):
        self.__task_id = task_id

    def to_dict_and_save_to_file(self, my_project: Project):  # Returns my_project after updates
        new_task_dict = {
            "task_id": self.__task_id,
            "task_title": self.task_title,
            "description": self.description,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "assignees": self.assignees,
            "priority": self.priority,
            "status": self.status,
            "comments": self.comments  # List of tuples
        }

        # Updating the project object
        my_project.tasks.append(new_task_dict)

        # Saving task in 'projects.json'
        with open(projects_file_path, "r") as f:
            all_projects = json.load(f)

        for it in range(len(all_projects)):
            if all_projects[it]["project_id"] == self.project_id:
                print("tasks before: ", all_projects[it]["tasks"])  #.
                all_projects[it]["tasks"] = my_project.tasks
                print("tasks after: ", all_projects[it]["tasks"])  #.
                break

        with open(projects_file_path, "w") as f:
            json.dump(all_projects, f, indent=4)

        # Updating the project in 'user.json'
        with open(user_file_path, "r") as f:
            all_users = json.load(f)

        for it in range(len(all_users)):
            # Updating the project for the leader of the project
            if all_users[it]["username"] == my_project.leader_username:
                leader_projects_as_leader = all_users[it]["projects_as_leader"]
                for iterate in range(len(leader_projects_as_leader)):
                    if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                        leader_projects_as_leader[iterate]["tasks"] = my_project.tasks
                        break

            # Updating the project for the members of the project
            projects_as_member = all_users[it]["projects_as_member"]
            if projects_as_member:
                for i in range(len(projects_as_member)):
                    if projects_as_member[i]["project_id"] == my_project.get_project_id():
                        projects_as_member[i]["tasks"] = my_project.tasks
                all_users[it]["projects_as_member"] = projects_as_member

        with open(user_file_path, "w") as f:
            json.dump(all_users, f, indent=4)

        # Cases concerning the admin
        with open(admin_file_path, "r") as f:
            admin_list = json.load(f)

        if admin_list:
            # Admin is the leader of the project
            if admin_list[0]["username"] == my_project.leader_username:
                leader_projects_as_leader = admin_list[0]["projects_as_leader"]
                for iterate in range(len(leader_projects_as_leader)):
                    if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                        leader_projects_as_leader[iterate]["tasks"] = my_project.tasks
                        admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                        break
            # Admin is a member of the project
            projects_as_member = admin_list[0]["projects_as_member"]
            if projects_as_member:
                for iterate in range(len(projects_as_member)):
                    if projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                        projects_as_member[iterate]["tasks"] = my_project.tasks
                        admin_list[0]["projects_as_member"] = projects_as_member
                        break

            with open(admin_file_path, "w") as f:
                json.dump(admin_list, f, indent=4)

        return my_project


def create_a_task(my_project: Project):
    task = Task(my_project)
    return task


def show_tasks_and_options(user: User, my_project: Project):
    ch = "-1"  # New task   Back  ...table of tasks...
    while ch != "0":
        clear_console(2)
        all_tasks = my_project.tasks
        if all_tasks:
            backlog_tasks = []
            todo_tasks = []
            doing_tasks = []
            done_tasks = []
            archived_tasks = []

            for it in range(len(all_tasks)):
                if all_tasks[it]["status"] == "BACKLOG":
                    backlog_tasks.append(all_tasks[it])

                elif all_tasks[it]["status"] == "TODO":
                    todo_tasks.append(all_tasks[it])

                elif all_tasks[it]["status"] == "DOING":
                    doing_tasks.append(all_tasks[it])

                elif all_tasks[it]["status"] == "DONE":
                    done_tasks.append(all_tasks[it])

                elif all_tasks[it]["status"] == "ARCHIVED":
                    archived_tasks.append(all_tasks[it])

            # Table of the project's tasks
            table = Table(title=f"IDs of tasks in project {my_project.get_project_title()}:")
            table.add_column("BACKLOG", justify="right", style="cyan", no_wrap=True)  #.
            table.add_column("TODO", style="magenta", no_wrap=True)  #.
            table.add_column("DOING", justify="right", style="green", no_wrap=True)  #.
            table.add_column("DONE", justify="right", style="cyan", no_wrap=True)  #.
            table.add_column("ARCHIVED", justify="right", style="magenta", no_wrap=True)  #.

            for it in range(max(len(backlog_tasks), len(todo_tasks),
                                len(doing_tasks), len(done_tasks), len(archived_tasks))):
                if it >= len(backlog_tasks):
                    backlog_tasks_id = ""
                else:
                    backlog_tasks_id = backlog_tasks[it]["task_id"][:8]

                if it >= len(todo_tasks):
                    todo_tasks_id = ""
                else:
                    todo_tasks_id = todo_tasks[it]["task_id"][:8]

                if it >= len(doing_tasks):
                    doing_tasks_id = ""
                else:
                    doing_tasks_id = doing_tasks[it]["task_id"][:8]

                if it >= len(done_tasks):
                    done_tasks_id = ""
                else:
                    done_tasks_id = done_tasks[it]["task_id"][:8]

                if it >= len(archived_tasks):
                    archived_tasks_id = ""
                else:
                    archived_tasks_id = archived_tasks[it]["task_id"][:8]

                table.add_row(f"{backlog_tasks_id}", f"{todo_tasks_id}",
                              f"{doing_tasks_id}", f"{done_tasks_id}",
                              f"{archived_tasks_id}")

            console = Console()
            console.print(table)

            print("\n1. New task\n2. Back")
            print("Enter the task's ID to see and change the details.")
            ch = input()

        else:
            print("    No tasks")

        print("1. New task\n2. Back")
        ch = input()
        if ch == "1":  # 1. New task
            if user.username == my_project.leader_username:
                my_task = create_a_task(my_project)  #.
                my_project = my_task.to_dict_and_save_to_file(my_project)
                pr_green("Task created successfully!")
                pr_green(f"task {my_task.get_task_id()} has been added to project {my_project.get_project_title()}.")
                clear_console(3)

            else:
                pr_red(f"As a member of project {my_project.get_project_title()}, You can not create a task!")
                print("Going Back...")
                clear_console(2)

        elif ch == "2":  # 2. Back
            print("Going Back...")
            clear_console(2)
            return user, my_project

        else:
            for it in range(len(all_tasks)):
                if ch == all_tasks[it]["task_id"][:8]:
                    my_task = Task(my_project)
                    my_task.set_task_id(all_tasks[it]["task_id"])
                    my_task.task_title = all_tasks[it]["task_title"]
                    my_task.description = all_tasks[it]["description"]
                    my_task.start_date = all_tasks[it]["start_date"]
                    my_task.due_date = all_tasks[it]["due_date"]
                    my_task.assignees = all_tasks[it]["assignees"]
                    my_task.priority = all_tasks[it]["priority"]
                    my_task.status = all_tasks[it]["status"]
                    my_task.comments = all_tasks[it]["comments"]

                    # To see and change the task's details:
                    user, my_project, my_task = task_details(user, my_project, my_task)

                    clear_console(2)
                    ch = "-1"
                    break

            if ch != "-1":
                pr_red("Error: Invalid value!")
                ch = "-1"


def task_details(user: User, my_project: Project, my_task: Task):
    ch = "-1"
    while ch != "0":
        print("        Task details")
        pr_cyan(f"    ID: {my_task.get_task_id()}")
        pr_cyan(f"    Title: {my_task.task_title}")
        pr_cyan(f"    Description: {my_task.description}")
        pr_cyan(f"    Start date: {my_task.start_date}")
        pr_cyan(f"    Due date: {my_task.due_date}")
        pr_cyan(f"    Assignees: ")
        if my_task.assignees:
            for it in range(len(my_task.assignees)):
                pr_cyan(f"        {my_task.assignees[it]}")
        pr_cyan(f"    Priority: {my_task.priority}")
        pr_cyan(f"    Status: {my_task.status}")
        pr_cyan(f"    Comments: ")
        if my_task.comments:
            for iterate in range(len(my_task.comments)):
                pr_cyan(f"        {my_task.comments[iterate]["comment"]}")
                pr_cyan(f"      By: {my_task.comments[iterate]["username"]}")
                pr_cyan(f"      Date:{my_task.comments[iterate]["date"]}")

        print("\n1. Change details\n2. Back")
        ch = input()
        if ch == "1":  # 1. Change details
            if user.username == my_project.leader_username or (user.username in my_task.assignees):
                user, my_project, my_task = change_task_details(user, my_project, my_task)
            else:
                pr_red("As neither the leader of this project nor an "
                       "assignee of the task, you can not change its details.")
                clear_console(2)
                ch = "-1"

        elif ch == "2":  # 2. Back
            print("Going Back...")
            clear_console(2)
            return user, my_project, my_task


#############################################
# Changing task details
# 1. Title
def change_title(title, user: User, my_project: Project, my_task: Task):
    pr_green(f"The title of the task (ID: {my_task.get_task_id()})\n has been changed to {title}.")
    # Updating Task object
    my_task.task_title = title
    # Updating Project object
    all_tasks = my_project.tasks
    for iterate in range(len(all_tasks)):
        if all_tasks[iterate]["task_id"] == my_task.get_task_id():
            all_tasks[iterate]["task_title"] = my_task.task_title
            break
    # Updating User object
    if user.username == my_project.leader_username:
        for iterate in range(len(user.projects_as_leader)):
            project_tasks = user.projects_as_leader[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["task_title"] = my_task.task_title
                        break

    else:
        for iterate in range(len(user.projects_as_member)):
            project_tasks = user.projects_as_member[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["task_title"] = my_task.task_title
                        break
    # Updating 'projects.json' file
    with open(projects_file_path, "r") as read_projects:
        all_projects = json.load(read_projects)
    for iterate in range(len(all_projects)):
        if all_projects[iterate]["project_id"] == my_project.get_project_id():
            project_tasks = all_projects[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["task_title"] = my_task.task_title
                        all_projects[iterate]["tasks"] = project_tasks
                        break
    with open(projects_file_path, "w") as write:  # Updating the projects file
        json.dump(all_projects, write, indent=4)

    # Updating the project in 'user.json' file (leader + members)
    with open(user_file_path, "r") as read_file:
        user_list = json.load(read_file)

    # Updating the leader in file
    for iterate in range(len(user_list)):
        if user_list[iterate]["username"] == my_project.leader_username:
            leader_projects_as_leader = user_list[iterate]["projects_as_leader"]
            for it in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[it]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[it]["tasks"]
                    for i in range(len(project_tasks)):
                        if project_tasks[i]["task_id"] == my_task.get_task_id():
                            project_tasks[i]["task_title"] = my_task.task_title
                            leader_projects_as_leader[it]["tasks"] = project_tasks
                            user_list[iterate]["projects_as_leader"] = leader_projects_as_leader
                            break
        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if user_list[iterate]["username"] in project_members:  # Updating the members in file
                    print(" IS IN MEMBERS")  #.
                    member_projects_as_member = user_list[iterate]["projects_as_member"]
                    for it in range(len(member_projects_as_member)):
                        if member_projects_as_member[it]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[it]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["task_title"] = my_task.task_title
                                    member_projects_as_member[it]["tasks"] = project_tasks
                                    user_list[iterate]["projects_as_member"] = member_projects_as_member
                                    break

    with open(user_file_path, "w") as f:
        json.dump(user_list, f, indent=4)

    # Updating the project in 'admin.json' file (if leader or if member)
    with open(admin_file_path, "r") as f:
        admin_list = json.load(f)

    if admin_list:
        if admin_list[0]["username"] == my_project.leader_username:  # Admin is the leader
            leader_projects_as_leader = admin_list[0]["projects_as_leader"]
            for iterate in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[iterate]["tasks"]
                    for it in range(len(project_tasks)):
                        if project_tasks[it]["task_id"] == my_task.get_task_id():
                            project_tasks[it]["task_title"] = my_task.task_title
                            leader_projects_as_leader[iterate]["tasks"] = project_tasks
                            admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                            break

        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if admin_list[0]["username"] in project_members:  # Admin is a member
                    member_projects_as_member = admin_list[0]["projects_as_member"]
                    for iterate in range(len(member_projects_as_member)):
                        if member_projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[iterate]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["task_title"] = my_task.task_title
                                    member_projects_as_member[iterate]["tasks"] = project_tasks
                                    admin_list[0]["projects_as_member"] = member_projects_as_member
                                    break
        with open(admin_file_path, "w") as write:
            json.dump(admin_list, write, indent=4)
    clear_console(2)
    return user, my_project, my_task


# 2. Description
def change_description(description, user: User, my_project: Project, my_task: Task):
    pr_green(f"The description of the task (ID: {my_task.get_task_id()})\n has been changed to: {description}.")
    # Updating Task object
    my_task.description = description
    # Updating Project object
    all_tasks = my_project.tasks
    for iterate in range(len(all_tasks)):
        if all_tasks[iterate]["task_id"] == my_task.get_task_id():
            all_tasks[iterate]["description"] = my_task.description
            break
    # Updating User object
    if user.username == my_project.leader_username:
        for iterate in range(len(user.projects_as_leader)):
            project_tasks = user.projects_as_leader[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["description"] = my_task.description
                        break

    else:
        for iterate in range(len(user.projects_as_member)):
            project_tasks = user.projects_as_member[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["description"] = my_task.description
                        break
    # Updating 'projects.json' file
    with open(projects_file_path, "r") as read_projects:
        all_projects = json.load(read_projects)
    for iterate in range(len(all_projects)):
        if all_projects[iterate]["project_id"] == my_project.get_project_id():
            project_tasks = all_projects[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["description"] = my_task.description
                        all_projects[iterate]["tasks"] = project_tasks
                        break
    with open(projects_file_path, "w") as write:  # Updating the projects file
        json.dump(all_projects, write, indent=4)

    # Updating the project in 'user.json' file (leader + members)
    with open(user_file_path, "r") as read_file:
        user_list = json.load(read_file)

    # Updating the leader in file
    for iterate in range(len(user_list)):
        if user_list[iterate]["username"] == my_project.leader_username:
            leader_projects_as_leader = user_list[iterate]["projects_as_leader"]
            for it in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[it]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[it]["tasks"]
                    for i in range(len(project_tasks)):
                        if project_tasks[i]["task_id"] == my_task.get_task_id():
                            project_tasks[i]["description"] = my_task.description
                            leader_projects_as_leader[it]["tasks"] = project_tasks
                            user_list[iterate]["projects_as_leader"] = leader_projects_as_leader
                            break
        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if user_list[iterate]["username"] in project_members:  # Updating the members in file
                    member_projects_as_member = user_list[iterate]["projects_as_member"]
                    for it in range(len(member_projects_as_member)):
                        if member_projects_as_member[it]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[it]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["description"] = my_task.description
                                    member_projects_as_member[it]["tasks"] = project_tasks
                                    user_list[iterate]["projects_as_member"] = member_projects_as_member
                                    break

    with open(user_file_path, "w") as f:
        json.dump(user_list, f, indent=4)

    # Updating the project in 'admin.json' file (if leader or if member)
    with open(admin_file_path, "r") as f:
        admin_list = json.load(f)

    if admin_list:
        if admin_list[0]["username"] == my_project.leader_username:  # Admin is the leader
            leader_projects_as_leader = admin_list[0]["projects_as_leader"]
            for iterate in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[iterate]["tasks"]
                    for it in range(len(project_tasks)):
                        if project_tasks[it]["task_id"] == my_task.get_task_id():
                            project_tasks[it]["description"] = my_task.description
                            leader_projects_as_leader[iterate]["tasks"] = project_tasks
                            admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                            break

        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if admin_list[0]["username"] in project_members:  # Admin is a member
                    member_projects_as_member = admin_list[0]["projects_as_member"]
                    for iterate in range(len(member_projects_as_member)):
                        if member_projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[iterate]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["description"] = my_task.description
                                    member_projects_as_member[iterate]["tasks"] = project_tasks
                                    admin_list[0]["projects_as_member"] = member_projects_as_member
                                    break
        with open(admin_file_path, "w") as write:
            json.dump(admin_list, write, indent=4)
    clear_console(2)
    return user, my_project, my_task


# 3. Add assignees
def add_assignees(user: User, my_project: Project, my_task: Task):
    ch = -1
    while ch != 0:
        assignee_possible = []
        with open(projects_file_path, "r") as f:
            all_projects = json.load(f)
        for iterate in range(len(all_projects)):
            if all_projects[iterate]["project_id"] == my_project.get_project_id():
                if all_projects[iterate]["members"]:
                    for it in range(len(all_projects[iterate]["members"])):
                        if all_projects[iterate]["members"][it] not in my_task.assignees:
                            assignee_possible.append(all_projects[iterate]["members"][it])

                    if assignee_possible:
                        for it in range(len(assignee_possible)):
                            print(f"    {it + 1}. {assignee_possible[it]}")
                        print(f"    {len(assignee_possible) + 1}. Back")
                        try:
                            ch = int(input("Enter a number to add an assignee to the task, or to go back: "))

                        except ValueError:
                            clear_console(1)
                            pr_red("Error: Invalid value!")
                            clear_console(2.5)

                        else:
                            if isinstance(ch, int) and (ch < 1 or ch > len(assignee_possible) + 1):
                                pr_red("Error: Invalid value!")
                                clear_console(2)

                            elif ch == len(assignee_possible) + 1:  # Going back
                                print("Going back...")
                                clear_console(2)
                                return user, my_project, my_task

                            elif isinstance(ch, int) and 1 <= ch <= len(assignee_possible):
                                username_to_add = assignee_possible[ch - 1]
                                pr_green(f"username_to_add: {username_to_add}")  #.
                                pr_green(f"A new assignee (username: {username_to_add}) has been added "
                                         f"to the task (task ID: {my_task.get_task_id()}).")
                                # Updating Task object
                                my_task.assignees.append(username_to_add)
                                # Updating Project object
                                all_tasks = my_project.tasks
                                for iterate_1 in range(len(all_tasks)):
                                    if all_tasks[iterate_1]["task_id"] == my_task.get_task_id():
                                        all_tasks[iterate_1]["assignees"] = my_task.assignees
                                        break
                                # Updating User object
                                if user.username == my_project.leader_username:
                                    for iterate_1 in range(len(user.projects_as_leader)):
                                        project_tasks = user.projects_as_leader[iterate_1]["tasks"]
                                        if project_tasks:
                                            for it_1 in range(len(project_tasks)):
                                                if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                                    project_tasks[it_1]["assignees"] = my_task.assignees
                                                    break

                                else:
                                    for iterate_1 in range(len(user.projects_as_member)):
                                        project_tasks = user.projects_as_member[iterate_1]["tasks"]
                                        if project_tasks:
                                            for it_1 in range(len(project_tasks)):
                                                if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                                    project_tasks[it_1]["assignees"] = my_task.assignees
                                                    break
                                # Updating 'projects.json' file
                                with open(projects_file_path, "r") as read_projects:
                                    all_projects = json.load(read_projects)

                                for iterate_1 in range(len(all_projects)):
                                    if all_projects[iterate_1]["project_id"] == my_project.get_project_id():
                                        project_tasks = all_projects[iterate_1]["tasks"]
                                        if project_tasks:
                                            for it_1 in range(len(project_tasks)):
                                                if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                                    project_tasks[it_1]["assignees"] = my_task.assignees
                                                    all_projects[iterate_1]["tasks"] = project_tasks
                                                    break
                                with open(projects_file_path, "w") as write:  # Updating the projects file
                                    json.dump(all_projects, write, indent=4)

                                # Updating the project in 'user.json' file (leader + members)
                                with open(user_file_path, "r") as read_file:
                                    user_list = json.load(read_file)

                                # Updating the leader in file
                                for iterate_1 in range(len(user_list)):
                                    if user_list[iterate_1]["username"] == my_project.leader_username:
                                        leader_projects_as_leader = user_list[iterate_1]["projects_as_leader"]
                                        for it_1 in range(len(leader_projects_as_leader)):
                                            if (leader_projects_as_leader[it_1]["project_id"]
                                                    == my_project.get_project_id()):
                                                project_tasks = leader_projects_as_leader[it_1]["tasks"]
                                                for i in range(len(project_tasks)):
                                                    if project_tasks[i]["task_id"] == my_task.get_task_id():
                                                        project_tasks[i]["assignees"] = my_task.assignees
                                                        leader_projects_as_leader[it_1]["tasks"] = project_tasks
                                                        user_list[iterate_1][
                                                            "projects_as_leader"] = leader_projects_as_leader
                                                        break
                                    for item in range(len(all_projects)):
                                        if all_projects[item]["project_id"] == my_project.get_project_id():
                                            project_members = all_projects[item]["members"]
                                            # Updating the members in file
                                            if user_list[iterate_1]["username"] in project_members:
                                                member_projects_as_member = user_list[iterate_1]["projects_as_member"]
                                                for it_1 in range(len(member_projects_as_member)):
                                                    if (member_projects_as_member[it_1]["project_id"]
                                                            == my_project.get_project_id()):
                                                        project_tasks = member_projects_as_member[it_1]["tasks"]
                                                        for i in range(len(project_tasks)):
                                                            if project_tasks[i]["task_id"] == my_task.get_task_id():
                                                                project_tasks[i]["assignees"] = my_task.assignees
                                                                member_projects_as_member[it_1]["tasks"] = project_tasks
                                                                user_list[iterate_1][
                                                                    "projects_as_member"] = member_projects_as_member
                                                                break

                                with open(user_file_path, "w") as f:
                                    json.dump(user_list, f, indent=4)

                                # Updating the project in 'admin.json' file (if leader or if member)
                                with open(admin_file_path, "r") as f:
                                    admin_list = json.load(f)

                                if admin_list:
                                    if admin_list[0]["username"] == my_project.leader_username:  # Admin is the leader
                                        leader_projects_as_leader = admin_list[0]["projects_as_leader"]
                                        for iterate_1 in range(len(leader_projects_as_leader)):
                                            if (leader_projects_as_leader[iterate_1]["project_id"]
                                                    == my_project.get_project_id()):
                                                project_tasks = leader_projects_as_leader[iterate_1]["tasks"]
                                                for it_1 in range(len(project_tasks)):
                                                    if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                                        project_tasks[it_1]["assignees"] = my_task.assignees
                                                        leader_projects_as_leader[iterate_1]["tasks"] = project_tasks
                                                        admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                                                        break

                                    for item in range(len(all_projects)):
                                        if all_projects[item]["project_id"] == my_project.get_project_id():
                                            project_members = all_projects[item]["members"]
                                            if admin_list[0]["username"] in project_members:  # Admin is a member
                                                member_projects_as_member = admin_list[0]["projects_as_member"]
                                                for iterate_1 in range(len(member_projects_as_member)):
                                                    if (member_projects_as_member[iterate_1]["project_id"]
                                                            == my_project.get_project_id()):
                                                        project_tasks = member_projects_as_member[iterate_1]["tasks"]
                                                        for i in range(len(project_tasks)):
                                                            if project_tasks[i]["task_id"] == my_task.get_task_id():
                                                                project_tasks[i]["assignees"] = my_task.assignees
                                                                member_projects_as_member[iterate_1][
                                                                    "tasks"] = project_tasks
                                                                admin_list[0][
                                                                    "projects_as_member"] = member_projects_as_member
                                                                break
                                    with open(admin_file_path, "w") as write:
                                        json.dump(admin_list, write, indent=4)
                                assignee_possible.pop(ch - 1)
                                clear_console(2)
                                return user, my_project, my_task

                    else:
                        print("Every member of this project is already an assignee!")
                        print("Going back...")
                        clear_console(2)
                        return user, my_project, my_task

            else:
                print("    No members to add.")
                print("Going back...")
                clear_console(2)
                return user, my_project, my_task


def remove_assignees(user: User, my_project: Project, my_task: Task):
    ch = -1
    while ch != 0:
        print(f"Choose one of the following assignees to remove them from the task: ")

        if len(my_task.assignees) > 0:
            for iterate in range(len(my_task.assignees)):
                pr_cyan(f"    {iterate + 1}. {my_task.assignees[iterate]}")
            print(f"    {len(my_task.assignees) + 1}. Back")

            try:
                ch = int(input())
            except ValueError:
                pr_red("Error: Invalid value!")
            else:
                if isinstance(ch, int) and (ch < 1 or ch > len(my_task.assignees) + 1):
                    pr_red("Error: Invalid value!")
                    clear_console(2)

                elif ch == len(my_task.assignees) + 1:  # Going back
                    print("Going back...")
                    clear_console(2)
                    return user, my_project, my_task

                elif isinstance(ch, int) and 1 <= ch <= (len(my_task.assignees)):
                    username_to_remove = my_task.assignees[ch - 1]
                    pr_green(f"An assignee (username: {username_to_remove}) has been removed "
                             f"from the task (task ID: {my_task.get_task_id()}).")
                    # Updating Task object
                    my_task.assignees.pop(my_task.assignees.index(username_to_remove))
                    # Updating Project object
                    all_tasks = my_project.tasks
                    for iterate_1 in range(len(all_tasks)):
                        if all_tasks[iterate_1]["task_id"] == my_task.get_task_id():
                            all_tasks[iterate_1]["assignees"] = my_task.assignees
                            break
                    # Updating User object
                    if user.username == my_project.leader_username:
                        for iterate_1 in range(len(user.projects_as_leader)):
                            project_tasks = user.projects_as_leader[iterate_1]["tasks"]
                            if project_tasks:
                                for it_1 in range(len(project_tasks)):
                                    if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                        project_tasks[it_1]["assignees"] = my_task.assignees
                                        break

                    else:
                        for iterate_1 in range(len(user.projects_as_member)):
                            project_tasks = user.projects_as_member[iterate_1]["tasks"]
                            if project_tasks:
                                for it_1 in range(len(project_tasks)):
                                    if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                        project_tasks[it_1]["assignees"] = my_task.assignees
                                        break
                    # Updating 'projects.json' file
                    with open(projects_file_path, "r") as read_projects:
                        all_projects = json.load(read_projects)

                    for iterate_1 in range(len(all_projects)):
                        if all_projects[iterate_1]["project_id"] == my_project.get_project_id():
                            project_tasks = all_projects[iterate_1]["tasks"]
                            if project_tasks:
                                for it_1 in range(len(project_tasks)):
                                    if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                        project_tasks[it_1]["assignees"] = my_task.assignees
                                        all_projects[iterate_1]["tasks"] = project_tasks
                                        break
                    with open(projects_file_path, "w") as write:  # Updating the projects file
                        json.dump(all_projects, write, indent=4)

                    # Updating the project in 'user.json' file (leader + members)
                    with open(user_file_path, "r") as read_file:
                        user_list = json.load(read_file)

                    # Updating the leader in file
                    for iterate_1 in range(len(user_list)):
                        if user_list[iterate_1]["username"] == my_project.leader_username:
                            leader_projects_as_leader = user_list[iterate_1]["projects_as_leader"]
                            for it_1 in range(len(leader_projects_as_leader)):
                                if (leader_projects_as_leader[it_1]["project_id"]
                                        == my_project.get_project_id()):
                                    project_tasks = leader_projects_as_leader[it_1]["tasks"]
                                    for i in range(len(project_tasks)):
                                        if project_tasks[i]["task_id"] == my_task.get_task_id():
                                            project_tasks[i]["assignees"] = my_task.assignees
                                            leader_projects_as_leader[it_1]["tasks"] = project_tasks
                                            user_list[iterate_1][
                                                "projects_as_leader"] = leader_projects_as_leader
                                            break
                        for item in range(len(all_projects)):
                            if all_projects[item]["project_id"] == my_project.get_project_id():
                                project_members = all_projects[item]["members"]
                                # Updating the members in file
                                if user_list[iterate_1]["username"] in project_members:
                                    member_projects_as_member = user_list[iterate_1]["projects_as_member"]
                                    for it_1 in range(len(member_projects_as_member)):
                                        if (member_projects_as_member[it_1]["project_id"]
                                                == my_project.get_project_id()):
                                            project_tasks = member_projects_as_member[it_1]["tasks"]
                                            for i in range(len(project_tasks)):
                                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                                    project_tasks[i]["assignees"] = my_task.assignees
                                                    member_projects_as_member[it_1]["tasks"] = project_tasks
                                                    user_list[iterate_1][
                                                        "projects_as_member"] = member_projects_as_member
                                                    break

                    with open(user_file_path, "w") as f:
                        json.dump(user_list, f, indent=4)

                    # Updating the project in 'admin.json' file (if leader or if member)
                    with open(admin_file_path, "r") as f:
                        admin_list = json.load(f)

                    if admin_list:
                        if admin_list[0]["username"] == my_project.leader_username:  # Admin is the leader
                            leader_projects_as_leader = admin_list[0]["projects_as_leader"]
                            for iterate_1 in range(len(leader_projects_as_leader)):
                                if (leader_projects_as_leader[iterate_1]["project_id"]
                                        == my_project.get_project_id()):
                                    project_tasks = leader_projects_as_leader[iterate_1]["tasks"]
                                    for it_1 in range(len(project_tasks)):
                                        if project_tasks[it_1]["task_id"] == my_task.get_task_id():
                                            project_tasks[it_1]["assignees"] = my_task.assignees
                                            leader_projects_as_leader[iterate_1]["tasks"] = project_tasks
                                            admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                                            break

                        for item in range(len(all_projects)):
                            if all_projects[item]["project_id"] == my_project.get_project_id():
                                project_members = all_projects[item]["members"]
                                if admin_list[0]["username"] in project_members:  # Admin is a member
                                    member_projects_as_member = admin_list[0]["projects_as_member"]
                                    for iterate_1 in range(len(member_projects_as_member)):
                                        if (member_projects_as_member[iterate_1]["project_id"]
                                                == my_project.get_project_id()):
                                            project_tasks = member_projects_as_member[iterate_1]["tasks"]
                                            for i in range(len(project_tasks)):
                                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                                    project_tasks[i]["assignees"] = my_task.assignees
                                                    member_projects_as_member[iterate_1][
                                                        "tasks"] = project_tasks
                                                    admin_list[0][
                                                        "projects_as_member"] = member_projects_as_member
                                                    break
                        with open(admin_file_path, "w") as write:
                            json.dump(admin_list, write, indent=4)
                    clear_console(2)
                    return user, my_project, my_task


# 5. Priority
def change_priority(priority, user: User, my_project: Project, my_task: Task):
    pr_green(f"The priority of the task (task ID: {my_task.get_task_id()})\n has been changed to: {priority}.")
    # Updating Task object
    my_task.priority = priority
    # Updating Project object
    all_tasks = my_project.tasks
    for iterate in range(len(all_tasks)):
        if all_tasks[iterate]["task_id"] == my_task.get_task_id():
            all_tasks[iterate]["priority"] = my_task.priority
            break
    # Updating User object
    if user.username == my_project.leader_username:
        for iterate in range(len(user.projects_as_leader)):
            project_tasks = user.projects_as_leader[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["priority"] = my_task.priority
                        break

    else:
        for iterate in range(len(user.projects_as_member)):
            project_tasks = user.projects_as_member[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["priority"] = my_task.priority
                        break
    # Updating 'projects.json' file
    with open(projects_file_path, "r") as read_projects:
        all_projects = json.load(read_projects)
    for iterate in range(len(all_projects)):
        if all_projects[iterate]["project_id"] == my_project.get_project_id():
            project_tasks = all_projects[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["priority"] = my_task.priority
                        all_projects[iterate]["tasks"] = project_tasks
                        break
    with open(projects_file_path, "w") as write:  # Updating the projects file
        json.dump(all_projects, write, indent=4)

    # Updating the project in 'user.json' file (leader + members)
    with open(user_file_path, "r") as read_file:
        user_list = json.load(read_file)

    # Updating the leader in file
    for iterate in range(len(user_list)):
        if user_list[iterate]["username"] == my_project.leader_username:
            leader_projects_as_leader = user_list[iterate]["projects_as_leader"]
            for it in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[it]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[it]["tasks"]
                    for i in range(len(project_tasks)):
                        if project_tasks[i]["task_id"] == my_task.get_task_id():
                            project_tasks[i]["priority"] = my_task.priority
                            leader_projects_as_leader[it]["tasks"] = project_tasks
                            user_list[iterate]["projects_as_leader"] = leader_projects_as_leader
                            break
        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if user_list[iterate]["username"] in project_members:  # Updating the members in file
                    member_projects_as_member = user_list[iterate]["projects_as_member"]
                    for it in range(len(member_projects_as_member)):
                        if member_projects_as_member[it]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[it]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["priority"] = my_task.priority
                                    member_projects_as_member[it]["tasks"] = project_tasks
                                    user_list[iterate]["projects_as_member"] = member_projects_as_member
                                    break

    with open(user_file_path, "w") as f:
        json.dump(user_list, f, indent=4)

    # Updating the project in 'admin.json' file (if leader or if member)
    with open(admin_file_path, "r") as f:
        admin_list = json.load(f)

    if admin_list:
        if admin_list[0]["username"] == my_project.leader_username:  # Admin is the leader
            leader_projects_as_leader = admin_list[0]["projects_as_leader"]
            for iterate in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[iterate]["tasks"]
                    for it in range(len(project_tasks)):
                        if project_tasks[it]["task_id"] == my_task.get_task_id():
                            project_tasks[it]["priority"] = my_task.priority
                            leader_projects_as_leader[iterate]["tasks"] = project_tasks
                            admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                            break

        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if admin_list[0]["username"] in project_members:  # Admin is a member
                    member_projects_as_member = admin_list[0]["projects_as_member"]
                    for iterate in range(len(member_projects_as_member)):
                        if member_projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[iterate]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["priority"] = my_task.priority
                                    member_projects_as_member[iterate]["tasks"] = project_tasks
                                    admin_list[0]["projects_as_member"] = member_projects_as_member
                                    break
        with open(admin_file_path, "w") as write:
            json.dump(admin_list, write, indent=4)
    clear_console(2)
    return user, my_project, my_task


# 6. Status
def change_status(status, user: User, my_project: Project, my_task: Task):
    pr_green(f"The status of the task (task ID: {my_task.get_task_id()})\n has been changed to: {status}.")
    # Updating Task object
    my_task.status = status
    # Updating Project object
    all_tasks = my_project.tasks
    for iterate in range(len(all_tasks)):
        if all_tasks[iterate]["task_id"] == my_task.get_task_id():
            all_tasks[iterate]["status"] = my_task.status
            break
    # Updating User object
    if user.username == my_project.leader_username:
        for iterate in range(len(user.projects_as_leader)):
            project_tasks = user.projects_as_leader[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["status"] = my_task.status
                        break

    else:
        for iterate in range(len(user.projects_as_member)):
            project_tasks = user.projects_as_member[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["status"] = my_task.status
                        break
    # Updating 'projects.json' file
    with open(projects_file_path, "r") as read_projects:
        all_projects = json.load(read_projects)
    for iterate in range(len(all_projects)):
        if all_projects[iterate]["project_id"] == my_project.get_project_id():
            project_tasks = all_projects[iterate]["tasks"]
            if project_tasks:
                for it in range(len(project_tasks)):
                    if project_tasks[it]["task_id"] == my_task.get_task_id():
                        project_tasks[it]["status"] = my_task.status
                        all_projects[iterate]["tasks"] = project_tasks
                        break
    with open(projects_file_path, "w") as write:  # Updating the projects file
        json.dump(all_projects, write, indent=4)

    # Updating the project in 'user.json' file (leader + members)
    with open(user_file_path, "r") as read_file:
        user_list = json.load(read_file)

    # Updating the leader in file
    for iterate in range(len(user_list)):
        if user_list[iterate]["username"] == my_project.leader_username:
            leader_projects_as_leader = user_list[iterate]["projects_as_leader"]
            for it in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[it]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[it]["tasks"]
                    for i in range(len(project_tasks)):
                        if project_tasks[i]["task_id"] == my_task.get_task_id():
                            project_tasks[i]["status"] = my_task.status
                            leader_projects_as_leader[it]["tasks"] = project_tasks
                            user_list[iterate]["projects_as_leader"] = leader_projects_as_leader
                            break
        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if user_list[iterate]["username"] in project_members:  # Updating the members in file
                    member_projects_as_member = user_list[iterate]["projects_as_member"]
                    for it in range(len(member_projects_as_member)):
                        if member_projects_as_member[it]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[it]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["status"] = my_task.status
                                    member_projects_as_member[it]["tasks"] = project_tasks
                                    user_list[iterate]["projects_as_member"] = member_projects_as_member
                                    break

    with open(user_file_path, "w") as f:
        json.dump(user_list, f, indent=4)

    # Updating the project in 'admin.json' file (if leader or if member)
    with open(admin_file_path, "r") as f:
        admin_list = json.load(f)

    if admin_list:
        if admin_list[0]["username"] == my_project.leader_username:  # Admin is the leader
            leader_projects_as_leader = admin_list[0]["projects_as_leader"]
            for iterate in range(len(leader_projects_as_leader)):
                if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():
                    project_tasks = leader_projects_as_leader[iterate]["tasks"]
                    for it in range(len(project_tasks)):
                        if project_tasks[it]["task_id"] == my_task.get_task_id():
                            project_tasks[it]["status"] = my_task.status
                            leader_projects_as_leader[iterate]["tasks"] = project_tasks
                            admin_list[0]["projects_as_leader"] = leader_projects_as_leader
                            break

        for item in range(len(all_projects)):
            if all_projects[item]["project_id"] == my_project.get_project_id():
                project_members = all_projects[item]["members"]
                if admin_list[0]["username"] in project_members:  # Admin is a member
                    member_projects_as_member = admin_list[0]["projects_as_member"]
                    for iterate in range(len(member_projects_as_member)):
                        if member_projects_as_member[iterate]["project_id"] == my_project.get_project_id():
                            project_tasks = member_projects_as_member[iterate]["tasks"]
                            for i in range(len(project_tasks)):
                                if project_tasks[i]["task_id"] == my_task.get_task_id():
                                    project_tasks[i]["status"] = my_task.status
                                    member_projects_as_member[iterate]["tasks"] = project_tasks
                                    admin_list[0]["projects_as_member"] = member_projects_as_member
                                    break
        with open(admin_file_path, "w") as write:
            json.dump(admin_list, write, indent=4)
    clear_console(2)
    return user, my_project, my_task


# 7. Add comment
# def add_comment(comment, user: User, my_project: Project, my_task: Task):  # The user is either the leader or an assignee
#

#########################################
#########################################
def change_task_details(user: User, my_project: Project, my_task: Task):
    ch = "-1"  # 1. Title  2. Description  3. Add assignees  4. Remove assignees
    while ch != "0":  # 5. Priority  6. Status 7. Add comment  8. Back
        print("What would you like to change in this task?")
        print("1. Title\n2. Description\n3. Add assignees\n4. Remove assignees")
        print("5. Priority\n6. Status\n7. Add comment\n8. Back")

        ch = input("Enter your choice: ")
        if ch == "1":  # 1. Title
            title = input("Enter the title of the task: ")
            user, my_project, my_task = change_title(title, user, my_project, my_task)
            clear_console(2)

        elif ch == "2":  # 2. Description
            description = input("Enter the description of the task: ")
            user, my_project, my_task = change_description(description, user, my_project, my_task)
            clear_console(2)

        elif ch == "3":  # 3. Add assignees
            user, my_project, my_task = add_assignees(user, my_project, my_task)
            clear_console(2)

        elif ch == "4":  # 4. Remove assignees
            user, my_project, my_task = remove_assignees(user, my_project, my_task)
            clear_console(2)

        elif ch == "5":  # 5. Priority
            ans = "-1"
            while ans == "-1":
                print("1. LOW\n2. MEDIUM\n3. HIGH\n4. CRITICAL")
                ans = input("Enter the new priority of the task: ")
                if ans == "1":
                    priority = Priority.LOW.value
                    user, my_project, my_task = change_priority(priority, user, my_project, my_task)

                elif ans == "2":
                    priority = Priority.MEDIUM.value
                    user, my_project, my_task = change_priority(priority, user, my_project, my_task)

                elif ans == "3":
                    priority = Priority.HIGH.value
                    user, my_project, my_task = change_priority(priority, user, my_project, my_task)
                elif ans == "4":
                    priority = Priority.CRITICAL.value
                    user, my_project, my_task = change_priority(priority, user, my_project, my_task)
                else:
                    pr_red("Error: Invalid value!")
                    clear_console(2)
                    ans = "-1"
            clear_console(2)

        elif ch == "6":  # 6. Status
            print("1. BACKLOG\n2. TODO\n3. DOING\n4. DONE\n5. ARCHIVED")
            ans = input("Enter the new priority of the task: ")
            if ans == "1":
                status = Status.BACKLOG.value
                user, my_project, my_task = (status, user, my_project, my_task)

            elif ans == "2":
                status = Status.TODO.value
                user, my_project, my_task = change_priority(status, user, my_project, my_task)

            elif ans == "3":
                status = Status.DOING.value
                user, my_project, my_task = change_priority(status, user, my_project, my_task)

            elif ans == "4":
                status = Status.DONE.value
                user, my_project, my_task = change_priority(status, user, my_project, my_task)

            elif ans == "5":
                status = Status.ARCHIVED.value
                user, my_project, my_task = change_priority(status, user, my_project, my_task)

            else:
                pr_red("Error: Invalid value!")
                clear_console(2)
                ans = "-1"
            clear_console(2)

        elif ch == "7":  # 7. Add comment
            print("add comment")
            clear_console(2)

        elif ch == "8":  # 8. Back
            print("Going back...")
            clear_console(2)
            return user, my_project, my_task

        else:
            pr_red("Error: Invalid value!")
            clear_console(2.5)
            ch = "-1"
