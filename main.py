import sys
import threading
import time
import numpy as np
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt

from overlay import TransparentOverlay
from audio_capture import AudioCapture
from stt import SpeechToText
from llm import LLM

class Worker(QObject):
    update_status = pyqtSignal(str)
    update_chat = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.model_switch_requested = None

    def handle_model_switch(self, model_type):
        print(f"Worker received switch request: {model_type}")
        # Model switching disabled as we are using a single optimized GGUF model
        print("Model switching is currently disabled for GGUF optimization.")
        self.model_switch_requested = None

    def run(self):
        # Initialize components
        self.update_status.emit("Initializing System...")
        
        try:
            self.audio_capture = AudioCapture()
            self.update_status.emit("Loading Whisper...")
            # Switch to tiny model for speed
            self.stt = SpeechToText(model_size="tiny")
            self.update_status.emit("Loading Qwen (Coder 3B)...")
            # Point to the local folder where we are downloading the model
            model_path = r"local_models\qwen2.5-coder-3b-instruct-q4_k_m.gguf"
            self.llm = LLM(model_path)
        except Exception as e:
            self.update_status.emit(f"Error: {str(e)}")
            return

        self.audio_capture.start()
        self.update_status.emit("Listening...")

        audio_buffer = []
        silence_threshold = 0.0003
        silence_frames = 0
        is_speaking = False
        
        # Audio processing loop
        while self.running:
            # Check for model switch
            if self.model_switch_requested:
                self.update_status.emit("Switching Model...")
                success = self.llm.reload_model(self.model_switch_requested)
                if success:
                    name = "1.5B" if "1.5B" in self.model_switch_requested else "3B"
                    self.update_status.emit(f"Ready! ({name} Model)")
                else:
                    self.update_status.emit("Switch Failed!")
                self.model_switch_requested = None
                
            chunk = self.audio_capture.get_audio_chunk()
            if chunk is None:
                time.sleep(0.01)
                continue
            
            # Digital Gain (Boost volume)
            chunk = chunk * 5.0
            
            energy = np.mean(np.abs(chunk))
            if energy > 0.0001: 
                # print(f"Energy: {energy:.6f}") # Commented out to reduce spam
                pass
            
            if energy > silence_threshold:
                is_speaking = True
                silence_frames = 0
                audio_buffer.append(chunk)
                self.update_status.emit("Hearing speech...")
            else:
                if is_speaking:
                    silence_frames += 1
                    audio_buffer.append(chunk)
                    
                    # Silence duration to trigger processing (Reduced for faster response)
                    # changing 1.5s to ~0.7s (12 frames)
                    if silence_frames > 12: 
                        self.process_audio(np.concatenate(audio_buffer))
                        audio_buffer = []
                        is_speaking = False
                        silence_frames = 0
                        self.update_status.emit("Listening...")
                else:
                    # Keep a small buffer just in case
                     if len(audio_buffer) > 5:
                         audio_buffer.pop(0)
                     audio_buffer.append(chunk)

    def process_audio(self, audio_data):
        self.update_status.emit("Transcribing...")
        text = self.stt.transcribe(audio_data)
        
        if not text or len(text.strip()) < 2:
            return

        self.update_chat.emit("User", text)
        self.update_status.emit("Thinking...")
        
        response = self.llm.generate_response(text)
        self.update_chat.emit("AI", response)

    def stop(self):
        self.running = False
        if hasattr(self, 'audio_capture'):
            self.audio_capture.stop()

def main():
    app = QApplication(sys.argv)
    window = TransparentOverlay()
    window.show()

    # Create worker thread
    thread = QThread()
    worker = Worker()
    worker.moveToThread(thread)
    
    # Connect signals
    thread.started.connect(worker.run)
    worker.update_status.connect(window.update_status)
    worker.update_chat.connect(window.append_message)
    
    # Switch Model Signal
    # Use DirectConnection because the worker thread is busy in a loop and cannot process queued events
    window.request_model_switch.connect(worker.handle_model_switch, Qt.ConnectionType.DirectConnection)
    
    # Clean exit
    app.aboutToQuit.connect(worker.stop)
    app.aboutToQuit.connect(thread.quit)
    app.aboutToQuit.connect(thread.wait)

    thread.start()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
