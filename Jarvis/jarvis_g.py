import speech_recognition as sr
import pyttsx3
import webbrowser
from gtts import gTTS
import pygame
import os
import time

# Initialize the engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index for different voices

def speak(text):
    print(f"JARVIS: {text}")
    
    # 1. Create the audio file using Google's AI voice
    tts = gTTS(text=text, lang='en', slow=False)
    filename = "voice.mp3"
    tts.save(filename)

    # 2. Initialize pygame mixer and play the file
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # 3. Wait for the audio to finish so it doesn't get cut off
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # 4. Cleanup
    pygame.mixer.music.unload()
    os.remove(filename)

def take_command():
    """Function to listen to microphone input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        return "None"
    return query.lower()

if __name__ == "__main__":
    speak("System online. How can I help you, sir?")
    
    while True:
        query = take_command()

        # Logic for opening websites
        if 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")

        elif 'open facebook' in query:
            speak("Opening Facebook")
            webbrowser.open("facebook.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        elif 'open gmail' in query:
            speak("Opening Gmail")
            webbrowser.open("gmail.com")
        
        elif 'open instagram' in query:
            speak("Opening Instagram")
            webbrowser.open("instagram.com")

        # Logic for opening local files
        elif 'open file' in query:
            # Replace this path with a path to a specific file on your PC
            file_path = "C:\\Users\\YourName\\Documents\\example.txt"
            
            if os.path.exists(file_path):
                speak("Opening the file, sir.")
                os.startfile(file_path)
            else:
                speak("I could not find the file at the specified path.")

        # Exit command
        elif 'go to sleep' in query or 'exit' in query:
            speak("Shutting down systems. Goodbye.")
            break