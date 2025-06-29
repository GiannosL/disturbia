import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from src import FileManipulationVariables


def run_gui(window_x: int = 400, window_y: int = 300):
    # create application window
    root = tk.Tk()
    root.title('disturbia')
    root.geometry(f'{window_x}x{window_y}')

    # notebook widget in order to create tabs
    notebook = ttk.Notebook(root)
    # empty tabs
    tab0 = ttk.Frame(notebook)
    tab1 = ttk.Frame(notebook)

    # add the frames to the notebook
    notebook.add(tab0, text='music player')
    notebook.add(tab1, text='album')

    # ==== tab 0 content ====

    # ==== tab 1 content ====
    file_info = FileManipulationVariables()
    # page header
    tab_1_title_label = ttk.Label(tab1, text='set album image to .mp3 files')
    tab_1_title_label.pack(pady=10)
    # folder selection button (for .mp3 directory selection)
    folder_select_btn = ttk.Button(
        tab1, 
        text='album song directory', 
        command=lambda: select_folder(btn=folder_select_btn, vars=file_info)
        )
    folder_select_btn.config(width=20)
    folder_select_btn.pack(pady=5)
    # file selection button (for .jpg or .png image)
    file_select_btn = ttk.Button(
        tab1,
        text='album cover file',
        command=lambda: select_file(btn=file_select_btn, vars=file_info)
        )
    file_select_btn.config(width=20)
    file_select_btn.pack(pady=5)


    # pack the notebook widget so it fills the window
    notebook.pack(expand=True, fill='both')

    root.mainloop()


def select_folder(btn: ttk.Button, vars: FileManipulationVariables):
    folder_path = filedialog.askdirectory()
    if folder_path:
        # save result
        vars.album_directory_path = folder_path
        # disable button
        btn.config(text='done!', state='disabled')
        print(vars.album_directory_path)


def select_file(btn: ttk.Button, vars: FileManipulationVariables):
    file_path = filedialog.askopenfilename()
    if file_path:
        vars.album_cover_path = file_path
        btn.config(text='done!', state='disabled')
        print(vars.album_cover_path)
