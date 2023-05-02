import os
import sys
import time
import contextlib
import speech_recognition as sr
import whisper
import pyttsx3     
import pexpect

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

# Hilo Principal
init_tts()


child = pexpect.spawn('llama.cpp/main -m llama.cpp/models/vicuna-13B-1.1-GPTQ-4bit-128g.GGML.bin --repeat_penalty 1.0 -i -r "User:" -f llama.cpp/prompts/chat-with-bob.txt')
speak("Hola soy Bob y estoy aquí para ayudarte.")
child.expect('User:', timeout=30)
time.sleep(30)
llama_out=child.before
llama_in=""
while True:
    try: 
        child.expect('User:')
        llama_out = child.before
        child.sendline(llama_in)
    except:
        pass
    try:
        speak(llama_out)
    except:
        print("Se ha producido un problema con el sistema de síntesis de voz.")
    try:                
        with ignoreStderr():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                    audio_data = r.listen(source)
    except:
        speak("Algo ha fallado con el reconocimiento de voz.")
    try:
        llama_in = r.recognize_whisper(audio_data, 
            language="spanish",
            model = "base",
            show_dict=False
            )
        print (llama_in)    
    except sr.UnknownValueError:
        speak("Lo siento, no te he entendido.")
    except sr.RequestError as e:
        speak("Se ha producido un error al transcribir.")
