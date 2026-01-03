import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import subprocess
import platform

class Jarvis:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0-1)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
        # Set voice (optional - uses default system voice)
        voices = self.engine.getProperty('voices')
        # Try to use a male voice (usually index 0)
        if len(voices) > 0:
            self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"JARVIS: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen to user's voice command"""
        with sr.Microphone() as source:
            print("\nListening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing...")
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you please repeat?")
                return ""
            except sr.RequestError:
                self.speak("Sorry, there seems to be an issue with the speech recognition service.")
                return ""
    
    def open_youtube(self):
        """Open YouTube in default browser"""
        self.speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    
    def open_facebook(self):
        """Open Facebook in default browser"""
        self.speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    
    def open_website(self, url):
        """Open any website"""
        self.speak(f"Opening {url}")
        if not url.startswith('http'):
            url = 'https://' + url
        webbrowser.open(url)
    
    def open_file(self, filepath):
        """Open any file on the PC"""
        try:
            if os.path.exists(filepath):
                self.speak(f"Opening {os.path.basename(filepath)}")
                
                # Use platform-specific file opening
                if platform.system() == 'Windows':
                    os.startfile(filepath)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', filepath])
                else:  # Linux
                    subprocess.call(['xdg-open', filepath])
                return True
            else:
                self.speak("Sorry, I couldn't find that file.")
                return False
        except Exception as e:
            self.speak("Sorry, I encountered an error opening the file.")
            print(f"Error: {e}")
            return False
    
    def search_and_open_file(self, filename):
        """Search for a file in common locations"""
        # Common search directories
        search_paths = [
            os.path.expanduser("~"),  # Home directory
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
        ]
        
        for search_path in search_paths:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if filename.lower() in file.lower():
                        filepath = os.path.join(root, file)
                        self.speak(f"Found {file}")
                        return self.open_file(filepath)
        
        self.speak(f"Sorry, I couldn't find {filename} on your computer.")
        return False
    
    def get_time(self):
        """Tell current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
    
    def get_date(self):
        """Tell current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today is {current_date}")
    
    def process_command(self, command):
        """Process user command and execute appropriate action"""
        if not command:
            return True
        
        # Exit commands
        if any(word in command for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # YouTube
        elif 'youtube' in command:
            self.open_youtube()
        
        # Facebook
        elif 'facebook' in command:
            self.open_facebook()
        
        # Open specific websites
        elif 'open' in command and any(word in command for word in ['google', 'gmail', 'twitter', 'instagram']):
            if 'google' in command:
                self.open_website('https://www.google.com')
            elif 'gmail' in command:
                self.open_website('https://mail.google.com')
            elif 'twitter' in command:
                self.open_website('https://www.twitter.com')
            elif 'instagram' in command:
                self.open_website('https://www.instagram.com')
        
        # Open file
        elif 'open file' in command or 'open document' in command:
            self.speak("Please say the filename")
            filename = self.listen()
            if filename:
                self.search_and_open_file(filename)
        
        # Time
        elif 'time' in command:
            self.get_time()
        
        # Date
        elif 'date' in command:
            self.get_date()
        
        # Help
        elif 'help' in command or 'what can you do' in command:
            self.speak("I can open YouTube, Facebook, and other websites. "
                      "I can open files on your computer. "
                      "I can tell you the time and date. "
                      "Just say 'exit' or 'goodbye' to close me.")
        
        else:
            self.speak("I'm not sure how to help with that. Say 'help' to know what I can do.")
        
        return True
    
    def run(self):
        """Main loop to run JARVIS"""
        self.speak("Hello! I am JARVIS, your personal assistant. How may I help you?")
        
        while True:
            command = self.listen()
            if not self.process_command(command):
                break


if __name__ == "__main__":
    # Create and run JARVIS
    jarvis = Jarvis()
    
    print("\n" + "="*50)
    print("JARVIS - Voice Assistant")
    print("="*50)
    print("\nCommands you can try:")
    print("  • 'Open YouTube'")
    print("  • 'Open Facebook'")
    print("  • 'Open file' (then say the filename)")
    print("  • 'What time is it?'")
    print("  • 'What's the date?'")
    print("  • 'Help' (to see all commands)")
    print("  • 'Exit' or 'Goodbye' (to quit)")
    print("\n" + "="*50 + "\n")
    
    jarvis.run()