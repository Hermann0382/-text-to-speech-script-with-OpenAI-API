import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import os
from dotenv import load_dotenv, set_key
from datetime import datetime

def check_api_key():
    # Check if .env exists and has API key
    if not os.path.exists('.env') or not os.getenv('OPENAI_API_KEY'):
        # Create API key setup window
        api_window = tk.Toplevel()
        api_window.title("OpenAI API Key Setup")
        api_window.geometry("400x200")
        
        ttk.Label(api_window, text="Please enter your OpenAI API key:").pack(pady=20)
        api_key_var = tk.StringVar()
        ttk.Entry(api_window, textvariable=api_key_var, width=50).pack(pady=10)
        
        def save_api_key():
            api_key = api_key_var.get().strip()
            if api_key:
                # Create or update .env file
                with open('.env', 'w') as f:
                    f.write(f'OPENAI_API_KEY={api_key}')
                load_dotenv()
                api_window.destroy()
                messagebox.showinfo("Success", "API key saved successfully!")
            else:
                messagebox.showerror("Error", "Please enter a valid API key")
        
        ttk.Button(api_window, text="Save API Key", command=save_api_key).pack(pady=20)
        ttk.Label(api_window, text="Get your API key from: openai.com/api-keys", foreground="blue").pack()
        
        # Wait for API key setup before continuing
        api_window.wait_window()

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech Converter")
        
        # Check for API key before setting up main interface
        check_api_key()
        
        # Available voices
        self.voices = {
            "Nova (Female)": "nova",
            "Shimmer (Female)": "shimmer",
            "Alloy (Neutral)": "alloy",
            "Echo (Male)": "echo",
            "Fable (Male)": "fable",
            "Onyx (Male)": "onyx"
        }
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text input
        ttk.Label(main_frame, text="Enter your text:").grid(row=0, column=0, sticky=tk.W)
        self.text_input = tk.Text(main_frame, height=5, width=50)
        self.text_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Voice selection
        ttk.Label(main_frame, text="Select voice:").grid(row=2, column=0, sticky=tk.W)
        self.voice_var = tk.StringVar()
        voice_dropdown = ttk.Combobox(main_frame, textvariable=self.voice_var, values=list(self.voices.keys()))
        voice_dropdown.grid(row=2, column=1, sticky=tk.W, pady=5)
        voice_dropdown.set("Nova (Female)")
        
        # File name
        ttk.Label(main_frame, text="File name:").grid(row=3, column=0, sticky=tk.W)
        self.filename_var = tk.StringVar()
        self.filename_var.set(f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        ttk.Entry(main_frame, textvariable=self.filename_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Save location
        ttk.Label(main_frame, text="Save location:").grid(row=4, column=0, sticky=tk.W)
        self.save_path = tk.StringVar()
        self.save_path.set(os.getcwd())  # Default to current directory
        ttk.Entry(main_frame, textvariable=self.save_path).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_location).grid(row=4, column=2, padx=5)
        
        # Convert button
        ttk.Button(main_frame, text="Convert to Speech", command=self.convert_to_speech).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=2)

    def browse_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_path.set(directory)

    def convert_to_speech(self):
        try:
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                self.status_var.set("Please enter some text!")
                return

            voice = self.voices[self.voice_var.get()]
            filename = f"{self.filename_var.get()}.mp3"
            full_path = os.path.join(self.save_path.get(), filename)

            response = requests.post(
                "https://api.openai.com/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "tts-1",
                    "input": text,
                    "voice": voice,
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.8
                    }
                }
            )

            with open(full_path, "wb") as f:
                f.write(response.content)
            
            self.status_var.set(f"Success! Saved to: {full_path}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
