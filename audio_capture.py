import soundcard as sc
import numpy as np
import threading
import queue
import time

class AudioCapture:
    def __init__(self, sample_rate=16000, block_size=1024):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.audio_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.mic = self._get_loopback_mic()

    def _get_loopback_mic(self):
        # Prioritize Default Microphone for Voice Input
        try:
            # 1. Priority: Default Microphone (System Default)
            # This handles Bluetooth, Wired, and Built-in mics automatically based on Windows settings.
            default = sc.default_microphone()
            print(f"[Audio] Selected Default Mic: {default.name}")
            return default
            
            # Legacy loopback logic (commented out or moved to fallback if needed, 
            # but user specifically asked for voice input from headphones)
            
        except Exception as e:
            print(f"[Audio] Error finding microphone: {e}")
            return None

    def start(self):
        if self.mic is None:
            print("No suitable microphone found.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._record_loop, daemon=True)
        self.thread.start()

    def _record_loop(self):
        print(f"Starting recording on: {self.mic.name}")
        with self.mic.recorder(samplerate=self.sample_rate) as recorder:
            while self.running:
                data = recorder.record(numframes=self.block_size)
                # data is (numframes, channels) float32
                # flatten to mono
                if data.shape[1] > 1:
                    data = np.mean(data, axis=1)
                else:
                    data = data.flatten()
                
                # Check for silence (all zeros) distinct from just quiet
                if np.max(np.abs(data)) == 0:
                   # Print only occasionally to avoid spam
                   pass 
                
                self.audio_queue.put(data)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_audio_chunk(self):
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None
