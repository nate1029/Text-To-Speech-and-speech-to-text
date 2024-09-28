import os
from gtts import gTTS

def text_to_speech(text, language='en'):
    """
    Convert text to speech and save as an mp3 file
    """
    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

# Example usage:
text_to_speech("Hello, world!")