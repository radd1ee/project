from load_save_functions import *
import datetime
import csv

FINANCE_FILE = 'finance.json'

class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

class FinanceManager:
    def __init__(self):
        self.records = []
        self.load_records()

    def load_records(self):
        data = load_data(FINANCE_FILE, [])
        self.records = [FinanceRecord(**record) for record in data]

    def save_records(self):
        data = [record.__dict__ for record in self.records]
        save_data(FINANCE_FILE, data)

    def add_record(self, amount, category, date, description):
        record_id = max([record.id for record in self.records], default=0) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(new_record)
        self.save_records()
        print('Запись успешно добавлена!')

    def list_records(self):
        if not self.records:
            print('Финансовых записей нет.')
            return
        for record in self.records:
            print(f'{record.id}. {record.date} | {record.amount} | {record.category} | {record.description}')

    def generate_report(self, start_date, end_date):
        try:
            start_date_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')
            end_date_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')
        except ValueError:
            print('Некорректный формат даты.')
            return

        filtered_records = [record for record in self.records if start_date_obj <= datetime.datetime.strptime(record.date, '%d-%m-%Y') <= end_date_obj]
        income = sum(record.amount for record in filtered_records if record.amount > 0)
        expenses = sum(record.amount for record in filtered_records if record.amount < 0)
        balance = income + expenses
        print(f'Финансовый отчёт за период с {start_date} по {end_date}:')
        print(f'- Общий доход: {income}')
        print(f'- Общие расходы: {abs(expenses)}')
        print(f'- Баланс: {balance}')

        # Сохранение отчёта в CSV-файл
        report_file = f'report_{start_date}_{end_date}.csv'
        with open(report_file, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Дата', 'Сумма', 'Категория', 'Описание']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for record in filtered_records:
                writer.writerow({
                    'ID': record.id,
                    'Дата': record.date,
                    'Сумма': record.amount,
                    'Категория': record.category,
                    'Описание': record.description
                })
        print(f'Подробная информация сохранена в файле {report_file}')

    def delete_record(self, record_id):
        record = self.get_record_by_id(record_id)
        if record:
            self.records.remove(record)
            self.save_records()
            print('Запись успешно удалена!')
        else:
            print('Запись не найдена.')

    def get_record_by_id(self, record_id):
        for record in self.records:
            if record.id == record_id:
                return record
        return None

    def export_records_to_csv(self):
        if not self.records:
            print('Финансовых записей нет.')
            return
        file_name = 'finance_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Сумма', 'Категория', 'Дата', 'Описание']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow({
                    'ID': record.id,
                    'Сумма': record.amount,
                    'Категория': record.category,
                    'Дата': record.date,
                    'Описание': record.description
                })
        print(f'Финансовые записи успешно экспортированы в файл {file_name}')

    def import_records_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                record_id = max([record.id for record in self.records], default=0) + 1
                amount = float(row.get('Сумма', '0'))
                category = row.get('Категория', '')
                date = row.get('Дата', datetime.datetime.now().strftime('%d-%m-%Y'))
                description = row.get('Описание', '')
                new_record = FinanceRecord(record_id, amount, category, date, description)
                self.records.append(new_record)
            self.save_records()
        print('Финансовые записи успешно импортированы из CSV-файла.')

def finance_menu():
    manager = FinanceManager()
    while True:
        print('\nУправление финансовыми записями:')
        print('1. Добавить новую запись')
        print('2. Просмотреть все записи')
        print('3. Генерация отчёта')
        print('4. Удалить запись')
        print('5. Экспорт финансовых записей в CSV')
        print('6. Импорт финансовых записей из CSV')
        print('7. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            try:
                amount = float(input('Введите сумму (доход — положительное число, расход — отрицательное): '))
                category = input('Введите категорию: ')
                date = input('Введите дату операции (в формате ДД-ММ-ГГГГ): ')
                description = input('Введите описание операции: ')
                manager.add_record(amount, category, date, description)
            except ValueError:
                print('Некорректный ввод суммы.')
        elif choice == '2':
            manager.list_records()
        elif choice == '3':
            start_date = input('Введите начальную дату (ДД-ММ-ГГГГ): ')
            end_date = input('Введите конечную дату (ДД-ММ-ГГГГ): ')
            manager.generate_report(start_date, end_date)
        elif choice == '4':
            try:
                record_id = int(input('Введите ID записи: '))
                manager.delete_record(record_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            manager.export_records_to_csv()
        elif choice == '6':
            manager.import_records_from_csv()
        elif choice == '7':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')