#Install the following modules in the terminal
'pip install tk' 
'pip install mutagen' 
'pip install pygame'
'pip install pillow'
'pip install lyricsgenius'
'pip install customtkinter'



from tkinter import *
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
from pygame import mixer
import time
from PIL import Image
import customtkinter
import tkinter as tk
import lyricsgenius


class MusicPlayer:
    ''' A simple music play application built using tkinter amd pygame.
        Allow users to choose a music folder, display the list of availabe MP3 files,
        and control music playback(play, pause, next, previous) along with volume control.
        Additionally, the application displays animated GIFs while playing and pausing the music.
        The music player also gives the user the ability to look up the lyrics of a file that is playing.'''
    
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
        

        self.current_index = -1
        
        self.window.protocol("WM_DELETE_WINDOW", self.quit_app)  # Bind the window close event to quit_app
        
        
        mixer.init()

        # file browsing
        open_files = Button(self.window, width=100, height=1, text="Choose Music Folder",
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

        # Lyrics button
        self.lyrics_button = Button(self.window, text="Lyrics", font=("arial", 10, 'bold'), command=self.display_lyrics_window,)
        self.lyrics_button.pack(pady=5)

        # initialize animations
        self.not_listening_animation(self.count)

        # Music slidebar
        self.song_bar = Scale(self.window,
                              from_=0,
                              to=100,
                              width=5,
                              highlightcolor="#0091EA",
                              highlightthickness=0,
                              orient='horizontal',
                              length=685,
                              showvalue=0,
                              troughcolor="#448AFF",
                              sliderlength=12,
                              borderwidth=0,
                              sliderrelief="flat",)
        self.song_bar.place(x=55, y=518)


        # Disable mouse events on the slider
        self.song_bar.bind("<ButtonPress-1>", lambda event: "break")
        self.song_bar.bind("<B1-Motion>", lambda event: "break")

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

        self.lyrics_window_open = False 
        self.lyrics_window = None
        
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
        '''
        Opens a file dialog to choose a music foldeer and displays the list of available MP3 files in the Listbox
        '''
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
        '''
        Plays the selected song from the listbox
        '''
        selected_song = self.musics.get(ACTIVE)
        mixer.music.load(selected_song)
        mixer.music.play()
        if len(selected_song) > 40:
            self.song_name.config(text=selected_song[:40] + ".........")
        else:
            self.song_name.config(text=selected_song)

        self.start_animation()

    def quit_app(self):
        '''
        Function to quit the whole application when the "Quit Application" button is pressed.
        '''
        self.window.destroy()
    
    
    def start_animation(self):
        '''
        Starts the animation.
        '''
        self.count = 0
        self.animation_frame["textvariable"] = '1'
        if self.animation_frame["text"] == "1":
            self.listening_animation(self.count)
            self.animation_frame["text"] = "0"
    
    def Play_music(self):
        '''
        Plays the music but also serves as a restart button when you press the play button.
        '''
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
            self.start_animation() 
    
    
    
   
    def Pause_Unpause(self):
        ''' 
        this is the function for the pause button where click the pause button will resume play from where it left off
        '''
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
        '''
        This function serves as the function for playing the next song when the next button is pressed.
        '''
        total_songs = self.musics.size()
        self.current_index += 1

        if self.current_index >= total_songs:
            # If it's the last song, go to the first song in the playlist
            self.current_index = 0

        next_song = self.musics.get(self.current_index)
        if len(next_song) > 40:
            self.song_name.config(text=next_song[0:40] + ".........")
        else:
            self.song_name.config(text=next_song)

        mixer.music.load(next_song)
        mixer.music.play()

        self.musics.selection_clear(0, END)
        self.musics.activate(self.current_index)
        self.musics.selection_set(self.current_index, last=None)

        self.count = 0
        self.animation_frame["textvariable"] = '1'
        if self.animation_frame["text"] == "1":
            self.listening_animation(self.count)
            self.animation_frame["text"] = "0"
    
    
    
  
    def Prev_song(self):
        '''
        This function is for playing the previous song when the back button is pressed.
        '''
        current_song = self.musics.curselection()
        select = current_song[0] - 1
        total_songs = self.musics.size()

        if select < 0:
            # If it's the first song, go to the last song in the playlist
            select = total_songs - 1

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
    
    
  
    def display_lyrics_window(self):
        '''
        This is the code for displaying the second TkInter window.
        '''
        if not self.lyrics_window_open:
            self.lyrics_window_open = True
            self.lyrics_window = Toplevel(self.window)
            self.lyrics_window.title("Lyrics")
            #self.lyrics_window.protocol("WM_DELETE_WINDOW", self.close_lyrics_window)

        artist_label = Label(self.lyrics_window, text="Artist:")
        artist_label.grid(row=0, column=0, padx=5, pady=5)

        artist_entry = Entry(self.lyrics_window)
        artist_entry.grid(row=0, column=1, padx=5, pady=5)

        song_label = Label(self.lyrics_window, text="Song:")
        song_label.grid(row=1, column=0, padx=5, pady=5)

        song_entry = Entry(self.lyrics_window)
        song_entry.grid(row=1, column=1, padx=5, pady=5)

        lyrics_text = Text(self.lyrics_window, wrap=WORD)
        lyrics_text.grid(row=3, columnspan=2, padx=5, pady=5)

       
        def get_lyrics(artist, song):
            '''
           
           This is the code for setting up the user to get the lyrics from the information inputted.  
           
           '''
            
            # This is the genius API where it pulls the lyrics from genius 
            genius = lyricsgenius.Genius("lJIC8GwL9tSEBTlypIOxHP59tvqZTiZlP9VMm68An0liV1tzRRXtXpDCYetf9H5K")

            try:
                song_info = genius.search_song(song, artist)
                if song_info is not None:
                    return song_info.lyrics
                else:
                    return "Lyrics not found."
            except Exception as e:
                print(f"Error occurred: {e}")
                return "Error occurred while fetching lyrics."

        
        
        def display_lyrics():
            '''
            This code is for displaying the lyrics once the user presses the get lyrics button
            '''
            
            artist = artist_entry.get()
            song = song_entry.get()
            lyrics = get_lyrics(artist, song)
            lyrics_text.delete(1.0, END)
            lyrics_text.insert(END, lyrics)

            # Reset back to False when the lyrics window is closed 
            def on_lyrics_window_close():
                self.lyrics_window_open = False
                self.lyrics_window.destroy()
                self.lyrics_window = None  # Reset the reference to the lyrics window

            self.lyrics_window.protocol("WM_DELETE_WINDOW", on_lyrics_window_close)

        get_lyrics_button = Button(self.lyrics_window, text="Get Lyrics", command=display_lyrics)
        get_lyrics_button.grid(row=2, columnspan=2, padx=5, pady=5)
        
        
        def close_lyrics_window():
            '''
            Code for qutting the lyrics screen
            '''

            self.lyrics_window_open = False
            self.lyrics_window.destroy()
            self.lyrics_window = None

        quit_button = Button(self.lyrics_window, text="Quit", command=close_lyrics_window)
        quit_button.grid(row=4, columnspan=2, padx=5, pady=5)

   
    def Pause(self):
        '''
        Function for pausing the music and changing the animation. The gif will display a different motion when paused. 
        '''
        global paused
        global change_anim
        self.change_anim = 0
        paused = True
        mixer.music.pause()
    
    
    
    def volume(self, vol):
        '''
        This function is for controlling the volume of the music. 
        '''
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
        '''
          This is for dispalying the playing time of the music. 
        '''
        
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

        self.song_bar.set(current_position)

        if int(current_position) == song_len:
            self.Next_song()
        self.song_bar.set(current_position)

        self.time_label_1.after(1000, self.playing_time)
    
    
    
    
    def listening_animation(self, count):
        '''
        Function for the listening animation when you press the play button. 
        The gif will play when you press the play button. 
        '''
        frame_count = self.frame_list1[count]
        self.animation_frame.configure(image=frame_count)
        count += 1
        if count == self.listening_frames:
            count = 0
        if self.animation_frame["textvariable"] == '1':
            self.window.after(30, lambda: self.listening_animation(count))
    
    
    
    
    def not_listening_animation(self, count):
        '''
        Function for the animation when you press the pause button.
        The gif will display the not_listening_animation when you press
        the pause button to stop the music. 
        '''
        frame_count = self.frame_list2[count]
        self.animation_frame.configure(image=frame_count)
        count += 1
        if count == self.not_listening_frames:
            count = 0
        if self.animation_frame["textvariable"] == '0':
            self.window.after(35, lambda: self.not_listening_animation(count))


if __name__ == "__main__":
    music_player = MusicPlayer()
