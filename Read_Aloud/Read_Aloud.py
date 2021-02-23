import multiprocessing
import os
import PyPDF2
import pyttsx3
import tkinter as tk
from tkinter import ttk, filedialog


def about():
    top = tk.Toplevel()
    top.title('About')
    top.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

    read_aloud_label = tk.Label(top, text='Read Aloud', fg='#0a69dc', font=('Arial', 20, 'bold'))
    read_aloud_label.pack(pady=(15, 20))
    version_label = tk.Label(top, text='Version 1.0.0', font=font)
    version_label.pack(pady=10)
    copyright_label = tk.Label(top, text='Copyright © 2021 Henry Li', font=font)
    copyright_label.pack(pady=10)
    about_label = tk.Label(top, text='Read Aloud reads pdf files aloud.', font=font)
    about_label.pack(pady=10)


def open_file(event):
    global file, filename
    file = filedialog.askopenfilename(filetypes=(('PDF Files', '*.pdf'),))
    filename = os.path.basename(file)[:55]
    if file:
        status_label.config(text=f'Opened - {filename}', fg='#90EE90')


def stop(event):
    file_menu.entryconfig('Open...    ⌘O', state='normal')
    root.bind('<Command-o>', open_file)
    start_entry.config(state='normal')
    end_entry.config(state='normal')
    stop_lbl.grid_forget()
    play_lbl.grid(row=0, column=0, padx=5)
    voice_option.config(state='enabled')
    rate_scale.state(['!disabled'])
    volume_scale.state(['!disabled'])
    status_label.config(text=f'Stopped - {filename}', fg='#FF4E0D')

    task.terminate()


def play(event):
    global task
    start = int(start_entry.get())
    end = int(end_entry.get())
    if end < start:
        status_label.config(text='Page range must be ascending', fg='#FF4E0D')
        return

    try:
        voice = voices[variable1.get()]
        rate = rate_scale.get()
        volume = volume_scale.get()

        task = multiprocessing.Process(target=message, args=(start, end, voice, rate, volume, file))
        task.daemon = True
        task.start()

        if file:
            status_label.config(text=f'Playing - {filename}', fg='#90EE90')
            play_lbl.grid_forget()
            stop_lbl.grid(row=0, column=0, padx=5)
            file_menu.entryconfig('Open...    ⌘O', state='disabled')
            root.bind('<Command-o>', '')
            start_entry.config(state='disabled')
            end_entry.config(state='disabled')
            voice_option.config(state='disabled')
            rate_scale.state(['disabled'])
            volume_scale.state(['disabled'])

        else:
            status_label.config(text='No file was opened', fg='#FF4E0D')

    except ValueError:
        status_label.config(text='Please input a page range', fg='#FF4E0D')

    except NameError:
        status_label.config(text='Please open a file (⌘O to open)', fg='#FF4E0D')

    except Exception:
        status_label.config(text='There was an error', fg='#FF4E0D')
        return


def message(start, end, voice, rate, volume, file):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    engine.setProperty('voice', voice)

    with open(file, 'rb') as pdf:
        pdfReader = PyPDF2.PdfFileReader(pdf)

        for num in range(max(start - 1, 1), end):
            page = pdfReader.getPage(num)
            text = page.extractText()
            engine.say(text)
            engine.runAndWait()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Read Aloud')

    img = tk.Image("photo", file='Read_Aloud.png')
    root.iconphoto(True, img)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app_width = 550
    app_height = 225
    x = int(screen_width / 2 - app_width / 2)
    y = int(screen_height / 2 - app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    main_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(menu=main_menu, label='Read Aloud')
    main_menu.add_command(label='About', command=about)
    main_menu.add_separator()
    main_menu.add_command(label='Quit        ⌘Q', command=root.quit)

    file_menu = tk.Menu(menu_bar, tearoff=False)
    menu_bar.add_cascade(menu=file_menu, label='File')
    file_menu.add_command(label='Open...    ⌘O', command=lambda: open_file('event'))
    root.bind('<Command-o>', open_file)

    font = ('Arial', 16)

    frame1 = tk.Frame(root)
    frame1.pack(pady=(20, 10))

    voice_lbl = tk.Label(frame1, text='Voice', font=font)
    voice_lbl.grid(row=0, column=0)

    voices = {'': '',
              'Alex': 'com.apple.speech.synthesis.voice.Alex',
              'Daniel': 'com.apple.speech.synthesis.voice.daniel',
              'Fred': 'com.apple.speech.synthesis.voice.Fred',
              'Samantha': 'com.apple.speech.synthesis.voice.samantha',
              'Tessa': 'com.apple.speech.synthesis.voice.tessa',
              'Veena': 'com.apple.speech.synthesis.voice.veena'}

    variable1 = tk.StringVar()
    variable1.set(list(voices.keys())[1])
    voice_option = ttk.OptionMenu(frame1, variable1, *voices.keys())
    voice_option.config(width=7)
    voice_option.grid(row=0, column=1, padx=(0, 195))

    start_label = tk.Label(frame1, text='Pages', font=font)
    start_label.grid(row=0, column=2)
    start_entry = tk.Entry(frame1, width=5)
    start_entry.grid(row=0, column=3)

    end_label = tk.Label(frame1, text='To', font=font)
    end_label.grid(row=0, column=4)
    end_entry = tk.Entry(frame1, width=5)
    end_entry.grid(row=0, column=5)

    frame2 = tk.Frame(root)
    frame2.pack(pady=10)

    rate_image = tk.PhotoImage(file='Rate.png')
    rate_label = tk.Label(frame2, image=rate_image)
    rate_label.grid(row=0, column=0)
    rate_scale = ttk.Scale(frame2, length=145, from_=1, to=300, value=200)
    rate_scale.grid(row=0, column=1, padx=(0, 5))

    sound_image = tk.PhotoImage(file='Volume.png')
    volume_label = tk.Label(frame2, image=sound_image)
    volume_label.grid(row=0, column=2)
    volume_scale = ttk.Scale(frame2, length=315, value=0.25)
    volume_scale.grid(row=0, column=3)

    status_label = tk.Label(root, bg='#0a69dc', font=('Arial', 18))
    status_label.pack(fill='x')

    frame3 = tk.Frame(root)
    frame3.pack(pady=10)

    play_image = tk.PhotoImage(file='Play.png')
    play_lbl = tk.Label(frame3, image=play_image)
    play_lbl.grid(row=0, column=0, padx=5)
    play_lbl.bind('<Button-1>', play)

    stop_image = tk.PhotoImage(file='Stop.png')
    stop_lbl = tk.Label(frame3, image=stop_image)

    stop_lbl.bind('<Button-1>', stop)
    root.bind('<Key-Escape>', stop)

    root.mainloop()
