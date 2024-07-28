# import python standard libraries
import json
import os
import sys

# import downloadable python libraries
from colorama import Fore, Style


class Directory:
    def __init__(self, name):
        self.name = name
        self.name_path = None
        self.name_exists = None
        self.check_directory()
        if not self.name_exists:
            self.create_directory()

    @staticmethod
    def get_executable_directory():
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def check_directory(self):
        self.name_path = os.path.join(self.get_executable_directory(), self.name)
        self.name_exists = os.path.exists(self.name_path)

    def create_directory(self):
        os.mkdir(self.name_path)


class File:
    def __init__(self, name):
        self.name = name
        self.name_path = None
        self.name_exists = None
        self.check_file()
        if not self.name_exists:
            self.create_file()

    @staticmethod
    def get_executable_directory():
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))

    def check_file(self):
        self.name_path = os.path.join(self.get_executable_directory(), "data", self.name)
        self.name_exists = os.path.isfile(self.name_path)

    def create_file(self):
        with open(self.name_path, "x") as file:
            file.write('{\n  "tasks": [\n  ]\n}')


class GetCommand:
    def __init__(self):
        self.ran_command = None
        self.task_name = None
        self.task_id = None
        while True:
            self.user_command = input(f">> ")
            self.identify_command()

    def identify_command(self):
        self.ran_command = None

        # interface commands
        if self.user_command == "exit" or self.user_command == "close":
            Command.exit_command()
            self.ran_command = True

        if self.user_command == "clear" or self.user_command == "cls":
            Command.clear_command()
            self.ran_command = True

        if self.user_command == "help":
            Command.help_command()
            self.ran_command = True

        # task commands
        if self.user_command.startswith("task add"):
            self.task_name = self.user_command.replace("task add ", "", 1)
            Command.task_add_command(self.task_name)
            self.ran_command = True

        if self.user_command == "task list":
            Command.task_list_command()
            self.ran_command = True

        if self.user_command.startswith("task done"):
            self.task_id = self.user_command.replace("task done ", "", 1)
            Command.task_done_command(self.task_id)
            self.ran_command = True

        if self.user_command.startswith("task incomplete"):
            self.task_id = self.user_command.replace("task incomplete ", "", 1)
            Command.task_incomplete_command(self.task_id)
            self.ran_command = True

        if self.user_command.startswith("task remove"):
            self.task_id = self.user_command.replace("task remove ", "", 1)
            Command.task_remove_command(self.task_id)
            self.ran_command = True

        # command not found
        if not self.ran_command:
            print(f"\n{Fore.RED}ERROR: {Style.RESET_ALL}The command '{self.user_command}' you entered, doesn't exist. "
                  f"Type 'help' for all available "
                  f"commands.\n")


