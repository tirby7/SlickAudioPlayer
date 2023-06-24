from tkinter import * 
import PIL 
import customtkinter
from luckycharms import luckycharms 


#Dark and Light Mode
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")




class SlickMusicPlayer(customtkinter.CTk):
    def __init__(self): 
        super().__init__()
        self.title(" Slick Music Player")
        self.geometry('1000x500')
        self.__titre_text = StringVar()
        self.__play_image = PhotoImage(file="img/play.png")
        self.__pause_image = PhotoImage(file="img/stop_button.png")
        self.__next_image = PhotoImage(file="img/forward_button.png")
        self.__back_image = PhotoImage(file="img/backward_button.png")
        self.__album_image = customtkinter.CTkImage(PIL.Image.open
                                                    ("img/Music_player_logo.png"),
                                                size =(150,150) )    
        self.__play_status: bool = False
        self.__theme: str= "white"
        self.__activate_now: int= 0
        self.__scrolloff:int = 8 

        self.__position = 0 
        
     
       

        self.__container = customtkinter.CTkFrame(self)

        self.__left_frame = customtkinter.CTkFrame(self.__container)
        
        self.__search_frame= customtkinter.CTkFrame(self.__left_frame)
        self.__search_entry = customtkinter.CTkEntry(
            self.__search_frame, placeholder_text= "search"
        )
        self.__search_entry.pack(fill="x", side="left", expand=1)
        self.__search_frame.pack(fill="x", pady=5)
        self.__scrollbar = customtkinter.CTkScrollbar(self.__left_frame)
        self.__scrollbar.pack(side="left", fill="y")
        self.__music_listbox = Listbox(
            self.__left_frame,
            bg="white",
            fg="gray",
            height=80,
            width=60,
            selectbackground="black",
            selectforeground="white",
            yscrollcommand=self.__scrollbar.set,
        )
        self.__music_listbox.pack(fill="x")
        self.__scrollbar.configure(command=self.__music_listbox.yview)
        self.__music_listbox.pack(fill="x")
        self.__scrollbar.configure(command=self.__music_listbox.yview)

        
        


        self.__left_frame.pack(pady=20, side="left", fill="y", padx=5)

        self.__right_frame = customtkinter.CTkFrame(self.__container)
        self.__titre_text = StringVar()
        self.__titre = customtkinter.CTkLabel(
            self.__right_frame, textvariable=self.__titre_text
        ).pack(pady=50)
        self.__image_music = customtkinter.CTkLabel(
            self.__right_frame, text="", image=self.__album_image
        )
        self.__image_music.pack()

        self.__right_frame_bottom=customtkinter.CTkLabel(self.__right_frame)

        self.__frame_center_button = customtkinter.CTkFrame(self.__right_frame_bottom)
        Button(
            self.__frame_center_button,
            text=None,
            relief="groove",
            borderwidth=0,
            command=self.back,
            image=self.__back_image, 
        ).pack(side="left")
        self.__play_button = Button(
            self.__frame_center_button,
            text="",
            relief="groove",
            command=self.play, 
            image= self.__play_image, 
        )
        self.__play_button.pack(padx=10, side="left")
        Button(
            self.__frame_center_button,
            text="",
            relief="groove",
            borderwidth=0,
            command=self.next,
            image=self.__next_image,
        ).pack(side="left")


        self.__right_frame_bottom.pack(side="bottom", pady=10)

        self.scale = customtkinter.CTkSlider(
            self.__right_frame, command= lambda x: (self.change_position(x))
        )
        self.scale.pack(side="bottom", fill="x", ipadx=150, pady=10)

        self.__right_frame.pack(side="right", fill="y", expand=1, padx=5)

        self.__container.pack(fill="y", anchor="sw")

        self.__music_listbox.bind("<Double-Button-1>", lambda x: self.select_item_in_listbox(x))
        self.__search_entry.bind("<KeyRelease>", self.search)

        self.play_time()

    def music_now(self, index):
            key = self.__music_listbox.get(index)

    def update_title_and_image(self,index):
            titre, _, artist, image = luckycharms.get_tags(self.music_now(index))
    
    def update_title_and_image(self, index) -> None:
        titre, _, artist, image = luckycharms.get_tags(self.music_now(index))

        if image is not None:
            with open(".tmp.jpg", "wb") as file:
                file.write(image)
            image = customtkinter.CTkImage(PIL.Image.open(".tmp.jpg"), size=(250, 230))
        else:
            image = self.__album_image

        self.__image_music.configure(image=image)
        self.__titre_text.set(f"{titre} {artist}")
    def change_position(self, position: float):
        luckycharms.set_position(position)
        self.__position = position

    def play_time(self):
        if self.__play_status:
            self.__position += 1
            _, time_left = luckycharms.get_position()
            self.scale.set(self.__position)
            if time_left == "59:59":
                self.next()
        self.after(1000, self.play_time)


    def play(self, index):
        self.__play_status = True
        total_len_music = len(self.__music_listbox.get(0, "end"))
        if index == total_len_music:
            index = 0
        song = self.music_now(index)
        self.scale._to = luckycharms.play(song)
        self.scale.set(0)
        self.__position = 0
        self.__play_button.config(image=self.__pause_image, command=self.pause)
        self.__music_listbox.selection_clear(0, "end")
        self.__music_listbox.activate(index)
        self.__music_listbox.selection_set(index, last=None)
        self.__activate_now: int = self.__music_listbox.curselection()[0]
        self.__music_listbox.yview(
            "moveto", (self.__activate_now - self.__scrolloff) / total_len_music,
        )  
        self.update_title_and_image(self.__activate_now)

    def pause(self):
        if self.__play_status:
            self.__play_button.config(image=self.__play_image)
        else:
            self.__play_button.config(image=self.__pause_image)
        self.__play_status: bool = luckycharms.pause()

    def next(self) -> None:
        self.__activate_now += 1
        self.play(self.__activate_now)

    def back(self): 
        self.__activate_now -= 1
        self.play(self.__activate_now)

    def select_item_in_listbox(self) -> None:
        self.play()

    def update_music_listbox(self, data):
        self.__music_listbox.delete(0, "end")
        for result in data:
            self.__music_listbox.insert("end", result)

    def search(self):
        search_output = self.__search_entry.get()
        search_result = [
            title
            for title in self.__all_WAVE_title
            if search_output.lower() in title.lower()
        ]
        self.update_music_listbox(search_result)








app = SlickMusicPlayer() 
app.mainloop() 



        
