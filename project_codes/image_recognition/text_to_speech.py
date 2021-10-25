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
        if len(text) > 0:
            currentPath = os.path.dirname(__file__)
            soundPath = os.path.join(currentPath,'sound.mp3')
            tts = gTTS(str(text))
            tts.save(soundPath)
            playsound(soundPath)

            # Avoid error(Permission denied)
            try:
                os.remove(soundPath)
            except:
                pass
        else :
            print('gTTS empty text input')
    except :
        print('gTTS error occured')
        pass