import pygame
import mutagen
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import filedialog
from typing import List
from PIL import Image, ImageTk
from mutagen.id3 import ID3, APIC

pygame.mixer.init()


class MusicPlayer:
    def __init__(self):
        self.index = 0
        self.playlist: List[Path] = []
        self.volume = 30
        self.is_paused = False
        self.current_song = ''
        pygame.mixer.music.set_volume(self.volume / 100)

    def add_playlist(self, play_list: List[Path]):
        self.playlist = play_list
        if self.playlist:
            self.load_song(self.index)
        #
        print()
        for el in play_list:
            print(el.name[:-4])
        print()

    def load_song(self, i: int):
        if 0 <= i < len(self.playlist):
            song_path = self.playlist[i]
            pygame.mixer.music.load(str(song_path))
            self.current_song = song_path.stem
        else:
            print("Invalid index.")

    def play(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play()

    def pause(self):
        if self.is_playing():
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()

    def next_song(self):
        if self.playlist:
            self.stop()
            self.index = (self.index + 1) % len(self.playlist)
            self.load_song(self.index)
            self.play()

    def prev_song(self):
        if self.playlist:
            self.stop()
            self.index = (self.index - 1) % len(self.playlist)
            self.load_song(self.index)
            self.play()

    def set_volume(self, value: int):
        self.volume = value
        pygame.mixer.music.set_volume(value / 100)

    def is_playing(self):
        return pygame.mixer.music.get_busy()


def get_album_art(song_path: Path):
    try:
        audio = mutagen.File(song_path)
        if audio is not None and 'APIC:' in audio.tags:
            apic = audio.tags['APIC:']  # ID3v2.3+
            return apic.data
        elif audio is not None and isinstance(audio.tags, ID3):
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    return tag.data
    except Exception as e:
        print(f"Error loading album art: {e}")
    return None


def get_music_player(frame: ttk.Frame, btn_width: int = 10):
    # load songs from music player
    music_player = MusicPlayer()

    #
    controls_frame = tk.Frame(frame)
    controls_frame.pack(pady=20)
    
    # album name label
    def update_label(mp: MusicPlayer):
        album_name = load_songs(mp=mp)
        album_name_label.config(text=album_name)
        update_song_label()

    album_name_label = tk.Label(
        controls_frame,
        text='select album'
    )
    album_name_label.pack(pady=(10, 5))

    # song name label
    song_name_label = tk.Label(
        controls_frame,
        text='no song loaded'
    )
    song_name_label.pack(pady=(5, 5))

    # Album art label (image)
    album_art_label = tk.Label(controls_frame)
    album_art_label.pack(pady=(5, 40))

    # Store reference to PhotoImage to avoid garbage collection
    album_art_label.image = None

    def update_album_art():
        album_art_label.config(image='', text='')  # Clear previous
        if music_player.playlist:
            song_path = music_player.playlist[music_player.index]
            art_data = get_album_art(song_path)
            if art_data:
                try:
                    from io import BytesIO
                    image = Image.open(BytesIO(art_data))
                    image = image.resize((200, 200))
                    photo = ImageTk.PhotoImage(image)
                    album_art_label.config(image=photo)
                    album_art_label.image = photo
                except Exception as e:
                    album_art_label.config(text='[No Image]')
                    album_art_label.image = None
            else:
                album_art_label.config(text='[No Image]')
                album_art_label.image = None
        else:
            album_art_label.config(text='[No Image]')
            album_art_label.image = None


    #
    def update_song_label():
        if music_player.playlist:
            song_name_label.config(text=music_player.current_song)
        else:
            song_name_label.config(text='no song loaded')
        update_album_art()

    #
    def next_song():
        music_player.next_song()
        update_song_label()

    def prev_song():
        music_player.prev_song()
        update_song_label()

    def play_song():
        music_player.play()
        update_song_label()

    def stop_song():
        music_player.stop()
        update_song_label()

    load_button = ttk.Button(
        controls_frame, 
        text='load', 
        width=btn_width,
        command=lambda: update_label(mp=music_player)
        )
    prev_button = ttk.Button(
        controls_frame,
        text='previous', 
        width=btn_width, 
        command=prev_song
        )
    next_button = ttk.Button(
        controls_frame, 
        text='next', 
        width=btn_width,
        command=next_song
        )
    play_button = ttk.Button(
        controls_frame, 
        text='play', 
        width=btn_width,
        command=play_song
        )
    pause_button = ttk.Button(
        controls_frame, 
        text='pause', 
        width=btn_width,
        command=stop_song
        )
    
    # set buttons
    load_button.pack(side=tk.LEFT, padx=5, pady=10)
    prev_button.pack(side=tk.LEFT, padx=5, pady=10)
    next_button.pack(side=tk.LEFT, padx=5, pady=10)
    play_button.pack(side=tk.LEFT, padx=5, pady=10)
    pause_button.pack(side=tk.LEFT, padx=5, pady=10)

    # volume slider
    def on_volume_change(value):
        music_player.set_volume(int(float(value)))

    volume_label = tk.Label(frame, text='volume')
    volume_label.pack(pady=(20, 10))
    volume_slider = tk.Scale(
        frame,
        from_=0,
        to=100,
        orient=tk.HORIZONTAL,
        length=600,
        command=on_volume_change
    )
    volume_slider.set(music_player.volume)
    volume_slider.pack(pady=5)


def load_songs(mp: MusicPlayer) -> str:
    my_files = filedialog.askdirectory(
        title='select album folder',
        )
    if my_files:
        my_files = Path(my_files)
        playlist = sorted(my_files.glob("*.mp3"))
        #    
        if playlist:
            mp.add_playlist(playlist)
            return str(my_files.name)
