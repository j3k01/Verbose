from gtts import gTTS
import os
import time

class VoiceHandler:
    def __init__(self, sign):
        self.sign = sign

    def play_sound(self):
        language = 'en'
        if self.sign == 'hello2':
            text = "hello"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("hello.mp3")
            os.system("start hello.mp3")
            time.sleep(5)
        elif self.sign == 'no2':
            text = "no"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("no.mp3")
            os.system("start no.mp3")
            time.sleep(5)
        elif self.sign == 'thanks2':
            text = "thanks"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("thanks.mp3")
            os.system("start thanks.mp3")
            time.sleep(5)
        elif self.sign == 'yes2':
            text = "yes"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("yes.mp3")
            os.system("start yes.mp3")
            time.sleep(5)
        elif self.sign == 'help':
            text = "help"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("help.mp3")
            os.system("start help.mp3")
            time.sleep(5)
        elif self.sign == 'nice':
            text = "nice"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("nice.mp3")
            os.system("start nice.mp3")
            time.sleep(5)
        elif self.sign == 'meet':
            text = "meet"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("meet.mp3")
            os.system("start meet.mp3")
            time.sleep(5)
        elif self.sign == 'you':
            text = "you"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("you.mp3")
            os.system("start you.mp3")
            time.sleep(5)
        elif self.sign == 'ok2':
            text = "ok"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("ok.mp3")
            os.system("start ok.mp3")
            time.sleep(5)
        elif self.sign == 'iloveyou2':
            text = "i love you"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("iloveyou.mp3")
            os.system("start iloveyou.mp3")
            time.sleep(5)
        elif self.sign == 'have':
            text = "have"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("have.mp3")
            os.system("start have.mp3")
            time.sleep(5)
        elif self.sign == 'day':
            text = "day"
            output = gTTS(text=text, lang=language, slow=False)
            output.save("day.mp3")
            os.system("start day.mp3")
            time.sleep(5)
