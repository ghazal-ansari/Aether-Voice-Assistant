import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import datetime
import requests
import threading
import queue
import webbrowser
import platform
import os
from gtts import gTTS
import pygame
import time


"""variables"""

speech_queue = queue.Queue()
speak_lock = threading.Lock()

"""functions"""


def tts_agent():
    pygame.mixer.init()
    while True:
        text = speech_queue.get()
        if text is None:
            break
        with speak_lock:
            try:
                filename = os.path.join("static", "sounds", "temp_audio.mp3")
                tts = gTTS(text=text, lang="en")
                tts.save(filename)

                # Load and play the audio
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()

                # Wait until playback finishes
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)  # Keeps the loop responsive

                # Stop and unload
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

                # Delay before deleting
                time.sleep(0.2)
                os.remove(filename)

            except Exception as e:
                append(f"Error in TTS: {e}", color="red")
        speech_queue.task_done()


tts_thread = threading.Thread(target=tts_agent, daemon=True)
tts_thread.start()


def append(text, color="white"):
    log_area.config(state=tk.NORMAL)
    tag_name = f"tag_{color}"
    if tag_name not in log_area.tag_names():
        log_area.tag_config(tag_name, foreground=color)
    log_area.insert(tk.END, text + "\n", tag_name)
    log_area.see(tk.END)
    log_area.config(state=tk.DISABLED)


def speak(text):
    append(f"Aether: {text}", color="white")
    time.sleep(0.1)
    speech_queue.put(text)


def stop_speaking():
    pygame.mixer.music.stop
    append("Aether: Speech stopped.", color="red")


def update_transcription(text):
    transcription_var.set(f"You: {text}")


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        update_transcription(command)
        append(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        update_transcription("Couldn't catch that")
        return "unrecognized"
    except sr.RequestError:
        update_transcription("Network error")
        return "error"


def answer_from_duckduckgo(query: str) -> str:
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("Answer"):
            return data["Answer"]
        elif data.get("Definition"):
            return data["Definition"]
        else:
            return
    except Exception as e:
        return f"Error fetching answer: {e}"


def open_web(site_name):
    site = site_name.strip().replace(" ", "")
    url = f"https://{site}.com"
    webbrowser.open(url)
    speak(f"{site.capitalize()} is open.")


def welcome_message():
    greeting = f"Hello {name}, how can I assist you today?"
    speak(greeting)


def is_creator_question(text):
    triggers = [
        "who made you",
        "who created you",
        "who developed you",
        "who is your creator",
        "who is your maker",
        "who built you",
        "who designed you",
        "who invented you",
        "who made jarvis",
        "who made you jarvis",
        "hey jarvis who made you",
        "who created",
        "create",
    ]
    return any(trigger in text for trigger in triggers)


def handle_command(command):
    if is_creator_question(command):
        response = (
            "I was created by Qazal Ansari as a personal voice assistant project, "
            "using Python and tools like speech recognition and DuckDuckGo search."
        )
        speak(response)
    elif "open" in command:
        parts = command.split("open", 1)
        if len(parts) > 1:
            open_web(parts[1])
        else:
            speak("Sorry, I couldn't recognize the website name.")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Current time is {now}.")
    elif command in ["unrecognized", "error"]:
        speak("Sorry, I didn't catch that.")
    else:
        response = answer_from_duckduckgo(command)
    if response:
        speak(response)
    else:
        speak("Sorry, I couldn't find an answer to that.")


def on_speak_button():
    def task():
        command = listen()
        handle_command(command)

    threading.Thread(target=task).start()


def on_text_submit(event=None):
    command = text_entry.get().strip()
    if command:
        update_transcription(command)
        append(f"You said: {command}")
        text_entry.delete(0, tk.END)
        threading.Thread(target=lambda: handle_command(command)).start()


def on_exit_button():
    speech_queue.put(None)
    root.destroy()


def close(event=None):
    speech_queue.put(None)
    root.destroy()


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


"""window"""

root = tk.Tk()
root.title("Aether Voice Assistant")
root.configure(bg="#000538")
root.geometry("1250x750")

"""style variables"""

FONT_TITLE = ("Times", 42, "bold")
FONT_TRANSCRIPTION = ("Segoe UI", 24)
FONT_LOG = ("Consolas", 18)
FONT_BUTTON = ("Segoe UI", 18, "bold")
FONT_ENTRY = ("Segoe UI", 18)
COLOR_BG = "#000538"
COLOR_TEXT = "white"
COLOR_HIGHLIGHT = "#6DA0BF"
COLOR_BUTTON_BG = "#4D81A0"
COLOR_STOP_BUTTON_BG = "#C1121F"
COLOR_EXIT_BUTTON_BG = "#4D81A0"
COLOR_LOG_BG = "#B1CCDD"
COLOR_SUBMIT_BUTTON_BG = "#74A4C2"

# Grid
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)

