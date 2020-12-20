import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import MultipleLocator
import mplfinance as mpf
from pandas_datareader import data
import tkinter as tk
from tkinter import ttk


def quit(e):
    root.quit()


def submit_btn_enabler(*args):
    x = stringvar1.get()
    y = stringvar2.get()
    z = stringvar3.get()
    if x and y and z:
        submit_btn.config(state='normal')
    else:
        submit_btn.config(state='disabled')


def about():
    global img_about
    top = tk.Toplevel()
    top.title('About StockPal')
    top.geometry('850x220')
    img_about = tk.PhotoImage(file='About.png')
    img_label = tk.Label(top, image=img_about)
    img_label.pack()


def grapher(event):
    global top
    top = tk.Toplevel()

    try:
        status_label.config(text='')
        ticker = ticker_entry.get()
        start = start_entry.get()
        end = end_entry.get()

        stock_data = data.DataReader(ticker, 'yahoo', start, end)

        fig, ax = mpf.plot(stock_data, type='candle', mav=(20, 50), volume=True, title=f"{ticker.upper()}",
                           style='yahoo', returnfig=True, figsize=(16, 9))

        ax[0].legend(('20 MA', '50 MA'), loc=(1, 1))
        ax[0].xaxis.set_major_locator(MultipleLocator(14))

        canvas = FigureCanvasTkAgg(fig, top)
        canvas.get_tk_widget().pack()

        toolbarFrame = tk.Frame(master=top)
        toolbarFrame.pack()
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)




    except Exception as e:
        status_label.config(text=e)
        top.destroy()


root = tk.Tk()
frame = tk.Frame(root, bg='#2E8B57')
frame.pack()
root.title('StockPal')
root.resizable(width=False, height=False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

app_width = 850
app_height = 220

x = screen_width / 2 - app_width / 2
y = screen_height / 2 - app_height / 2

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.config(bg='#2E8B57')

img = tk.Image("photo", file='StockPal.png')
root.iconphoto(True, img)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label='StockPal', menu=file_menu)
file_menu.add_command(label='About StockPal', command=about)
file_menu.add_command(label='Quit                     ⌘Q', command=root.quit)

stringvar1 = tk.StringVar(root)
stringvar2 = tk.StringVar(root)
stringvar3 = tk.StringVar(root)

stringvar1.trace("w", submit_btn_enabler)
stringvar2.trace("w", submit_btn_enabler)
stringvar3.trace("w", submit_btn_enabler)

ticker_lbl = tk.Label(frame, text='Ticker Symbol', bg='#2E8B57', fg='#E9E9E9', font=('Arial', 17))
ticker_lbl.grid(row=0, column=1, pady=20)
ticker_entry = ttk.Entry(frame, textvariable=stringvar1, font=('helvetica', 20))
ticker_entry.grid(row=1, column=1)
ticker_entry.focus()

start_lbl = tk.Label(frame, text='Start Date YYYY-MM-DD', bg='#2E8B57', fg='#E9E9E9', font=('Arial', 17))
start_lbl.grid(row=0, column=2)
start_entry = ttk.Entry(frame, textvariable=stringvar2, font=('helvetica', 20))
start_entry.grid(row=1, column=2)

end_lbl = tk.Label(frame, text='End Date YYYY-MM-DD', bg='#2E8B57', fg='#E9E9E9', font=('Arial', 17))
end_lbl.grid(row=0, column=3)
end_entry = ttk.Entry(frame, textvariable=stringvar3, font=('helvetica', 20))
end_entry.grid(row=1, column=3)

s = ttk.Style()
s.configure('submit.TButton', font=('Arial', 16))
submit_btn = ttk.Button(root, text='Submit', state='disabled', style='submit.TButton')
submit_btn.pack(pady=20, ipadx=10, ipady=8)
submit_btn.bind('<Return>', grapher)
submit_btn.bind('<KP_Enter>', grapher)
submit_btn.bind('<Button-1>', grapher)

status_label = tk.Label(root, text='', bd=1, relief='groove', anchor='e', fg='#FF3333', bg='#E9E9E9')
status_label.pack(fill='x', side='bottom', ipady=2)

root.bind('<Mod1-q>', quit)

root.mainloop()
