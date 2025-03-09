from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import tkinter as tk
from tkinter import Scrollbar, Text
import speech_recognition as sr
import pyttsx3
import os

# Initialize chatbot
chatbot = ChatBot("EnhancedBot")

# Train chatbot with English corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()


# Function to speak text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()


# Function to get chatbot response
def get_response():
    user_input = user_entry.get()

    if user_input.lower() == "exit":
        root.destroy()
    else:
        chat_history.insert(tk.END, "You: " + user_input + "\n")

        response = chatbot.get_response(user_input)
        chat_history.insert(tk.END, "Bot: " + str(response) + "\n\n")

        # Speak chatbot response
        speak(str(response))

        # Save chat to history
        save_chat("You: " + user_input)
        save_chat("Bot: " + str(response))

        user_entry.delete(0, tk.END)


# Function to recognize speech
def voice_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        chat_history.insert(tk.END, "Listening...\n")

        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            user_entry.delete(0, tk.END)
            user_entry.insert(0, text)
            get_response()
        except sr.UnknownValueError:
            chat_history.insert(tk.END, "Bot: Sorry, I didn't understand.\n\n")
        except sr.RequestError:
            chat_history.insert(tk.END, "Bot: API error. Check your internet connection.\n\n")


# Function to save chat history
def save_chat(text):
    with open("chat_history.txt", "a") as file:
        file.write(text + "\n")


# Function to load chat history
def load_chat_history():
    if os.path.exists("chat_history.txt"):
        with open("chat_history.txt", "r") as file:
            chats = file.readlines()
            for chat in chats:
                chat_history.insert(tk.END, chat)


# Create GUI
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("500x600")
root.configure(bg="#1E1E1E")

# Chat history text box
chat_history = Text(root, wrap=tk.WORD, bg="#282C34", fg="white", font=("Arial", 12))
chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Scrollbar for chat history
scrollbar = Scrollbar(chat_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_history.yview)

# Load previous chat history
load_chat_history()

# User input field
user_entry = tk.Entry(root, font=("Arial", 12), bg="#3C3F41", fg="white")
user_entry.pack(pady=5, padx=10, fill=tk.X)

# Button frame
button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=5)

# Send button
send_button = tk.Button(button_frame, text="Send", font=("Arial", 12), command=get_response, bg="#0078D7", fg="white")
send_button.pack(side=tk.LEFT, padx=5)

# Voice input button
voice_button = tk.Button(button_frame, text="🎤 Speak", font=("Arial", 12), command=voice_input, bg="#28A745",
                         fg="white")
voice_button.pack(side=tk.RIGHT, padx=5)

# Run the GUI
root.mainloop()
