#!/usr/bin/env python
# coding: utf-8

# In[12]:


import speech_recognition as sr
import pyttsx3

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def process_command(command):
    if "hello" in command:
        return "Hello! How can I help you?"
    elif "goodbye" in command:
        return "Goodbye! Have a great day."
    else:
        return "I'm sorry, I didn't understand that command."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            response = process_command(command)
            print("Response:", response)
            speak(response)


# In[28]:


import speech_recognition as sr
from gtts import gTTS
import os
import pyttsx3

user_information = {}

def recognize_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def process_command(command):
    global user_information

    if 'hello' in command:
        return "Hello! How can I assist you?"
    elif 'how are you' in command:
        return "I'm a computer program, so I don't have feelings, but I'm here to help!"
    elif 'goodbye' in command:
        return "Goodbye! Have a great day."
    elif 'time' in command:
        import datetime
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}."
    elif 'weather' in command:
        # Example of fetching weather information from an API (replace with your API key and endpoint)
        api_key = 'your_weather_api_key'
        city = 'your_city'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The weather in {city} is {description} with a temperature of {temperature} degrees Celsius."
        else:
            return "Sorry, I couldn't fetch the weather information at the moment."
    elif 'teach me' in command:
        # Custom command to teach the assistant
        return teach_assistant(command)
    elif 'thank you' in command:
        return "You're welcome! If you have more questions, feel free to ask."
    else:
        return "I'm sorry, I didn't understand that command."

def teach_assistant(command):
    global user_information

    try:
        # Extracting information from the command
        _, info_key, info_value = command.split(' ', 2)

        # Storing the information in the dictionary
        user_information[info_key] = info_value

        return f"Got it! I've learned that your {info_key} is {info_value}."
    except ValueError:
        return "Sorry, I couldn't understand the information. Please provide the information in the format 'teach me your [key] is [value]'."



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            response = process_command(command)
            print("Response:", response)
            speak(response)


# In[36]:


import speech_recognition as sr
from gtts import gTTS
import os

def recognize_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def load_commands_from_file(file_path):
    commands = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Ensure there is at least one colon in the line
            if ':' in line:
                key, value = line.split(':', 1)
                commands[key.strip()] = value.strip()
            else:
                print(f"Ignoring invalid line in the file: {line}")

    return commands

def process_command(command, command_responses):
    if command in command_responses:
        return command_responses[command]
    else:
        return "I'm sorry, I didn't understand that command."

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('start output.mp3')

if __name__ == "__main__":
    # Specify the path to your text file containing commands
    commands_file_path = r'E:\AI\Data\Com.txt'

    # Load available commands from the text file
    available_commands = load_commands_from_file(commands_file_path)

    while True:
        voice_command = recognize_audio()

        if voice_command:
            response = process_command(voice_command, available_commands)
            print("Response:", response)

            # Convert the response to speech
            text_to_speech(response)


# In[ ]:


import speech_recognition as sr
import requests


WIT_API_KEY = 'your_wit_ai_api_key'

def recognize_audio():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def process_command(command):
    
    wit_url = f'https://api.wit.ai/message?v=20220115&q={command}'
    headers = {'Authorization': f'Bearer {WIT_API_KEY}'}

    try:
        response = requests.get(wit_url, headers=headers)
        data = response.json()

        # Extract intent from Wit.ai response
        intent = data['intents'][0]['name'] if data['intents'] else None

        return intent
    except Exception as e:
        print(f"Error processing command with Wit.ai: {e}")
        return None

if __name__ == "__main__":
    while True:
        user_command = recognize_audio()

        if user_command:
            intent = process_command(user_command)
            print("Intent:", intent)

            # Add your logic to handle different intents
            if intent == 'greeting':
                print("Hello! How can I assist you?")
            elif intent == 'goodbye':
                print("Goodbye! Have a great day.")
            else:
                print("I'm not sure how to respond to that.")

# Note: Replace 'your_wit_ai_api_key' with your actual Wit.ai API key.

