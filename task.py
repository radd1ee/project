from load_save_functions import *
import csv

TASKS_FILE = 'tasks.json'

class Task:
    def __init__(self, task_id, title, description, done=False, priority='Средний', due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data(TASKS_FILE, [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data(TASKS_FILE, data)

    def add_task(self, title, description, priority, due_date):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, title, description, False, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print('Задача успешно добавлена!')

    def list_tasks(self, filter_by=None):
        if not self.tasks:
            print('Список задач пуст.')
            return
        filtered_tasks = self.tasks
        if filter_by == 'done':
            filtered_tasks = [task for task in self.tasks if task.done]
        elif filter_by == 'not_done':
            filtered_tasks = [task for task in self.tasks if not task.done]
        for task in filtered_tasks:
            status = 'Выполнена' if task.done else 'Не выполнена'
            print(f'{task.id}. {task.title} [{status}] (Приоритет: {task.priority}, Срок: {task.due_date})')

    def mark_task_done(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print('Задача отмечена как выполненная!')
        else:
            print('Задача не найдена.')

    def edit_task(self, task_id, title, description, priority, due_date):
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            self.save_tasks()
            print('Задача успешно обновлена!')
        else:
            print('Задача не найдена.')

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print('Задача успешно удалена!')
        else:
            print('Задача не найдена.')

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def export_tasks_to_csv(self):
        if not self.tasks:
            print('Список задач пуст.')
            return
        file_name = 'tasks_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Название', 'Описание', 'Статус', 'Приоритет', 'Срок выполнения']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    'ID': task.id,
                    'Название': task.title,
                    'Описание': task.description,
                    'Статус': 'Выполнена' if task.done else 'Не выполнена',
                    'Приоритет': task.priority,
                    'Срок выполнения': task.due_date
                })
        print(f'Задачи успешно экспортированы в файл {file_name}')

    def import_tasks_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                task_id = max([task.id for task in self.tasks], default=0) + 1
                title = row.get('Название', '')
                description = row.get('Описание', '')
                status = row.get('Статус', 'Не выполнена')
                done = True if status == 'Выполнена' else False
                priority = row.get('Приоритет', 'Средний')
                due_date = row.get('Срок выполнения', None)
                new_task = Task(task_id, title, description, done, priority, due_date)
                self.tasks.append(new_task)
            self.save_tasks()
        print('Задачи успешно импортированы из CSV-файла.')

def tasks_menu():
    manager = TaskManager()
    while True:
        print('\nУправление задачами:')
        print('1. Добавить новую задачу')
        print('2. Просмотреть все задачи')
        print('3. Отметить задачу как выполненную')
        print('4. Редактировать задачу')
        print('5. Удалить задачу')
        print('6. Экспорт задач в CSV')
        print('7. Импорт задач из CSV')
        print('8. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            title = input('Введите название задачи: ')
            description = input('Введите описание задачи: ')
            priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
            due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
            manager.add_task(title, description, priority, due_date)
        elif choice == '2':
            manager.list_tasks()
        elif choice == '3':
            try:
                task_id = int(input('Введите ID задачи: '))
                manager.mark_task_done(task_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '4':
            try:
                task_id = int(input('Введите ID задачи: '))
                title = input('Введите новое название задачи: ')
                description = input('Введите новое описание задачи: ')
                priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
                due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
                manager.edit_task(task_id, title, description, priority, due_date)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            try:
                task_id = int(input('Введите ID задачи: '))
                manager.delete_task(task_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '6':
            manager.export_tasks_to_csv()
        elif choice == '7':
            manager.import_tasks_from_csv()
        elif choice == '8':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')