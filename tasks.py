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


user_file_path = "user.json"
projects_file_path = "projects.json"
admin_file_path = "admin.json"


class Priority(Enum):
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH",
    CRITICAL = "CRITICAL"


class Status(Enum):
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

    def to_dict_and_save_to_file(self, my_project: Project):    # Returns my_project after updates
        new_task_dict = {
            "task_id": self.__task_id,
            "task_title": self.task_title,
            "description": self.description,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "assignees": self.assignees,
            "priority": self.priority,
            "status": self.status,
            "comments": self.comments    # List of tuples
        }

        # Updating the project object
        my_project.tasks.append(new_task_dict)

        # Saving task in 'projects.json'
        with open(projects_file_path, "r") as f:
            all_projects = json.load(f)

        for it in range(len(all_projects)):
            if all_projects[it]["project_id"] == self.project_id:
                print("tasks before: ", all_projects[it]["tasks"]) #.
                all_projects[it]["tasks"] = my_project.tasks
                print("tasks after: ", all_projects[it]["tasks"]) #.
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

    def change_details(self): #. change obj data and save to files
        pass

    def add_comment(self, user: User, comment):    # The user is either the leader or an assignee
        self.comments.append((comment, user.username, time.ctime(time.time())))

    def set_title(self, title):
        self.task_title = title

    def set_description(self, description):
        self.description = description

    def change_priority(self, priority):
        if priority == "LOW":
            self.priority = Priority.LOW
        elif priority == "MEDIUM":
            self.priority = Priority.MEDIUM
        elif priority == "HIGH":
            self.priority = Priority.HIGH
        elif priority == "CRITICAL":
            self.priority = Priority.CRITICAL

    def change_status(self, status):
        if status == "BACKLOG":
            self.status = Status.BACKLOG
        elif status == "TODO":
            self.status = Status.TODO
        elif status == "DOING":
            self.status = Status.DOING
        elif status == "DONE":
            self.status = Status.DONE
        elif status == "ARCHIVED":
            self.status = Status.ARCHIVED

    # def add_assignee(self, user: User):





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
            table.add_column("BACKLOG", justify="right", style="cyan", no_wrap=True) #.
            table.add_column("TODO", style="magenta", no_wrap=True) #.
            table.add_column("DOING", justify="right", style="green", no_wrap=True) #.
            table.add_column("DONE", justify="right", style="cyan", no_wrap=True) #.
            table.add_column("ARCHIVED", justify="right", style="magenta", no_wrap=True) #.

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
                my_task = create_a_task(my_project) #.
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

                    user, my_project, my_task = task_details(user, my_project, my_task)

                    print("function to see and change the chosen task's details.")#. function to see and change the chosen task's details
                    clear_console(2)
                    ch = "-1"
                    break

            if ch != "-1":
                pr_red("Error: Invalid value!")
                ch = "-1"


def task_details(user: User, my_project: Project, my_task: Task):
    ch = "-1"
    while ch != "0":
        table = Table(title="Task details")

        table.add_column("ID", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Title", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Description", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Start Date", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Due Date", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Assignees", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Priority", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Status", justify="right", style="cyan", no_wrap=True, min_width=20)
        table.add_column("Comments", justify="right", style="cyan", no_wrap=True, width=150)

        table.add_row(f"{my_task.get_task_id()}", f"{my_task.task_title}", f"{my_task.description}",
                      f"{my_task.start_date}", f"{my_task.due_date}", f"{my_task.assignees}", f"{my_task.priority}",
                      f"{my_task.status}", f"{my_task.comments}")

        console = Console()
        console.print(table)

        print("\n1. Change details\n2. Back")
        ch = input()
        if ch == "1":    # 1. Change details
            if user.username == my_project.leader_username or user.username in my_task.assignees:
                print("function for changing details") #.
            else:
                pr_red("As neither the leader of this project nor an "
                       "assignee of the task, you can not change its details.")
                clear_console(2)
                ch = "-1"

        elif ch == "2":    # 2. Back
            print("Going Back...")
            clear_console(2)
            return user, my_project, my_task


# def change_task_details(user: User, my_project: Project, my_task: Task):
#     ch = "-1"
#     while ch != "0":
