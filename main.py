from collections import namedtuple
import tkinter as tk
from tkinter import ttk


def handle_operation(button_text: str):
    def inner():
        print(button_text)
    return inner


def handle_number(button_text: str):
    def inner():
        print(button_text)
    return inner


CalcButton = namedtuple('CalcButton',
                        ['column', 'row', 'text', 'is_operation'])
buttons = (
    CalcButton(0, 1, '7', False), CalcButton(1, 1, '8', False), CalcButton(2, 1, '9', False), CalcButton(3, 1, 'X', True),
    CalcButton(0, 2, '4', False), CalcButton(1, 2, '5', False), CalcButton(2, 2, '6', False), CalcButton(3, 2, ':', True),
    CalcButton(0, 3, '1', False), CalcButton(1, 3, '2', False), CalcButton(2, 3, '3', False), CalcButton(3, 3, '+', True),
    CalcButton(0, 4, '^', True), CalcButton(1, 4, '0', False), CalcButton(2, 4, '-', True), CalcButton(3, 4, '=', True)
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
    ttk.Button(master=calc_frame, text=button.text,
               command=(handle_operation(button.text) if button.is_operation else handle_number(button.text))).grid(row=button.row, column=button.column)

window.mainloop()

