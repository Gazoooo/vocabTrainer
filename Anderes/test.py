from gtts import gTTS
from io import BytesIO
from tempfile import TemporaryFile
import pyttsx3

#tts = gTTS(text='Hello', lang='en')
#f = TemporaryFile()
#tts.write_to_fp(f)
# Play f
#f.close()

# mp3_fp = BytesIO()
# tts = gTTS('hello', lang='en')
# tts.write_to_fp(mp3_fp)


engine = pyttsx3.init()
engine.setProperty('rate', 130)
engine.setProperty('volume', 0.2)
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice: %s" % voice.name)
    print(" - ID: %s" % voice.id)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    print("\n")

engine.setProperty('voice', voices[1].id)
engine.say("I will speak this text")
engine.runAndWait()
