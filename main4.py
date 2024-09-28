import os
import wave
import pyaudio
import speech_recognition as sr
from gtts import gTTS
from fpdf import FPDF
from playsound import playsound

# Constants for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

def text_to_speech(text, language='en'):
    """Convert text to speech and save as an mp3 file."""
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("output.mp3")
        # Play the audio file directly
        playsound("output.mp3")
    except Exception as e:
        print(f"Error in text to speech: {e}")

def speech_to_text():
    """Convert speech to text."""
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording audio...")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    r = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text  # Return recognized text for further use
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand your audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def save_to_pdf(text, filename='output.pdf'):
    """Save the given text to a PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split text into lines to avoid overflow
    for line in text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
    print(f"Saved to {filename}")

# Main function
if __name__ == "__main__":
    question = "Which one among the seven wonders is present in India?"
    text_to_speech(question)
    recognized_text = speech_to_text()
    
    if recognized_text:
        save_to_pdf(recognized_text)
