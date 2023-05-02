import pyttsx3

engine = pyttsx3.init("espeak")
voices = engine.getProperty('voices')
print(voices)

n=0
while not(voices[n].id=="Spanish_(Spain)"): 
    n=n+1

engine.setProperty('voice',voices[n].id) #Spanish_(Spain)
engine.setProperty('rate',105)






def speak(text):
    engine.say(text)
    engine.runAndWait()

speak ("Hola mundo esto es una prueba")