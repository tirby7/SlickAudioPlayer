import time 
from os import path, walk
import os

#working with audio files 
import eyed3 
from mutagen.wave import WAVE

import pygame 

pygame.mixer.init() # CH was missing ()!

Play:bool = True # should be a class var


def get_tags(song_path):
    audio_file = eyed3.load(song_path)
    img= None
    if audio_file is not None: 
        titre = audio_file.tag.title or 'Unknown'
        album_name = audio_file.tag.album or 'Unkown'
        artist_name = audio_file.tag.artist or 'Unknown'
    else:
        titre = song_path.split("/")[-1].split(".")[0]
        album_name="Unkown"
        artist_name="Unkown"
    return titre, album_name, artist_name
    
def play(song_path): 
    pygame.mixer.music.load(song_path)
    pygame.mixer_music.play() 
    #audio = WAVE (song_path)  # CH
    #return audio.info.length  # CH

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
        Play = True 
        pygame.mixer.music.unpause() # CH again, missing ()!!!!!!
    return Play  # Why return if its a global var (or better class var) anyway

def find_audio_file(search_path):
    file_dict: dict = {}
    tag_dict = {}
    print(os.listdir(search_path)) # DEBUG
    for root, _, files in walk(search_path):
        for file in files:
            #if ".wav" in file: # CH commented out to test mp3 files
                audio_file = path.join(root, file) 
                titre, album, artist = get_tags(audio_file)
                file_dict[f"{titre} {album} {artist}"] = audio_file
                tag_dict[audio_file] = eyed3.load(audio_file)
    return file_dict, tag_dict




# this won't be run when the file is included, so put your tests here!
if __name__ == "__main__":

    filedict, tag_dict = find_audio_file("music_files")
    
    # make a list of IDs from the keys
    song_ID_list = list(filedict.keys())
    print(song_ID_list)

    # selecy a song from list
    song_key = song_ID_list[3]
    path_to_song = filedict[song_key]
    song_tag = tag_dict[path_to_song]
    duration_secs = song_tag.info.time_secs
    print(song_key, path_to_song, duration_secs)

    # play first song
    play(path_to_song)

    
    time.sleep(1)
    print("pause on")
    pause()
    time.sleep(1)
    print("pause off")
    pause()
    time.sleep(10)

    