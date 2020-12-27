import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.ticker import MultipleLocator
import mplfinance as mpf
import yfinance as yf
from pandas_datareader import data
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF


def start_entry_dash(event):
    if len(start_entry.get()) == 4:
        start_entry.insert('end', "-")
    elif len(start_entry.get()) == 7:
        start_entry.insert('end', "-")
    elif len(start_entry.get()) == 11:
        start_entry.delete(10, 'end')


def end_entry_dash(event):
    if len(end_entry.get()) == 4:
        end_entry.insert('end', "-")
    elif len(end_entry.get()) == 7:
        end_entry.insert('end', "-")
    elif len(end_entry.get()) == 11:
        end_entry.delete(10, 'end')


def save(event):
    file = filedialog.asksaveasfilename(title='Save PDF', defaultextension=".pdf")
    if file is None:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.set_left_margin(20)
    pdf.multi_cell(w=171, h=5, txt=info_box.get(1.0, 'end'), align='L')
    pdf.output(file)


def chart_btn_enabler(*args):
    x = stringvar1.get()
    y = stringvar2.get()
    z = stringvar3.get()
    if x:
        info_btn.config(state='normal')
    else:
        info_btn.config(state='disabled')

    if x and y and z:
        chart_btn.config(state='normal')
    else:
        chart_btn.config(state='disabled')


def about():
    global img_about
    top = tk.Toplevel(bg='#2E8B57')
    top.title('About')
    top.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    top.resizable(width=False, height=False)
    img_about = tk.PhotoImage(file='About.png')
    img_label = tk.Label(top, image=img_about, bg='#2E8B57')
    img_label.pack()


def info(event):
    try:
        info_box.delete(1.0, 'end')
        info_box.config(state='normal')
        save_btn.config(state='normal')
        status_label.config(text='')
        file_menu.entryconfig('Save            ⌘S', state='normal')

        ticker = ticker_entry.get()

        stock = yf.Ticker(ticker)
        info = sorted([[k, v] for k, v in stock.info.items()])

        for k, v in info:
            info_box.insert(tk.INSERT, f'{k.title()}: {v}\n\n')

        info_box.config(state='disabled')

    except Exception:
        status_label.config(text="Ticker symbol not found")


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

    except Exception:
        status_label.config(text='Invalid ticker symbol information')
        top.destroy()


def clear(event):
    ticker_entry.delete(0, 'end')
    start_entry.delete(0, 'end')
    end_entry.delete(0, 'end')

    info_box.config(state='normal')
    info_box.delete(1.0, 'end')
    info_box.config(state='disabled')
    file_menu.entryconfig('Save            ⌘S', state='disabled')

    status_label.config(text='')


root = tk.Tk()
frame = tk.Frame(root, bg='#2E8B57')
frame.pack()
root.title('StockPal')
root.resizable(width=False, height=False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

app_width = 850
app_height = 750

x = screen_width / 2 - app_width / 2
y = screen_height / 2 - app_height / 2

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.config(bg='#2E8B57')

img = tk.Image("photo", file='StockPal.png')
root.iconphoto(True, img)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='StockPal', menu=file_menu)
file_menu.add_command(label='About StockPal', command=about)
file_menu.add_separator()
file_menu.add_command(label='Save            ⌘S', command=lambda: save('event'), state='disabled')
file_menu.add_command(label='Quit             ⌘Q', command=root.quit)

stringvar1 = tk.StringVar(root)
stringvar2 = tk.StringVar(root)
stringvar3 = tk.StringVar(root)

stringvar1.trace("w", chart_btn_enabler)
stringvar2.trace("w", chart_btn_enabler)
stringvar3.trace("w", chart_btn_enabler)

ticker_lbl = tk.Label(frame, text='Ticker Symbol', bg='#2E8B57', fg='#E9E9E9', font=('Arial', 17))
ticker_lbl.grid(row=0, column=1, pady=20)
ticker_entry = tk.Entry(frame, textvariable=stringvar1, font=('helvetica', 20))
ticker_entry.grid(row=1, column=1)
ticker_entry.focus()

start_lbl = tk.Label(frame, text='Start Date YYYY-MM-DD', bg='#2E8B57', fg='#E9E9E9', font=('Arial', 17))
start_lbl.grid(row=0, column=2)
start_entry = tk.Entry(frame, textvariable=stringvar2, font=('helvetica', 20))
start_entry.grid(row=1, column=2)
start_entry.bind('<KeyRelease>', start_entry_dash)

end_lbl = tk.Label(frame, text='End Date YYYY-MM-DD', bg='#2E8B57', fg='#E9E9E9', font=('Arial', 17))
end_lbl.grid(row=0, column=3)
end_entry = tk.Entry(frame, textvariable=stringvar3, font=('helvetica', 20))
end_entry.grid(row=1, column=3)
end_entry.bind('<KeyRelease>', end_entry_dash)

btn_frame = tk.Frame(root, bg='#2E8B57')
btn_frame.pack(pady=20)
font = ('Arial', 16)

info_btn = tk.Button(btn_frame, text='Current Info', state='disabled', font=font)
info_btn.grid(row=0, column=0, ipadx=5, ipady=7, padx=(0, 20))
info_btn.bind('<Return>', info)
info_btn.bind('<KP_Enter>', info)
info_btn.bind('<Button-1>', info)

chart_btn = tk.Button(btn_frame, text='Chart', state='disabled', font=font)
chart_btn.grid(row=0, column=1, ipadx=20, ipady=7, padx=(0, 20))
chart_btn.bind('<Return>', grapher)
chart_btn.bind('<KP_Enter>', grapher)
chart_btn.bind('<Button-1>', grapher)

clear_btn = tk.Button(btn_frame, text='Clear', font=font)
clear_btn.grid(row=0, column=2, ipadx=25, ipady=7)
clear_btn.bind('<Return>', clear)
clear_btn.bind('<KP_Enter>', clear)
clear_btn.bind('<Button-1>', clear)

scroll_bar_frame = tk.Frame(root)
scroll_bar = tk.Scrollbar(scroll_bar_frame, orient='vertical')
info_box = tk.Text(scroll_bar_frame, yscrollcommand=scroll_bar.set, width=67, height=20, borderwidth=0, wrap='word',
                   state='disabled', font=('Arial', 18))
scroll_bar.config(command=info_box.yview)
scroll_bar.pack(side='right', fill='y')
scroll_bar_frame.pack()
info_box.pack(pady=20)

save_btn = tk.Button(root, text='Save', state='disabled', font=font)
save_btn.pack(pady=20, ipadx=25, ipady=7, )
save_btn.bind('<Return>', save)
save_btn.bind('<KP_Enter>', save)
save_btn.bind('<Button-1>', save)

status_label = tk.Label(root, text='', bd=1, relief='groove', anchor='e', fg='#FF3333', bg='#E9E9E9')
status_label.pack(fill='x', side='bottom', ipady=2)

root.bind('<Command-s>', save)

root.mainloop()