class Command:
    def __init__(self):
        pass

    @staticmethod
    def exit_command():
        exit()

    @staticmethod
    def clear_command():
        os.system("cls")

    @staticmethod
    def help_command():
        print(f"\nInterface Commands:\n-exit/close: Closes the program\n-clear/cls: Clears the terminal\n-help: Shows "
              f"this menu\n\nTask Command:\n-task add <name>: Adds a new task to the to do list, replace <name> with "
              f"the actual name of the task.\n-task list: Lists all the tasks, with it's id, and status\n-task done "
              f"<id>: Mark a task done, using it's id, use the 'task list' command to get the task's id.\n-task "
              f"incomplete <id>: Mark a task incomplete, using it's id, use the 'task list' command to get the task's "
              f"id.\n-task remove <id>: Remove a task, using it's id, use the 'task list' command to get the task's "
              f"id.\n")

    @staticmethod
    def task_add_command(name):
        def get_executable_directory():
            if getattr(sys, "frozen", False):
                return os.path.dirname(sys.executable)
            else:
                return os.path.dirname(os.path.abspath(__file__))

        def load_todo_list():
            with open(os.path.join(get_executable_directory(), "data", "tasks.json")) as file:
                return json.load(file)

        def save_todo_list(data):
            with open(os.path.join(get_executable_directory(), "data", "tasks.json"), 'w') as file:
                json.dump(data, file, indent=4)

        def get_next_task_id():
            tasks = load_todo_list().get("tasks", [])
            if tasks:
                return max(task['id'] for task in tasks) + 1
            else:
                return 0

        print(f"\n{Fore.GREEN}DONE: {Style.RESET_ALL}Task with ID:" + str(get_next_task_id()) + f", name: {name}, "
              f"Done: {Fore.RED}False{Style.RESET_ALL}. Has successfully been created.\n")
        new_task = {
            "id": get_next_task_id(),
            "name": name,
            "done": False
        }

        todo_list = load_todo_list()
        todo_list.setdefault("tasks", []).append(new_task)
        save_todo_list(todo_list)

    @staticmethod
    def task_list_command():
        def get_executable_directory():
            if getattr(sys, "frozen", False):
                return os.path.dirname(sys.executable)
            else:
                return os.path.dirname(os.path.abspath(__file__))

        def load_todo_list():
            with open(os.path.join(get_executable_directory(), "data", "tasks.json")) as file:
                return json.load(file)

        todo_list = load_todo_list()
        tasks = todo_list.get("tasks", [])

        print(f"")
        for task in tasks:
            task_id = task["id"]
            task_name = task["name"]
            task_done = f"{Fore.GREEN}Yes{Style.RESET_ALL}" if task["done"] else f"{Fore.RED}No{Style.RESET_ALL}"
            print(f"ID: {task_id}, Name: {task_name}, Done: {task_done}")
        print(f"")

    @staticmethod
    def task_done_command(task_id):
        already_done = False

        def get_executable_directory():
            if getattr(sys, "frozen", False):
                return os.path.dirname(sys.executable)
            else:
                return os.path.dirname(os.path.abspath(__file__))

        def load_todo_list():
            with open(os.path.join(get_executable_directory(), "data", "tasks.json")) as file:
                return json.load(file)

        def save_todo_list(data):
            with open(os.path.join(get_executable_directory(), "data", "tasks.json"), 'w') as file:
                json.dump(data, file, indent=4)

        todo_list = load_todo_list()
        tasks = todo_list.get("tasks", [])

        for task in tasks:
            if task['id'] == int(task_id):
                if task['done']:
                    print(f"\n{Fore.YELLOW}ERROR: {Style.RESET_ALL}Task with ID: '{task_id}' is already done.\n")
                    already_done = True
                else:
                    task['done'] = True
                    save_todo_list(todo_list)
                    print(f"\n{Fore.GREEN}DONE: {Style.RESET_ALL}Task with ID: '{task_id}' is now done.\n")
                    return

        if not already_done:
            print(f"\n{Fore.RED}ERROR: {Style.RESET_ALL}Task with ID: '{task_id}' couldn't be found.\n")

    @staticmethod
    def task_incomplete_command(task_id):
        already_incomplete = False

        def get_executable_directory():
            if getattr(sys, "frozen", False):
                return os.path.dirname(sys.executable)
            else:
                return os.path.dirname(os.path.abspath(__file__))

        def load_todo_list():
            with open(os.path.join(get_executable_directory(), "data", "tasks.json")) as file:
                return json.load(file)

        def save_todo_list(data):
            with open(os.path.join(get_executable_directory(), "data", "tasks.json"), 'w') as file:
                json.dump(data, file, indent=4)

        todo_list = load_todo_list()
        tasks = todo_list.get("tasks", [])

        for task in tasks:
            if task['id'] == int(task_id):
                if not task['done']:
                    print(f"\n{Fore.YELLOW}ERROR: {Style.RESET_ALL}Task with ID: '{task_id}' is already incomplete.\n")
                    already_incomplete = True
                else:
                    task['done'] = False
                    save_todo_list(todo_list)
                    print(f"\n{Fore.GREEN}DONE: {Style.RESET_ALL}Task with ID: '{task_id}' is now incomplete.\n")
                    return

        if not already_incomplete:
            print(f"\n{Fore.RED}ERROR: {Style.RESET_ALL}Task with ID: '{task_id}' couldn't be found.\n")

    @staticmethod
    def task_remove_command(task_id):
        def get_executable_directory():
            if getattr(sys, "frozen", False):
                return os.path.dirname(sys.executable)
            else:
                return os.path.dirname(os.path.abspath(__file__))

        def load_todo_list():
            with open(os.path.join(get_executable_directory(), "data", "tasks.json")) as file:
                return json.load(file)

        def save_todo_list(data):
            with open(os.path.join(get_executable_directory(), "data", "tasks.json"), 'w') as file:
                json.dump(data, file, indent=4)

        todo_list = load_todo_list()
        tasks = todo_list.get("tasks", [])

        task_found = False
        for task in tasks:
            if task['id'] == int(task_id):
                tasks.remove(task)
                task_found = True
                print(f"\n{Fore.GREEN}REMOVED: {Style.RESET_ALL} Task with ID '{task_id}' has been removed.\n")
                break

        if not task_found:
            print(f"\n{Fore.RED}ERROR: {Style.RESET_ALL} Task with ID '{task_id}' couldn't be found.\n")

        for index, task in enumerate(tasks):
            task['id'] = index

        todo_list['tasks'] = tasks
        save_todo_list(todo_list)


def main():
    Command.clear_command()
    Directory("data")
    File("tasks.json")
    GetCommand()


if __name__ == "__main__":
    main()
