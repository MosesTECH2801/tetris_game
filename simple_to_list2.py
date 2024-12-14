import json
from datetime import datetime
import os

class Task:
    def __init__(self, title, description, due_date=None, priority="Medium", status="Pending"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.filename = "todo_list.json"
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for task_data in data:
                        task = Task(
                            task_data['title'],
                            task_data['description'],
                            task_data.get('due_date'),
                            task_data.get('priority', 'Medium'),
                            task_data.get('status', 'Pending')
                        )
                        self.tasks.append(task)
            except:
                print("Error loading tasks file")

    def save_tasks(self):
        try:
            with open(self.filename, 'w') as file:
                tasks_data = []
                for task in self.tasks:
                    task_dict = {
                        'title': task.title,
                        'description': task.description,
                        'due_date': task.due_date,
                        'priority': task.priority,
                        'status': task.status,
                        'created_date': task.created_date
                    }
                    tasks_data.append(task_dict)
                json.dump(tasks_data, file, indent=4)
        except:
            print("Error saving tasks")

    def add_task(self):
        print("\nAdd New Task")
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ")
        priority = input("Enter priority (High/Medium/Low): ").capitalize()

        task = Task(title, description, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("\nNo tasks found!")
            return

        print("\nTask List:")
        for i, task in enumerate(self.tasks, 1):
            print(f"\nTask {i}:")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Due Date: {task.due_date or 'Not set'}")
            print(f"Priority: {task.priority}")
            print(f"Status: {task.status}")
            print("-" * 30)

    def delete_task(self):
        self.view_tasks()
        if not self.tasks:
            return

        try:
            task_num = int(input("\nEnter task number to delete: "))
            if 1 <= task_num <= len(self.tasks):
                del self.tasks[task_num - 1]
                self.save_tasks()
                print("Task deleted successfully!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

def main():
    todo = ToDoList()
    
    while True:
        print("\n=== To-Do List Menu ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            todo.add_task()
        elif choice == '2':
            todo.view_tasks()
        elif choice == '3':
            todo.delete_task()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()