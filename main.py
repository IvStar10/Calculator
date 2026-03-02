from collections import namedtuple
import tkinter as tk
from tkinter import ttk


def handle_operation(button_text: str) -> None:
    def inner(keypress_event=None):
        if keypress_event is None:
            # Нажата экранная кнопка, с клавиатуры ничего нет.
            key = None
        else:
            key = keypress_event.keysym

        if button_text == '=' or key == 'Return':
            ...
        elif button_text == 'C' or key == 'Delete':
            enter_field.delete(0, 'end')
        else:
            ...
    return inner


def handle_number(button_text: str) -> None:
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
    window.bind(button.key, (handle_operation(button.text) if button.is_operation else handle_number(button.text)))

window.mainloop()

