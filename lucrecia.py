## ChatBot Lucrecia
## Interface con reconocimienot de voz y síntesis de voz en Español 
## para LlaMa y el modelo de lenguaje Vicuna 13B
## Libre distribucion 2023 
## Usa el sistema de text-to-speech de Google (gTTS)

import os
import subprocess
import sys
import time
import contextlib
import speech_recognition as sr
import whisper
import pexpect

def speak(text):
    p1= subprocess.Popen(["gtts-cli","-l","es","-t","com.mx",text],stdin=None,stdout=subprocess.PIPE,stderr=None)
    p2= subprocess.Popen(["play","-t","mp3","-"],stdin=p1.stdout,stdout=None,stderr=None)
    p1.stdout.close()
    return p2.communicate()[0]

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

llama_in=""
llama_out=""
child = pexpect.spawn('llama.cpp/main -m llama.cpp/models/vicuna-13B-1.1-GPTQ-4bit-128g.GGML.bin --interactive-first --threads 12 --repeat_last_n 128 --keep -1 -r "User:" -f llama.cpp/prompts/lucrecia.txt', 
    echo=False, 
    encoding='utf-8',
    logfile=sys.stdout,
    timeout=None)
try:
    # Aquí descartamos las partes del prompt inicial 
    # que sirven para dar contexto a la conversación
    child.expect_exact('User:',timeout=15)
    llama_out = child.before
    child.expect_exact('User:',timeout=15)
    llama_out = child.before
    child.expect_exact('User:',timeout=15)
    llama_out = child.before
    child.expect_exact('Lucrecia:',timeout=15)
    llama_out = child.before
    child.expect_exact('User:',timeout=15)
    llama_out = child.before
except:
    llama_out = ""
speak(llama_out)
while True:
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
            model = "medium",
            show_dict=False
            )
        if (llama_in!=''):
            child.sendline(llama_in)
    except sr.UnknownValueError:
        speak("Lo siento, no te he entendido.")
    except sr.RequestError as e:
        speak("Se ha producido un error al transcribir.")
    try: 
        child.expect_exact('Lucrecia:',timeout=15)
        llama_out = child.before
    except:
        llama_out = child.read()
        child.sendcontrol('m')
        child.sendcontrol('j')
    try:
        child.expect_exact('User:',timeout=45)
        llama_out = child.before
    except:
        llama_out = ""
    try:
        speak(llama_out)
    except:
        print("Se ha producido un problema con el sistema de síntesis de voz.")
