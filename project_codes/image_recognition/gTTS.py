from gtts import gTTS
from playsound import playsound
import os 

def TextToSpeech(text):
    """
    input : some text or word
    output : sound.mp3 of the text or word

    convert text or word to mp3 file and save to current path
    """
    try :
        currentPath = os.path.dirname(__file__)
        tts = gTTS(str(text))
        tts.save(os.path.join(currentPath,'sound.mp3'))
        playsound(os.path.join(currentPath,'sound.mp3'))
    except :
        print('gTTS Error')
        pass
