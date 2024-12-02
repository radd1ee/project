def calculator_menu():
    print('\nКалькулятор')
    while True:
        expression = input('Введите выражение для вычисления или "назад" для возврата: ')
        if expression.lower() == "назад":
            break
        try:
            import ast
            result = eval(expression, {'__builtins__': None}, {})
            print(f'Результат: {result}')
        except Exception as e:
            print(f'Ошибка: {e}')