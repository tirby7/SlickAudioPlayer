from tkinter import * 
from tkinter import filedialog
import os
from mutagen.mp3 import MP3 
from PIL import Image
import customtkinter
from pygame import mixer 
import time






#Dark and Light Mode
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

#The Window
window = Tk() 
window.title("Slick Music Player")
window.maxsize(800, 600)
window.minsize(800,600)
window.configure(bg='#323232')

vol = IntVar()
extention ='mp3'
gif1 = 'assets/music.gif'
gif2 = 'assets/sad.gif'
count = 0 
change_anim = 0

#function to browse music folders 
def open():
    global path 
    global song 
    path = filedialog.askdirectory() 
    if path:
        os.chidir(path)
        songs = os.listdir(path)
        for song in songs: 
            if song.endswith(extention):
                musics.insert(END, song)

#Pause and unpase buttons 
def Pause_Unpause():
    global music_name
    global count
    music_name = musics.get(ACTIVE)
    if len(music_name)>40: 
        song_name.config(text = music_name[0:40] + '..........')
    else: 
        song_name.config(text = music_name)
    
    if(Pause_button['textvariable']=="3"):
        Pause()
        count = 0 
        animation_frame["textvariable"] = '0'
        if animation_frame["text"] =="0": 
            not_listening_animation(count)
            animation_frame["text"] = "1"
    
    elif(Pause_button['textvariable']=="4"):
        animation_frame["textvarialbe"] = '1'
        try: 
            paused
        except NameError:
            pass
        else: 
            mixer.music.unpause() 
            count= 0 
            if animation_frame["text"] =="1":
                listeming_animation(count)
            animation_frame['text']="0"
        Pause_button.config(textvariable="3")


#function that will play the music
def Play_song(): 
    global count
    music_name= musics.get(ACTIVE)
    if len(music_name) >40:
        song_name.config(text = music_name[0:40] + ".........")
    else:  
        song_name.config(text = music_name)
    playing_time()
    mixer.music.load(music_name)
    mixer.music.play() 
    count = 0 
    animation_frame["textvariable"] = '1'
    if animation_frame["text"] == "1":
        listeming_animation(count)
        animation_frame["text"] = "0"


#Next song function 
def Next_song(): 
    current_song = musics.curselection() 
    select = current_song[0] + 1 
    next_song = musics.get(select)
    if len(next_song) > 40: 
        song_name.config(text = next_song[0:40] + ".........")
    else: 
        song_name.config(text = next_song)
    
    mixer.music.load(next_song)
    mixer.music.play(loops=0)

    musics.selection_clear(current_song, END)
    musics.activate(select)
    musics.selection_set(select, last=None)
    count = 0 
    animation_frame["textvariable"] = '1' 
    if animation_frame["text"] == "1":
        listeming_animation(count)
        animation_frame["text"] = "0"

# function for previous song
def Prev_song():
    current_song= musics.curselection()
    select = current_song[0] - 1
    next_song = musics.get(select)
    if len(next_song) > 40:
         song_name.config(text =next_song[0:40] + ".........")
    else:
         song_name.config(text = next_song) 
    
    mixer.music.load(next_song)
    mixer.music.play()

    musics.selection_clear(current_song, END)
    musics.activate(select)
    musics.selection_set(select, last=None)
    count = 0
    animation_frame["textvariable"] = '1'
    if animation_frame["text"] == "1":
       listeming_animation(count)
       animation_frame["text"] = "0"


#this is the pause fucntion to pause the songs 
def Pause():
    global paused 
    global change_anim
    change_anim = 0
    paused = TRUE
    mixer.music.pause()   

#function to control the volume of the files 
def volum(vol): 
    Volume = int(vol)/100
    if Volume >=0.80: 
        slider.config(fg='blue')
    else: slider.config(fg='blue')

    if Volume == 0: 
        Audio_icon.config(image = mute)
    else: Audio_icon.config(image = audio)
    mixer.music.set_volume(Volume)


#This functin shows the positon of the song playing 
def playing_time():
    current_positon = mixer.music.get_pos()/1000

    converted_time = time.strftime('%M:%S', time.gmtime(current_positon))
    time_label_1.config(text = converted_time)

    cur_song = musics.get(ACTIVE)
    a = MP3(cur_song)
    song_length = a.info.length
    song_len = int(song_length)
    song_bar.config(to = song_len)

    converted__song_length = time.strftime('%M:%S', time.gmtime(song_length))
    time_label_2.config(text = converted__song_length)

    if int(current_positon) == song_len: 
        Next_song() 
        song_bar.set(current_positon)

        time_label_1.after(1000, playing_time)


