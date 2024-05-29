import json
import rich
import uuid
from enum import Enum
from user import User
from user import Admin
import time
from projects import Project

a = time.time()
user_file_path = "user.json"
projects_file_path = "projects.json"
admin_file_path = "admin_1.json"


class Task:
    def __init__(self, my_project: Project, task_title):
        self.project_id = my_project.get_project_id()
        self.__task_id = uuid.uuid1()
        self.task_title = task_title
        self.description = "" #. optional
        self.start_date = time.ctime(time.time())
        self.due_date = time.ctime(time.time() + 24 * 60 * 60)
        self.assignees = []
        self.priority = "LOW"
        self.status = "BACKLOG"
        self.comments = {
            "comment": "",
            "user": "",
            "date": ""
        } #.??

    def get_unique_identifier(self):
        return self.__task_id

    def to_dict_and_save_to_file(self, leader: User, my_project: Project):
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
        # Saving task in 'projects.json'
        with open(projects_file_path, "r") as f:
            all_projects = json.load(f)

        for it in range(len(all_projects)):
            if all_projects[it]["project_id"] == self.project_id:
                print("tasks before: ", all_projects[it]["tasks"]) #.
                all_projects[it]["tasks"].append(new_task_dict)
                print("tasks after: ", all_projects[it]["tasks"]) #.
                break

        with open(projects_file_path, "w") as f:
            json.dump(all_projects, f, indent=4)

        # Updating the project in 'user.json'
        with open(user_file_path, "r") as f:
            all_users = json.load(f)

        for it in range(len(all_users)):
            if all_users[it]["username"] == my_project.leader_username:    # Finding the leader
                leader_projects_as_leader = all_users[it]["projects_as_leader"]
                for iterate in range(len(leader_projects_as_leader)):
                    if leader_projects_as_leader[iterate]["project_id"] == my_project.get_project_id():





    def change_details(self): #. change obj data and save to files
        pass




#############
# input()
#
# task_1 = Task("mdc", "oijh")
# print(time.gmtime())
# print(time.time())
# b = time.time()
# print(b-a)
# print(time.ctime(a))
# print(f"start date: {task_1.start_date}")
# print(f"due date: {task_1.due_date}")
