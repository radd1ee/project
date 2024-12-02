import os
import json
import datetime
import csv
from notes import notes_menu
from tasks import tasks_menu
from contacts import contacts_menu
from finance import finance_menu
from calculator import calculator_menu

def main_menu():
    while True:
        print('\nДобро пожаловать в Персональный помощник!')
        print('Выберите действие:')
        print('1. Управление заметками')
        print('2. Управление задачами')
        print('3. Управление контактами')
        print('4. Управление финансовыми записями')
        print('5. Калькулятор')
        print('6. Выход')
        choice = input('Введите номер действия: ')
        if choice == '1':
            notes_menu()
        elif choice == '2':
            tasks_menu()
        elif choice == '3':
            contacts_menu()
        elif choice == '4':
            finance_menu()
        elif choice == '5':
            calculator_menu()
        elif choice == '6':
            print('До свидания!')
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')

if __name__ == '__main__':
    main_menu()