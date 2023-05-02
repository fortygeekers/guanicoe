import os
import sys
import time
import contextlib
import speech_recognition as sr
import whisper
import pyttsx3

def init_tts():
    global tts_engine 
    tts_engine = pyttsx3.init("espeak")
    voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice',voices[31].id) #Spanish_(Spain)
    tts_engine.setProperty('rate',105)

def speak(text):
    global tts_engine
    print(text)
    tts_engine.say(text)
    tts_engine.runAndWait()

@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

# ____main____
init_tts()
try:
    with ignoreStderr():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(">")
            speak("")
            audio_data = r.listen(source)
except:
    speak ("Algo falla con el micrófono.")

try:
    print(r.recognize_whisper(audio_data, 
        language="spanish",
        model = "base",
        show_dict=False
        ))
except sr.UnknownValueError:
    speak("Lo siento, no te he entendido.")
except sr.RequestError as e:
    speak("Se ha producido un error al transcribir.")
