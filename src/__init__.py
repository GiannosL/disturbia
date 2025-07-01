import tkinter as tk


class FileManipulationVariables:
    def __init__(self):
        # path to directory and file
        self.album_directory_path = ''
        self.album_cover_path = ''
        self.year = tk.StringVar(value='1997')

        # image mime: 'image/jpeg' or 'image/png'
        self.image_mime = tk.StringVar(value='image/jpeg')
