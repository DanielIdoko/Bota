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

# Tkinter UI
root = tk.Tk()
root.title("Curiosity AI")
root.geometry("380x500")
root.attributes("-topmost", True)
root.resizable(False, False)
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                font=("Segoe UI", 10),
                padding=6,
                background="#444",
                foreground="white")
style.map("TButton", background=[("active", "#555")])

# Output Text
output = tk.Text(root,
                 wrap="word",
                 bg="#121212",
                 fg="white",
                 font=("Segoe UI", 11),
                 relief="flat",
                 padx=10,
                 pady=10)
output.pack(fill="both", expand=True)

# Bottom input frame
bottom = tk.Frame(root, bg="#1e1e1e")
bottom.pack(fill="x", pady=8)

entry = tk.Entry(bottom,
                 font=("Segoe UI", 11),
                 bg="#222",
                 fg="white",
                 relief="flat")
entry.pack(side="left", fill="x", expand=True, padx=(10, 5))

send_btn = ttk.Button(bottom, text="Send", command=send_text)
send_btn.pack(side="left", padx=5)

voice_btn = ttk.Button(bottom, text="🎤", width=3, command=listen_voice)
voice_btn.pack(side="left", padx=(5, 10))

root.mainloop()
