

# install these in your terminal
#pip3 install pygame  
#pip3 install audioplayer # maybe this is better than pygame?
#pip3 install rich

import os 
import time 
from tkinter import * 
from tkinter.filedialog import askdirectory  # TK module for file dialog widgets
from pygame import mixer
mixer.init(44100, -16,2,2048)


# please put all your widgets and callbacks inside a class, this will make things
# easier later!
class AudioPlayerApp(Frame):

    def __init__(self, root):
        self.root = root

        self.lower_frame = Frame(root, bg="white", width=485, height=180 )
        self.lower_frame.place(x=0, y=400)

        # only Class names should start with upper case
        self.music_frame = Frame(root, bd=2 , relief=RIDGE)
        self.music_frame.place(x=0, y=585, width=485, height=100)

        # button 
        self.browse_button = Button(root, text= "Browse Music", width=59, height=1, 
                                    font=("calibri", 14, "bold"), fg="Black", bg="#FFFFFF",
                                    command=self.addMusic)
        self.browse_button.place (x=0, y=550)

        self.scroll = Scrollbar(self.music_frame) 
        self.scroll.pack(side=RIGHT, fill=Y)

        self.file_list = StringVar()
        self.playlist = Listbox(self.music_frame, width=100, font=("Times new roman", 10),
                                bg="#333333", fg="grey", selectbackground="lightblue",
                                listvariable=self.file_list, selectmode=SINGLE,
                                cursor="hand2", bd=0, yscrollcommand=self.scroll.set)

        self.playlist.bind("<Double-Button-1>", self.playMusic)
        self.playlist.pack (side=RIGHT, fill=BOTH)
        self.scroll.config(command=self.playlist.yview)

    def addMusic(self): 
        #path = ("directory code")
        # you could have the user enter

        #if path:
            #os.chdir(path)
        
        # get the path to the music folder from user, ensures that it exists
        self.music_folder = askdirectory(parent=self.root, 
                            initialdir='.',  
                            title="Which folder contains you music files?")

        songs = os.listdir(self.music_folder)
        for song in songs: 
            if song.endswith(".wav"):  # I think pygame can only play .wav (?)
                self.playlist.insert(END, song)
            

    def playMusic(self, event): 
        '''called when 2 x clicked on a list element'''
        music_Name = self.playlist.get(ACTIVE)
        print(self.music_folder + "/" + music_Name)
        mixer.music.load(self.music_folder + "/" + music_Name)
        mixer.music.play()

# run app instance
root = Tk()
root.title("slick music player")
root.geometry("485x700+290+10")
myapp = AudioPlayerApp(root) # create an App object inside the master window
root.mainloop()


'''

lower_frame = Frame(root, bg= "white", width = 485, height = 180 )
lower_frame.place(x=0, y=400)

#image_icon = PhotoImage(file= "Music player logo.png") #Application Icon
#root.iconphoto(False, image_icon)

#Menu = PhotoImage (file = "White background.jpg") #Menu background 
#Label(root, image = Menu).place(x=0, y=580, width = 485, height = 580)

Music_Frame = Frame(root, bd = 2 , relief = RIDGE)
Music_Frame.place(x=0, y=585, width = 485, height = 100)


def AddMusic(): 
    path = ("directory code")
    if path:
        os.chdir(path)
        songs = os.listdir(path)

        for song in songs: 
            if song.endswith(".mp3", ".AAC"):
                self.playlist.insert(END, song)



root.mainloop() 



def PlayMusic(): 
    Music_Name = self.playlist.get(ACTIVE)
    print(Music_Name(ACTIVE))
    mixer.music.load(self.playlist.get(ACTIVE))
    mixer.music.play()

'''