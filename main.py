# TODO: Добавить историю вычислений.
from collections import namedtuple
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

        if button_text == '=' or key == 'Return':
            try:
                res = calculate_expression(enter_field.get())
            except ZeroDivisionError:
                showerror('Помилка',
                          'Ділення на 0!')
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


CalcButton = namedtuple('CalcButton',
                        ['column', 'row', 'text', 'is_operation', 'key'])
buttons = (
    CalcButton(0, 3, '1', False, '<KP_1>'),
    CalcButton(1, 3, '2', False, '<KP_2>'),
    CalcButton(2, 3, '3', False, '<KP_3>'),
    CalcButton(0, 2, '4', False, '<KP_4>'),
    CalcButton(1, 2, '5', False, '<KP_5>'),
    CalcButton(2, 2, '6', False, '<KP_6>'),
    CalcButton(0, 1, '7', False, '<KP_7>'),
    CalcButton(1, 1, '8', False, '<KP_8>'),
    CalcButton(2, 1, '9', False, '<KP_9>'),
    CalcButton(1, 4, '0', False, '<KP_0>'),
    CalcButton(3, 1, 'X', True, '<KP_Multiply>'),
    CalcButton(3, 2, ':', True, '<KP_Divide>'),
    CalcButton(3, 3, '+', True, '<KP_Add>'),
    CalcButton(3, 4, '-', True, '<KP_Subtract>'),
    CalcButton(2, 4, '=', True, '<Return>'),
    CalcButton(0, 4, 'C', True, '<Delete>')
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
    btn = ttk.Button(master=calc_frame, text=button.text,
                     command=(handle_operation(button.text) if button.is_operation else handle_number(button.text)))
    btn.grid(row=button.row, column=button.column)
    window.bind(button.key,
                (handle_operation(button.text) if button.is_operation else handle_number(button.text)))

window.mainloop()
