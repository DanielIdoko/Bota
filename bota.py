import tkinter as tk
from tkinter import ttk
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("API_KEY")

# Gemini API setup
# NOTE: configure() now uses keyword argument `api_key`
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Voice setup
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech recognition setup
recognizer = sr.Recognizer()

def listen_voice():
    try:
        with sr.Microphone() as source:
            output.insert(tk.END, "Listening...\n")
            root.update()
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            output.insert(tk.END, f"You (voice): {text}\n\n")
            handle_query(text)
    except sr.UnknownValueError:
        output.insert(tk.END, "I didn’t catch that. Try again.\n\n")
    except Exception as e:
        output.insert(tk.END, f"Error: {str(e)}\n\n")

# Chat memory
chat_history = []

def handle_query(user_input):
    if not user_input.strip():
        return

    # Add user message to memory
    chat_history.append({"role": "user", "content": user_input})

    # Ask Gemini
    response = model.generate_content(messages=chat_history)
    answer = response.text

    # Show bot response
    output.insert(tk.END, f"Bot: {answer}\n\n")
    speak(answer)

    # Add bot response to memory
    chat_history.append({"role": "assistant", "content": answer})

# Send button function
def send_text():
    text = entry.get()
    if text.strip() == "":
        return
    output.insert(tk.END, f"You: {text}\n\n")
    entry.delete(0, tk.END)
    handle_query(text)

















