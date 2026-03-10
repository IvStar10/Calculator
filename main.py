import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror


def get_operands(operator_idx: int, expression: str) -> tuple[int, int]:
    return int(expression[0:operator_idx]), int(expression[operator_idx+1:])


def calculate_expression(expr: str) -> int | float:
    if '.' in expr or ',' in expr:
        raise ValueError('Float numbers is unsupported.')
    for char in expr:
        if not char.isnumeric():
            # Оператор
            match char:
                case '+':
                    op1, op2 = get_operands(expr.find('+'), expr)
                    return op1 + op2
                case '-':
                    op1, op2 = get_operands(expr.find('-'), expr)
                    return op1 - op2
                case 'X':
                    op1, op2 = get_operands(expr.find('X'), expr)
                    return op1 * op2
                case ':':
                    op1, op2 = get_operands(expr.find(':'), expr)
                    return op1 / op2
                case _:
                    raise ValueError('Invalid operation.')
    else:
        return int(expr)  # Оператора нет, возвращаем исходное число.


def handle_operation(button_text: str):
    def inner(keypress_event=None):
        if keypress_event is None:
            # Нажата экранная кнопка, с клавиатуры ничего нет.
            key = None
        else:
            key = keypress_event.keysym

        expression = enter_field.get()
        if button_text == '=' or key == 'Return':
            try:
                res = calculate_expression(expression)
            except ZeroDivisionError:
                showerror('Помилка',
                          'Ділення на 0!')
                return
            except ValueError as e:
                if str(e) == 'Invalid operation.':
                    showerror('Помилка',
                              'Невідома операція.')
                elif str(e) == 'Float numbers is unsupported.':
                    showerror('Помилка',
                              'Підтримуються тільки цілі числа.')
                else:
                    # Ошибка от get_operands при конвертации к int.
                    showerror('Помилка',
                              'Цей калькулятор підтримує тільки одну операцію.')
                return
            enter_field.delete(0, 'end')
            enter_field.insert(0, str(res))

            history_text_field.insert('end', f'{expression} = {res}\n')
        elif button_text == 'C' or key == 'Delete':
            enter_field.delete(0, 'end')
        elif button_text in ('+', '-', 'X', ':') or key in ('KP_Multiply', 'KP_Divide', 'KP_Add', 'KP_Subtract'):
            enter_field.insert('end', button_text)
        else:
            raise ValueError("Invalid operation.")
    return inner


def handle_number(button_text: str):
    def inner(keypress_event=None):
        enter_field.insert('end', button_text)
    return inner


buttons = (
    (0, 3, '1', False, '<KP_1>'),
    (1, 3, '2', False, '<KP_2>'),
    (2, 3, '3', False, '<KP_3>'),
    (0, 2, '4', False, '<KP_4>'),
    (1, 2, '5', False, '<KP_5>'),
    (2, 2, '6', False, '<KP_6>'),
    (0, 1, '7', False, '<KP_7>'),
    (1, 1, '8', False, '<KP_8>'),
    (2, 1, '9', False, '<KP_9>'),
    (1, 4, '0', False, '<KP_0>'),
    (3, 1, 'X', True, '<KP_Multiply>'),
    (3, 2, ':', True, '<KP_Divide>'),
    (3, 3, '+', True, '<KP_Add>'),
    (3, 4, '-', True, '<KP_Subtract>'),
    (2, 4, '=', True, '<Return>'),
    (0, 4, 'C', True, '<Delete>')
)

window = tk.Tk()
enter_field_var = tk.StringVar()

history_frame = ttk.Frame(master=window)
calc_frame = ttk.Frame(master=window)

history_text_field = tk.Text(master=history_frame)

enter_field = ttk.Entry(master=calc_frame, textvariable=enter_field_var)

history_frame.grid(row=0, column=0)
calc_frame.grid(row=0, column=1)
history_text_field.pack()
enter_field.grid(row=0, column=0, columnspan=4)

for button in buttons:
    btn = ttk.Button(master=calc_frame, text=button[2],
                     command=(handle_operation(button[2]) if button[3] else handle_number(button[2])))
    btn.grid(row=(button[1]), column=(button[0]))
    window.bind(button[4],
                (handle_operation(button[2]) if button[3] else handle_number(button[2])))

window.mainloop()
