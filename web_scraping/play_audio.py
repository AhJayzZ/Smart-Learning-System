from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_mp3("fish-ame_pr_url.mp3")
play(sound)
 