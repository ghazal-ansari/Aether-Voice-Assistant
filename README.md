🚀 Overview

Aether is a fully functional desktop voice assistant built with Python.
It can listen, speak, search the web, and interact with you using both voice and text commands.

This project uses:

🎙️ SpeechRecognition for real-time voice input

🗣️ gTTS (Google Text-to-Speech) and Pygame for speech synthesis

🌍 DuckDuckGo API for intelligent question answering

🧩 Tkinter for an elegant graphical user interface

🧩 Features

✅ Voice Recognition — Speak naturally, and Aether understands your command.
✅ Text Commands — Type instructions directly into the GUI.
✅ Web Search Integration — Answers general queries using DuckDuckGo’s instant answer API.
✅ Smart Responses — Handles custom questions like “Who created you?”
✅ Open Websites — Simply say “Open YouTube” or “Open Google”.
✅ Speech Queue System — Prevents overlapping audio output.
✅ GUI Interface — Clean, dark-themed desktop layout with logs and real-time transcription.
✅ Multithreaded — Voice recognition and speech synthesis run smoothly without freezing the interface.


⚙️ Requirements

Ensure you have Python 3.9+ installed.

Then install the dependencies:

pip install -r requirements.txt


requirements.txt

tkinter
SpeechRecognition
requests
gTTS
pygame


💡 Note: On some systems, tkinter is pre-installed with Python. If not, install it via your package manager (sudo apt install python3-tk on Linux).

🧠 How It Works

Start Aether: Run the Python script.

Speak or Type:

Click “🎤 Speak” to give a voice command.

Or type into the entry box and press Enter or click Submit.

Aether Listens: The assistant processes your input via the SpeechRecognition library.

Get Answers:

Opens requested websites (e.g., “Open YouTube”).

Fetches information from DuckDuckGo (e.g., “Who is Elon Musk?”).

Tells the current time.

Answers creator-related questions.

Aether Speaks Back: The response is converted to audio using Google TTS and played using Pygame.

🧩 Example Commands
Command	Action
“What time is it?”	Tells the current time
“Open Google”	Opens Google in your default browser
“Who created you?”	Responds with the creator’s name
“Define artificial intelligence”	Fetches the definition
“Tell me about Python programming”	Answers from DuckDuckGo
🖥️ GUI Layout

🪟 Top: App title — AETHER

💬 Middle: Speech transcription (“You: …”)

📜 Log Area: Conversation history (color-coded)

🧾 Text Entry: Type messages manually

🔘 Buttons:

🎤 Speak — Start voice recognition

🛑 Stop Speaking — Stop current audio output

🚪 Exit — Quit the application

Language: Python
Version: 1.0.0


💬 Acknowledgments

SpeechRecognition

Google Text-to-Speech (gTTS)

DuckDuckGo Instant Answer API

Pygame

Tkinter
