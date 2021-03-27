import tkinter as tk
from random import choice, randint, sample


def quit(event):
    root.quit()


def pw_generator():
    if Var1.get() == 1 or Var2.get() == 1 or Var3.get() == 1 or Var4.get() == 1:
        try:
            copy_btn.config(state='normal')
            pw_entry.delete(0, 'end')
            status_label.config(text='')

            pw_length = int(my_entry.get())

            password = ''
            x = 0
            while True:
                if Var1.get() == 1:
                    password += chr(randint(65, 90))
                    x += 1
                    if len(password) >= pw_length:
                        break
                if Var2.get() == 1:
                    password += chr(randint(97, 122))
                    x += 1
                    if len(password) >= pw_length:
                        break
                if Var3.get() == 1:
                    password += chr(randint(48, 57))
                    x += 1
                    if len(password) >= pw_length:
                        break
                if Var4.get() == 1:
                    password += chr(randint(*choice([(33, 47), (58, 64), (91, 96), (123, 126)])))
                    x += 1
                    if len(password) >= pw_length:
                        break

            password = "".join(sample(password, len(password)))
            pw_entry.insert(0, password)

        except ValueError:
            status_label.config(text='Number of characters should an integer', fg='#FF3333')
    else:
        status_label.config(text='Please choose a modifier', fg='#FF3333')


def copy():
    copy_btn.config(state='disabled')
    status_label.config(text='Copied to clipboard', fg='green')

    root.clipboard_clear()
    root.clipboard_append(pw_entry.get())


root = tk.Tk()
root.title('Password Generator')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 370
app_height = 330
x = screen_width / 2 - app_width / 2
y = screen_height / 2 - app_height / 2
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

Lbl_frame_1 = tk.LabelFrame(root, text='Modifiers', labelanchor='n')
Lbl_frame_1.pack(pady=10)

Var1 = tk.IntVar()
Var2 = tk.IntVar()
Var3 = tk.IntVar()
Var4 = tk.IntVar()

ChkBtn_1 = tk.Checkbutton(Lbl_frame_1, text='A–Z', width=7, variable=Var1)
ChkBtn_1.grid(row=0, column=0, pady=5)

ChkBt_2 = tk.Checkbutton(Lbl_frame_1, text='a–z', width=7, variable=Var2)
ChkBt_2.grid(row=0, column=1, pady=5)

ChkBtn_3 = tk.Checkbutton(Lbl_frame_1, text='0–9', width=7, variable=Var3)
ChkBtn_3.grid(row=0, column=2, pady=5)

ChkBt_4 = tk.Checkbutton(Lbl_frame_1, text='Special', width=7, variable=Var4)
ChkBt_4.grid(row=0, column=3, pady=5)

Lbl_frame_2 = tk.LabelFrame(root, text='Number of Characters', labelanchor='n')
Lbl_frame_2.pack(pady=10)

my_entry = tk.Entry(Lbl_frame_2, font=('Arial', 20), width=10)
my_entry.pack(pady=20, padx=20)

pw_entry = tk.Entry(root, text='', font=('Arial', 20), bd=0, bg='systembuttonface', justify='center', width=23)
pw_entry.pack(pady=10)

frame_1 = tk.Frame(root)
frame_1.pack()

generate_btn = tk.Button(frame_1, text='Generate Password', command=pw_generator)
generate_btn.grid(row=0, column=0, padx=10)

copy_btn = tk.Button(frame_1, text='Copy', state='disabled', command=copy)
copy_btn.grid(row=0, column=1, padx=10)

status_label = tk.Label(root, text='', bd=1, relief='ridge', anchor='e', bg='#E9E9E9')
status_label.pack(fill='x', side='bottom', ipady=2)

root.bind('<Control-q>', quit)

root.mainloop()
