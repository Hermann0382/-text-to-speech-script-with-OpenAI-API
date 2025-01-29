import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

text_to_speak = "Hier siehst Du unter der Haube wie der Code aus sieht, mit dem eine Stimme wie die meine generiert wird. Lass mir ein Like, wenn Du das genauso cool wie ich findest, oder folge mir, wenn Du mehr solche Inhalte sehen möchtest."

# Generate a filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"german_speech_{timestamp}.mp3"

response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "tts-1",
        "input": text_to_speak,
        "voice": "nova",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }
)

# Save with the custom filename
with open(filename, "wb") as f:
    f.write(response.content)
