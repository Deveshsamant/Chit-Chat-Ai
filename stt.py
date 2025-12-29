import whisper
import numpy as np
import torch
import os

# Add local ffmpeg to path
ffmpeg_path = os.path.abspath(os.path.join(os.getcwd(), "ffmpeg", "bin"))
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path

class SpeechToText:
    def __init__(self, model_size="base"):
        print(f"Loading Whisper model: {model_size}...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Local model path
        local_path = os.path.join(os.getcwd(), "local_models", "whisper")
        if not os.path.exists(local_path):
            os.makedirs(local_path)
            
        self.model = whisper.load_model(model_size, device=device, download_root=local_path)
        print(f"Whisper model loaded on {device}")

    def transcribe(self, audio_data):
        # audio_data: numpy array of float32, mono
        
        # Whisper expects raw audio or 30s chunks.
        # It handles normalization internally.
        
        # Ensure it's float32
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)

        result = self.model.transcribe(audio_data, fp16=(self.model.device.type == "cuda"))
        return result["text"].strip()
