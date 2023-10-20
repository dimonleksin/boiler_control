
# Import the required module for text  
# to speech conversion 
from gtts import gTTS 
import mp3play
import time

  
# This module is imported so that we can  
# play the converted audio 
import os 

def play(my_text):
    # Language in which you want to convert 
    language ='en'
    
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=my_text, lang=language, slow=False) 
    
    # Saving the converted audio in a mp3 file named 
    # welcome  
    myobj.save("welcome.mp3")
    os.system("ffmpeg welcome.mp3")
    # myobj.write_to_fp(fp)
    # Playing the converted file 
    # m = vlc.MediaPlayer("file:///welcome.mp3")
    # m.play()
    
    return


play("Привет")