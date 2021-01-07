from forex_python.converter import CurrencyRates
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 440
height = 170
x = screen_width / 2 - width / 2
y = screen_height / 2 - height / 0.55
root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

root.title('Currency Converter')

currencies = ['', 'USD', 'CAD', 'MXN', 'PHP', 'CNY', 'JPY', 'THB', 'MYR', 'IDR', 'INR', 'DKK', 'EUR', 'BGN', 'CZK',
              'BRL']

variable1 = tk.StringVar(root)
variable2 = tk.StringVar(root)


def convert(e):
    c = CurrencyRates()

    from_currency = variable1.get()
    to_currency = variable2.get()

    try:
        if from_amount_entry.get() == '':
            tk.messagebox.showerror('Error', 'Please enter a valid amount.')

        elif from_currency == '' or to_currency == '':
            tk.messagebox.showerror('Error', 'Please select a currency pair.')

        else:
            new_amt = c.convert(from_currency, to_currency, float(from_amount_entry.get()))
            new_amount = float(f'{new_amt:.2e}')

            to_amount_label.config(text=f'{new_amount:,}')

    except ValueError:
        tk.messagebox.showerror('Error', 'Please enter a valid amount.')


def clear(e):
    from_amount_entry.delete(0, 'end')
    to_amount_label.config(text='')


menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(menu=file_menu, label='File')
file_menu.add_command(label='Quit             ⌘Q', command=root.quit)

font = ('arial', 15)

frame1 = tk.Frame(root)
frame1.pack(pady=20, padx=(48, 0), anchor='w')

from_label = tk.Label(frame1, text='From:', font=font)
from_label.grid(row=0, column=0)

from_currency_option = ttk.OptionMenu(frame1, variable1, *currencies)
from_currency_option.config(width=4)
from_currency_option.grid(row=0, column=2, padx=(0, 100))

to_label = tk.Label(frame1, text='To:', font=font)
to_label.grid(row=0, column=3)

to_currency_option = ttk.OptionMenu(frame1, variable2, *currencies)
to_currency_option.config(width=4)
to_currency_option.grid(row=0, column=4)

frame2 = tk.Frame(root)
frame2.pack(pady=0, padx=(50, 0), anchor='w')

from_amount_entry = tk.Entry(frame2, width=15, font=font)
from_amount_entry.grid(row=0, column=0, padx=(0, 70))

to_amount_label = tk.Label(frame2, text='', width=15, font=font)
to_amount_label.grid(row=0, column=1)

frame3 = tk.Frame(root)
frame3.pack(pady=20, padx=(50, 0), anchor='w')

convert_btn = ttk.Button(frame3, text='Convert')
convert_btn.grid(row=0, column=0, padx=(0, 20))
convert_btn.bind('<Button-1>', convert)
convert_btn.bind('<Return>', convert)
convert_btn.bind('<KP_Enter>', convert)

clear_btn = ttk.Button(frame3, text='Clear')
clear_btn.grid(row=0, column=1)
clear_btn.bind('<Button-1>', clear)
clear_btn.bind('<Return>', clear)
clear_btn.bind('<KP_Enter>', clear)

root.mainloop()
