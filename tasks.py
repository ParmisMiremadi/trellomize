import json
import uuid
from enum import Enum
from user import User
import time
from projects import Project
from user import clear_console
from user import pr_red, pr_green, pr_cyan
from rich.console import Console
from rich.table import Table


a = time.time()
user_file_path = "user.json"
projects_file_path = "projects.json"
admin_file_path = "admin_1.json"


class Task:
    def __init__(self, my_project: Project):
        self.project_id = my_project.get_project_id()
        self.__task_id = uuid.uuid1()
        self.task_title = "" #. optional/ adding later (manually)
        self.description = "" #. optional/ adding later (manually)
        self.start_date = time.ctime(time.time())
        self.due_date = time.ctime(time.time() + 24 * 60 * 60)
        self.assignees = []
        self.priority = "LOW"
        self.status = "BACKLOG"
        self.comments = {
            "comment": "",
            "user": "",
            "date": ""
        }  # . adding them later (manually)

    def get_unique_identifier(self):
        return self.__task_id

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
            "comments": self.comments
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

            # Table the project's tasks
            table = Table(title=f"ID of tasks in project {my_project.get_project_title()}:")
            table.add_column("BACKLOG", justify="right", style="cyan", no_wrap=True) #.
            table.add_column("TODO", style="magenta") #.
            table.add_column("DOING", justify="right", style="green") #.
            table.add_column("DONE", justify="right", style="cyan") #.
            table.add_column("ARCHIVED", justify="right", style="magenta") #.

            table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690") #.
            table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347") #.
            table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889") #.
            table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889") #.

            console = Console()
            console.print(table)

        else:
            print("    No tasks")
            print("1. New task\n2. Back")
            ch = input()
            if ch == "1":  # 1. New task
                if user.username == my_project.leader_username:
                    my_task = create_a_task(my_project) #.

                else:
                    pr_red(f"As a member of project {my_project.get_project_title()}, You can not create a task!")
                    print("Going Back...")
                    clear_console(2)

            elif ch == "2":  # 4. Back
                print("Going Back...")
                clear_console(2)
                return user, my_project

            else:
                pr_red("Error: Invalid value!")

