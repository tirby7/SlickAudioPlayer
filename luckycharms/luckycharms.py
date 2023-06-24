import time 
from os import path, walk 

#working with audio files 
import eyed3 
from mutagen.wave import WAVE

import pygame 

pygame.mixer.init

Play:bool = True





def get_tags(song_path):
    audio_file = eyed3.load(song_path)
    img= None
    if audio_file is not None: 
        titre = audio_file.tag.title or 'Unknown'
        album_name = audio_file.tag.album or 'Unkown'
        artist_name = audio_file.tag.artist or 'Unknown'
        album_image = audio_file.tag.images
        for image in album_image:
            img - image.image_data
    else:
        titre = song_path.split("/")[-1].split(".")[0]
        album_name="Unkown"
        artist_name="Unkown"
    return titre, album_name, artist_name, img

def play(song_path): 
    pygame.mixer.music.load(song_path)
    pygame.mixer_music.play() 
    audio = WAVE (song_path)
    return audio.info.length

def set_postion(position): 
    pygame.mixer.music.set_pos(position)
    

def get_position(): 
   position = pygame.mixer.music.get_pos()/1000
   position_as_time_format = time.strftime ("%M:%S", time.gmtime(position))
   return position, position_as_time_format

def pause(): 
    global Play
    if Play: 
        Play = False 
        pygame.mixer.music.pause()
    else: 
        PLAY = True 
        pygame.mixer.music.unpause
    return PLAY

def find_audio_file(search_path):
    file_dict: dict = {}
    for root, _, files in walk(search_path):
        for file in files:
            if ".wav" in file:
                audio_file = path.join(root, file)
                titre, album, artist, _ = get_tags(audio_file)
                file_dict[f"{titre} {album} {artist}"] = audio_file
    return file_dict