# this involves the gifs and having them display when the music is playing or not playing 
image1 = Image.open(gif1)
image2 = Image.open(gif2)

listening_frames = image1.n_frames
not_listening_frames = image2.n_frames

frame_list1 = [PhotoImage(file = gif1,  format=f'gif -index {i}') for i in range(listening_frames)]
frame_list2 = [PhotoImage(file = gif2, format=f'gif -index {i}') for i in range(not_listening_frames)]

# function for getting the happy gif to display when the music playing 
def listeming_animation(count): 
    frame_count = frame_list1[count]
    animation_frame.configure(image = frame_count)
    count +=1
    if count == listening_frames:
        count = 0 
    if animation_frame["textvariable"] == '1': 
        window.after(30, lambda: listeming_animation(count))

# this animation is for the gif that will play when music is not playing

def not_listening_animation(count):
    frame_count = frame_list2[count]
    animation_frame.configure(image = frame_count)
    count +=1 
    if count == not_listening_frames:
        count = 0 
    if animation_frame["textvariable"] == '0':

        window.after(35, lambda: not_listening_animation(count))

#create file browser button which will locate the files to play the music from 

open_files = Button(window, width = 100, height =1, text= "Choose Music", bg= "#0091EA", fg='white', font=("arial", 10, 'bold'), command=open)



# Creating playlist
musics = Listbox(window, width=800, height=15 , fg= 'white', bg='#424242', yscrollcommand=1, borderwidth=1, font=("arial", 9), selectmode=SINGLE)
musics.pack(padx=10)


#Frame  for animations 

smile = PhotoImage(file = "assets/music.gif")
animation_frame = Label(window, width=800, text = "1", height=220, bg= '#323232',  highlightthickness=0, textvariable="0")
animation_frame.pack(padx=10, pady=5)

not_listening_animation(count)


#Slide bar for the music

song_bar = Scale(window, 
   from_=0,
   to= 100,
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
song_bar.place(x = 55, y = 518)

# This piece of code is usted to tell the audio postions (time labels)
time_label_1 = Label(window, text='', fg = "white", bg='#424242', font=("arial", 9))
time_label_1.place(x = 10, y = 510)
time_label_2 = Label(window, fg = "white", text='', bg='#424242', font=("arial", 9))
time_label_2.place(x = 752, y = 510)

#This frame is used to place the play button, pause button and the other buttons
Control_frame = Frame(window, width=800, height=70, bg='#212121').pack(side=BOTTOM)


#icons that will appear in the application 
Play_Button = PhotoImage(file ="img2/play_button.png")
Pause_Button = PhotoImage(file = "img2/pause.png")
Next_Button = PhotoImage(file= "img2/next.png")
Previous_Button = PhotoImage(file= "img2/previous.png")
Stop_Button = PhotoImage(file= "img2/Stop_button.png")
song_icon = PhotoImage(file = "img2/Music_player_logo.png")
audio = PhotoImage(file= "img2/audio.png")
mute = PhotoImage(file= 'img2/mute.png')


# creating play button
Play_button = Button(Control_frame, relief= GROOVE, image=Play_Button, bg='#212121', command= Play_song, textvariable = "1", border=0, text = "1")
Play_button.place(x = 400, y = 544 )

# creating pause button
Pause_button = Button(Control_frame,  relief= GROOVE, image=Pause_Button, bg='#212121', command=Pause_Unpause, text = "0", textvariable = "3", border=0)
Pause_button.place(x = 450, y = 544 )

# creating next button
Next_button = Button(Control_frame, relief= GROOVE, image=Next_Button, bg='#212121', command=Next_song, border=0)
Next_button.place(x = 500, y = 544)

# creating previous button
Prev_button = Button(Control_frame, relief= GROOVE, image=Previous_Button, bg='#212121', command=Prev_song, border=0)
Prev_button.place(x = 350, y = 544)

Audio_icon = Label(image= audio, bg = '#212121')
Audio_icon.place(x = 590, y = 560)


#slide bar to control volume


# Creating slider to control volume
slider = Scale(
    window,
    length=150, 
    bg='#212121',
    orient='horizontal', 
    variable=vol, 
    command=volum, 
    cursor="hand2",  
    highlightthickness= 0,
    width=8,
    troughcolor="#448AFF",
    highlightcolor="#0091EA", 
    sliderlength=12, 
    borderwidth=0,
    sliderrelief="flat"
    )
slider.set(50)
slider.place(x = 630, y = 550)

song_icon_label = Label(Control_frame, image=song_icon, bg='#212121')
song_icon_label.place(x = 10, y = 544)
song_name = Label(Control_frame, text = "", bg='#424242', fg='white')
song_name.place(x = 50, y = 552.5)

window.mainloop()