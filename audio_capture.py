import soundcard as sc
import numpy as np
import threading
import queue
import time

class AudioCapture:
    def __init__(self, sample_rate=16000, block_size=4096):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.audio_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.mic = self._get_loopback_mic()

    def _get_loopback_mic(self):
        # Prioritize System Audio (Loopback) to hear what the user hears (Speakers/Headphones)
        try:
            # 1. Get the current default output device (Speaker/Headphones)
            default_speaker = sc.default_speaker()
            print(f"[Audio] Default Speaker: {default_speaker.name}")
            
            # 2. Find the corresponding loopback microphone
            # Loopback devices usually share the name or ID structure of the speaker
            all_mics = sc.all_microphones(include_loopback=True)
            for mic in all_mics:
                if mic.isloopback and mic.name == default_speaker.name:
                    print(f"[Audio] Selected Loopback Device: {mic.name}")
                    return mic
            
            # 3. Fallback: Try "Stereo Mix" if specific loopback not found
            for mic in all_mics:
                if "Stereo Mix" in mic.name:
                    print(f"[Audio] Selected Fallback Loopback: {mic.name}")
                    return mic

            # 4. Last Resort: Default Microphone (Warning: Will capture Room Audio, not System Audio)
            print("[Audio] Warning: No Loopback found. Falling back to Default Mic.")
            return sc.default_microphone()

        except Exception as e:
            print(f"[Audio] Error finding loopback device: {e}")
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
        consecutive_silence_count = 0
        try:
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
                    max_val = np.max(np.abs(data))
                    if max_val == 0:
                       consecutive_silence_count += 1
                       if consecutive_silence_count == 20: # Approx 5 seconds at 4096/16000 (~0.25s per block)
                           print("[WARNING] Microphone is returning pure silence (0.0). Check mute switch or privacy settings!")
                    else:
                        consecutive_silence_count = 0
                    
                    self.audio_queue.put(data)
        except Exception as e:
            print(f"[Audio] Recording Error: {e}")
            self.running = False

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_audio_chunk(self):
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None
