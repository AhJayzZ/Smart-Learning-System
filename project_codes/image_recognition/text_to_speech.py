from gtts import gTTS
from pygame import mixer
import os

def TextToSpeech(text):
    """
    input : some text or word
    output : sound.mp3 of the text or word

    Step 1.convert text or word to mp3 file and save to current path
    Step 2.use pygame mixer to play the mp3 file
    """
    try :
        if len(text) > 0:
            mixer.init()
            mixer.music.unload()
            currentPath = os.path.dirname(__file__)
            soundPath = os.path.join(currentPath,'sound.mp3')
            tts = gTTS(str(text))
            tts.save(soundPath)
            mixer.music.load(soundPath)
            mixer.music.play()
        else :
            print('gTTS empty text input')
    except Exception as error:
        print(error)