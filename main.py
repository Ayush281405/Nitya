import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your Key Here>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# initialize the recognizer 
#recognizer = sr.Recognizer()

# function to make the assistant speak
#def speak(text):
#   engine = pyttsx3.init()
#   engine.say(text)
#   engine.runAndWait()
#  engine.stop()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    
     
# openai api key
def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Nitya skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


# function to process commands
def process_command(c):
    if 'open youtube' in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://music.youtube.com/watch?v=0jBNe7IVBAI&si=uZzVk4FYoDViGhKb&feature=xapp_share")
    elif 'open instagram' in c.lower():
        speak("Opening instagram")
        webbrowser.open("https://www.instagram.com/p/DBOq_ilTkCX/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link= musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # OpenAI handling the request
        output = aiProcess(c)
        speak(output) 

# main loop
if __name__ == "__main__":
    print("Initializing Nitya...")
    speak("Initializing Nitya...")
    #print("At last,")
    #print("after endless lifetimes of wandering.....,you have found me,") 
    #speak("At last,")
    #speak("after endless lifetimes of wandering.....,you have found me,") 
    speak("Say 'HELLO' to activate me...")

    while True:
# Obtaining audio from the microphone
        r=sr.Recognizer()
    
        print("listening...")
        try: 
            with sr.Microphone() as source:
                print("Say Hello to activate me...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "hello".lower()):
                if first_time := True:
                        speak("Hello Sakhi, I am Nitya, your virtual assistant.")
                        #speak("Great ! Guru Kripa Kevalam...")
                        #speak("Saancho Ekk Radharaman...Juto Baaki Sansaar")
                        first_time = False
                
                # listening for the next command after wake word
                with sr.Microphone() as source:
                    print("Nitya is active now...?")
                    speak("How can I help you today...?")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    process_command(command)
                    

        except Exception as e:
            print("Error; {0}".format(e))
