from tkinter import *
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
from pygame import mixer
import time
from PIL import Image
import customtkinter


class MusicPlayer:
    def __init__(self):
        # Dark and Light Mode
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        # This will create the window for the application
        self.window = Tk()
        self.window.title("Slick Music Player")
        self.window.maxsize(800, 600)
        self.window.minsize(800, 600)
        self.window.configure()

        self.vol = IntVar()
        self.extention = '.mp3'
        self.gif1 = 'Animation/smile2.gif'
        self.gif2 = 'Animation/sad emoji 2.gif'
        self.count = 0
        self.change_anim = 0
        self.motion1 = Image.open(self.gif1)
        self.motion2 = Image.open(self.gif2)

        self.listening_frames = self.motion1.n_frames
        self.not_listening_frames = self.motion2.n_frames

        self.frame_list1 = [PhotoImage(file=self.gif1, format=f'gif -index {i}') for i in range(self.listening_frames)]
        self.frame_list2 = [PhotoImage(file=self.gif2, format=f'gif -index {i}') for i in range(self.not_listening_frames)]
        
        mixer.init()

        # file browsing
        open_files = Button(self.window, width=100, height=1, text="Choose Music Folder", bg="#0091EA", fg='white',
                            font=("arial", 10, 'bold'), command=self.open)
        open_files.pack(padx=10, pady=3)

        # Playlist
        self.musics = Listbox(self.window, width=800, height=15, fg='white', bg='#424242', yscrollcommand=1,
                              borderwidth=1, font=("arial", 9), selectmode=SINGLE)
        self.musics.pack(padx=10)

        # Bind the double-click event to the Listbox
        self.musics.bind("<Double-1>", self.play_selected_song)

        # Frame for animations
        self.animation_frame = Label(self.window, width=800, text="1", height=220, bg='#323232', highlightthickness=0,
                                     textvariable="0")
        self.animation_frame.pack(padx=10, pady=5)

        # initialize animations
        self.not_listening_animation(self.count)

        # Music slidebar
        self.song_bar = Scale(self.window,
                              from_=0,
                              to=100,
                              width=5,
                              cursor="hand2",
                              highlightcolor="#0091EA",
                              highlightthickness=0,
                              orient='horizontal',
                              length=685,
                              showvalue=0,
                              troughcolor="#448AFF",
                              sliderlength=12,
                              borderwidth=0,
                              sliderrelief="flat")
        self.song_bar.place(x=55, y=518)

        # Label to show the position of the song
        self.time_label_1 = Label(self.window, text='', fg="white", bg='#424242', font=("arial", 9))
        self.time_label_1.place(x=10, y=510)
        self.time_label_2 = Label(self.window, fg="white", text='', bg='#424242', font=("arial", 9))
        self.time_label_2.place(x=752, y=510)

        # Frame for the buttons (play, pause, next, and previous buttons)
        Control_frame = Frame(self.window, width=800, height=70, bg='#212121').pack(side=BOTTOM)

        # Photos for icons
        self.play = PhotoImage(file="Icons/Play_button_2.png")
        self.pause = PhotoImage(file="Icons/Pause_button.png")
        self.forward = PhotoImage(file="Icons/next_B.png")
        self.back = PhotoImage(file="Icons/Prev_button.png")
        self.audio = PhotoImage(file="Icons/audio2.png")
        self.mute = PhotoImage(file="Icons/mute2.png")
        self.icon = PhotoImage(file="Icons/music3.png")

        # Creating play button
        self.Play_button = Button(Control_frame, relief=GROOVE, image=self.play, bg='#212121', command=self.Play_music,
                                  textvariable="1", border=0)
        self.Play_button.place(x=400, y=544)

        # Creating pause button
        self.Pause_button = Button(Control_frame, relief=GROOVE, image=self.pause, bg='#212121',
                                   command=self.Pause_Unpause, text="0", textvariable="3", border=0)
        self.Pause_button.place(x=450, y=544)

        # Creating next button
        self.Next_button = Button(Control_frame, relief=GROOVE, image=self.forward, bg='#212121',
                                  command=self.Next_song, border=0)
        self.Next_button.place(x=500, y=544)

        # Creating previous button
        self.Prev_button = Button(Control_frame, relief=GROOVE, image=self.back, bg='#212121',
                                  command=self.Prev_song, border=0)
        self.Prev_button.place(x=350, y=544)

        self.Audio_icon = Label(image=self.audio, bg='#212121')
        self.Audio_icon.place(x=590, y=560)

        # Creating slider to control volume
        self.slider = Scale(
            self.window,
            length=150,
            bg='#212121',
            orient='horizontal',
            variable=self.vol,
            command=self.volume,
            cursor="hand2",
            highlightthickness=0,
            width=8,
            troughcolor="#448AFF",
            highlightcolor="#0091EA",
            sliderlength=12,
            borderwidth=0,
            sliderrelief="flat"
        )
        self.slider.set(50)
        self.slider.place(x=630, y=550)

        self.song_icon_label = Label(Control_frame, image=self.icon, bg='#212121')
        self.song_icon_label.place(x=10, y=544)
        self.song_name = Label(Control_frame, text="", bg='#424242', fg='white')
        self.song_name.place(x=50, y=552.5)

        self.window.mainloop()

    def open(self):
        global path
        global song
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs = os.listdir(path)
            for song in songs:
                if song.endswith(self.extention):
                    self.musics.insert(END, song)

    def play_selected_song(self, event):
        selected_song = self.musics.get(ACTIVE)
        mixer.music.load(selected_song)
        mixer.music.play()

    def Play_music(self):
        music_name = self.musics.get(ACTIVE)
        if len(music_name) > 40:
            self.song_name.config(text=music_name[0:40] + ".........")
        else:
            self.song_name.config(text=music_name)
        self.playing_time()
        mixer.music.load(music_name)
        mixer.music.play()
        self.count = 0
        self.animation_frame["textvariable"] = '1'
        if self.animation_frame["text"] == "1":
            self.listening_animation(self.count)
            self.animation_frame["text"] = "0"

    def Pause_Unpause(self):
        music_name = self.musics.get(ACTIVE)
        if len(music_name) > 40:
            self.song_name.config(text=music_name[0:40] + ".........")
        else:
            self.song_name.config(text=music_name)

        if self.Pause_button['textvariable'] == "3":
            self.Pause()
            self.count = 0
            self.animation_frame["textvariable"] = '0'
            if self.animation_frame["text"] == "0":
                self.not_listening_animation(self.count)
                self.animation_frame["text"] = "1"
            self.Pause_button.config(textvariable="4")

        elif self.Pause_button['textvariable'] == "4":
            self.animation_frame["textvariable"] = '1'
            try:
                paused
            except NameError:
                pass
            else:
                mixer.music.unpause()
                self.count = 0
                if self.animation_frame["text"] == "1":
                    self.listening_animation(self.count)
                    self.animation_frame["text"] = "0"
            self.Pause_button.config(textvariable="3")

    def Next_song(self):
        current_song = self.musics.curselection()
        select = current_song[0] + 1
        next_song = self.musics.get(select)
        if len(next_song) > 40:
            self.song_name.config(text=next_song[0:40] + ".........")
        else:
            self.song_name.config(text=next_song)

        mixer.music.load(next_song)
        mixer.music.play(loops=0)

        self.musics.selection_clear(current_song, END)
        self.musics.activate(select)
        self.musics.selection_set(select, last=NONE)
        self.count = 0
        self.animation_frame["textvariable"] = '1'
        if self.animation_frame["text"] == "1":
            self.listening_animation(self.count)
            self.animation_frame["text"] = "0"

    def Prev_song(self):
        current_song = self.musics.curselection()
        select = current_song[0] - 1
        next_song = self.musics.get(select)
        if len(next_song) > 40:
            self.song_name.config(text=next_song[0:40] + ".........")
        else:
            self.song_name.config(text=next_song)

        mixer.music.load(next_song)
        mixer.music.play()

        self.musics.selection_clear(current_song, END)
        self.musics.activate(select)
        self.musics.selection_set(select, last=None)
        self.count = 0
        self.animation_frame["textvariable"] = '1'
        if self.animation_frame["text"] == "1":
            self.listening_animation(self.count)
            self.animation_frame["text"] = "0"

    def Pause(self):
        global paused
        global change_anim
        self.change_anim = 0
        paused = True
        mixer.music.pause()

    def volume(self, vol):
        Volume = int(vol) / 100
        if Volume >= 0.80:
            self.slider.config(fg='blue')
        else:
            self.slider.config(fg='black')

        if Volume == 0:
            self.Audio_icon.config(image=self.mute)
        else:
            self.Audio_icon.config(image=self.audio)
        mixer.music.set_volume(Volume)

    def playing_time(self):
        current_position = mixer.music.get_pos() / 1000

        converted_time = time.strftime('%M:%S', time.gmtime(current_position))
        self.time_label_1.config(text=converted_time)

        cur_song = self.musics.get(ACTIVE)
        a = MP3(cur_song)
        song_length = a.info.length
        song_len = int(song_length)
        self.song_bar.config(to=song_len)

        converted__song_length = time.strftime('%M:%S', time.gmtime(song_length))
        self.time_label_2.config(text=converted__song_length)

        if int(current_position) == song_len:
            self.Next_song()
        self.song_bar.set(current_position)

        self.time_label_1.after(1000, self.playing_time)

    def listening_animation(self, count):
        frame_count = self.frame_list1[count]
        self.animation_frame.configure(image=frame_count)
        count += 1
        if count == self.listening_frames:
            count = 0
        if self.animation_frame["textvariable"] == '1':
            self.window.after(30, lambda: self.listening_animation(count))

    def not_listening_animation(self, count):
        frame_count = self.frame_list2[count]
        self.animation_frame.configure(image=frame_count)
        count += 1
        if count == self.not_listening_frames:
            count = 0
        if self.animation_frame["textvariable"] == '0':
            self.window.after(35, lambda: self.not_listening_animation(count))


if __name__ == "__main__":
    music_player = MusicPlayer()
