

# install these in your terminal
#pip3 install pygame  


import time
from tkinter import * 
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from pygame import mixer
import os 



# - add new button
# - fix layout
# - fix image file names (asset folder)



class AudioPlayerApp(Frame):

    def __init__(self, root):
        mixer.init(44100, -16,2,2048)

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

    def addMusic(self, event): 
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
root.mainloop()  # redo inheritance to be able to do this: myapp.mainloop()

'''

image_icon = PhotoImage(file="Music player logo.png")
root.iconphoto(False, image_icon)

#myapp = AudioPlayerApp(root) # create an App object inside the master window

#Menu = PhotoImage(file = "White-Background-PNG-Pic.png")
#Label(root, image = Menu).place(x=0, y=580, width = 485, height = 100)


Frame_Music = Frame(root, bd = 2, relief = RIDGE)
Frame_Music.place (x=0, y=585, width = 485, height = 100 )

#play button ( cant get it to appear)
#ButtonPlay = PhotoImage(file = "play.png")
#Button(root, image = ButtonPlay, bg = "#000000", bd =0, height = 60, width = 60,command = PlayMusic).place(x=215, y= 487)

#Stop Button (square appears)
#ButtonStop = PhotoImage(file= "Stop Button.png")
ButtonStop = PhotoImage(file= "Music player logo.png")
Button(root, image = ButtonStop, bg = "#000000", bd = 0, height =60, width =60, command = mixer.music.stop ).place(x=130, y=487)

#Volume button appears but is to big ( need resizing)
#VolumeButton = PhotoImage(file = "volume-icon-10.png")
VolumeButton = PhotoImage(file = "Music player logo.png")

panel = Label(root, image = VolumeButton).place(x = 20, y = 487)


#Browse Button 
Button(root, text="Browse Music", width=59, height=1, 
             #font=("calibri", 12, "bold"), 
             fg="Black", 
             bg="#FFFFFF", 
             command = AddMusic).place(x=0, y=550)

#scroll bar 
Scroll = Scrollbar (Frame_Music)
Playlist = Listbox(Frame_Music, width = 100, font = ("Times new roman", 10),bg ="#333333", fg= "grey", selectbackground = "lightblue", cursor = "hand2", bd = 0, yscrollcommand = Scroll.set) 

Scroll.config(command = Playlist.yview)
Scroll.pack(side = RIGHT, fill = Y)
Playlist.pack(side = RIGHT, fill = BOTH)


root.mainloop()
'''

