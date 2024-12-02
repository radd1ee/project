from load_save_functions import *
import csv

CONTACTS_FILE = 'contacts.json'

class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        data = load_data(CONTACTS_FILE, [])
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.__dict__ for contact in self.contacts]
        save_data(CONTACTS_FILE, data)

    def add_contact(self, name, phone, email):
        contact_id = max([contact.id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print('Контакт успешно добавлен!')

    def search_contacts(self, query):
        results = [contact for contact in self.contacts if query.lower() in contact.name.lower() or query in contact.phone]
        if results:
            for contact in results:
                print(f"{contact.id}. {contact.name} (Телефон: {contact.phone}, E-mail: {contact.email})")
        else:
            print('Контакты не найдены.')

    def edit_contact(self, contact_id, name, phone, email):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            contact.name = name
            contact.phone = phone
            contact.email = email
            self.save_contacts()
            print('Контакт успешно обновлён!')
        else:
            print('Контакт не найден.')

    def delete_contact(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print('Контакт успешно удалён!')
        else:
            print('Контакт не найден.')

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None

    def export_contacts_to_csv(self):
        if not self.contacts:
            print('Список контактов пуст.')
            return
        file_name = 'contacts_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Имя', 'Телефон', 'E-mail']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow({
                    'ID': contact.id,
                    'Имя': contact.name,
                    'Телефон': contact.phone,
                    'E-mail': contact.email
                })
        print(f'Контакты успешно экспортированы в файл {file_name}')

    def import_contacts_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                contact_id = max([contact.id for contact in self.contacts], default=0) + 1
                name = row.get('Имя', '')
                phone = row.get('Телефон', '')
                email = row.get('E-mail', '')
                new_contact = Contact(contact_id, name, phone, email)
                self.contacts.append(new_contact)
            self.save_contacts()
        print('Контакты успешно импортированы из CSV-файла.')

def contacts_menu():
    manager = ContactManager()
    while True:
        print('\nУправление контактами:')
        print('1. Добавить новый контакт')
        print('2. Поиск контакта')
        print('3. Редактировать контакт')
        print('4. Удалить контакт')
        print('5. Экспорт контактов в CSV')
        print('6. Импорт контактов из CSV')
        print('7. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            name = input('Введите имя контакта: ')
            phone = input('Введите номер телефона: ')
            email = input('Введите e-mail: ')
            manager.add_contact(name, phone, email)
        elif choice == '2':
            query = input('Введите имя или номер телефона для поиска: ')
            manager.search_contacts(query)
        elif choice == '3':
            try:
                contact_id = int(input('Введите ID контакта: '))
                name = input('Введите новое имя: ')
                phone = input('Введите новый номер телефона: ')
                email = input('Введите новый e-mail: ')
                manager.edit_contact(contact_id, name, phone, email)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '4':
            try:
                contact_id = int(input('Введите ID контакта: '))
                manager.delete_contact(contact_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            manager.export_contacts_to_csv()
        elif choice == '6':
            manager.import_contacts_from_csv()
        elif choice == '7':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')