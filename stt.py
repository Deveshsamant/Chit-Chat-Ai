import numpy as np
import torch
import os
from faster_whisper import WhisperModel

class SpeechToText:
    def __init__(self, model_size="small"):
        # Map "tiny" to "small" if user passed tiny, or keep as is.
        # Recommendation: Use "small" or "medium" for better accent recognition.
        if model_size == "tiny" or model_size == "base":
            model_size = "small" # Upgrade automatically for better quality

        print(f"Loading Faster-Whisper model: {model_size}...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        
        # Local model path
        local_path = os.path.join(os.getcwd(), "local_models", "faster_whisper_cache")
        if not os.path.exists(local_path):
            os.makedirs(local_path)
            
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type, download_root=local_path)
        print(f"Faster-Whisper model loaded on {device} ({compute_type})")

    def transcribe(self, audio_data):
        # audio_data: numpy array of float32, mono
        
        # faster-whisper expects float32
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)

        segments, info = self.model.transcribe(audio_data, beam_size=5, language="en")
        
        # Combine all segments
        text = " ".join([segment.text for segment in segments]).strip()
        return text