# Title
title = tk.Label(root, text="AETHER", font=FONT_TITLE, fg=COLOR_HIGHLIGHT, bg=COLOR_BG)
title.grid(row=0, column=0, pady=(25, 10), sticky="n")

# Transcription
transcription_var = tk.StringVar()
transcription_label = tk.Label(
    root,
    textvariable=transcription_var,
    font=FONT_TRANSCRIPTION,
    fg=COLOR_TEXT,
    bg=COLOR_BG,
)
transcription_label.grid(row=1, column=0, sticky="n")

# Log area
log_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=FONT_LOG,
    bg=COLOR_LOG_BG,
    fg=COLOR_TEXT,
    height=15,
    width=70,
)
log_area.grid(row=2, column=0, pady=10)
log_area.tag_config("blue", foreground=COLOR_HIGHLIGHT)
log_area.tag_config("white", foreground=COLOR_TEXT)
log_area.tag_config("red", foreground="#9D0910")

# Entry + Submit
entry_frame = tk.Frame(root, bg=COLOR_BG)
entry_frame.grid(row=3, column=0, pady=10)

text_entry = tk.Entry(
    entry_frame, font=FONT_ENTRY, bg="#7F908F", fg="white", insertbackground=COLOR_TEXT
)
text_entry.pack(side="left", padx=5, ipadx=200, ipady=5)

submit_btn = tk.Button(
    entry_frame,
    text="Submit",
    font=FONT_BUTTON,
    bg=COLOR_SUBMIT_BUTTON_BG,
    fg="white",
    command=on_text_submit,
)
submit_btn.pack(side="left", padx=5)

# Buttons
btn_frame = tk.Frame(root, bg=COLOR_BG)
btn_frame.grid(row=4, column=0, pady=10)

speak_btn = tk.Button(
    btn_frame,
    text="🎤Speak",
    font=FONT_BUTTON,
    bg=COLOR_BUTTON_BG,
    fg="white",
    command=on_speak_button,
)
speak_btn.pack(side="left", padx=10)

stop_btn = tk.Button(
    btn_frame,
    text="🛑Stop Speaking",
    font=FONT_BUTTON,
    bg=COLOR_STOP_BUTTON_BG,
    fg="white",
    command=stop_speaking,
)
stop_btn.pack(side="left", padx=10)

exit_btn = tk.Button(
    btn_frame,
    text="🚪Exit",
    font=FONT_BUTTON,
    bg=COLOR_EXIT_BUTTON_BG,
    fg="white",
    command=on_exit_button,
)
exit_btn.pack(side="left", padx=10)

# Watermark
watermark = tk.Label(
    root, text="<Developed by Qazal Ansari>", font="Times", fg="white", bg=COLOR_BG
)
watermark.grid(row=5, column=0, pady=10, sticky="s")

# Bind keys
root.bind("<Return>", on_text_submit)
root.bind("<Escape>", close)

# Welcome message
name = platform.node()
threading.Thread(target=welcome_message).start()

# Center the window
center_window(root)

# Start the GUI loop
root.mainloop()
