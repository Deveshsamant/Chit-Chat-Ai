
import sys
import threading
import queue
import time
import numpy as np
import re
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread, Qt

from overlay import TransparentOverlay
from audio_capture import AudioCapture
from stt import SpeechToText
from llm import LLM

# --- Worker for LLM (Thinker) ---
class LLMWorker(QObject):
    response_ready = pyqtSignal(str) # Final response
    token_ready = pyqtSignal(str)    # Streaming tokens
    status_update = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()
        self.running = True
        self.llm = None
        
    def run(self):
        try:
            # Initialize LLM
            self.status_update.emit("Loading LLM...")
            # Point to the local folder where we are downloading the model
            model_path = r"local_models\qwen2.5-coder-3b-instruct-q4_k_m.gguf"
            self.llm = LLM(model_path)
            self.status_update.emit("LLM Ready")
        except Exception as e:
            self.status_update.emit(f"LLM Error: {str(e)}")
            return

        while self.running:
            try:
                # Wait for question (blocking 1s timeout to check running)
                user_text = self.queue.get(timeout=1.0)
                
                # Process Question
                self.status_update.emit("Thinking...")
                
                # Generate (Modified llm.py should support streaming, but we can capture prints or modify LLM later)
                # For now, we assume LLM.generate_response prints tokens. 
                # Ideally, we should update LLM class to yield tokens, but for now we run it.
                # To support streaming to UI, we need to modify LLM.generate_response to callback.
                # For this step, let's just run it and send final result, or implement a wrapper if possible.
                
                # IMPORTANT: We need streaming. 
                # Let's wrap generate_stream in LLM class or access model directly?
                # The generic LLM class handles logic. Let's use it.
                
                # We can update LLM class later to take a callback. 
                # For now, let's just get the full response to prove concurrency, 
                # or hack a token callback if needed.
                # Actually, the user wants "answer fast", so streaming is key.
                # Let's stick to full response for the structure first, or we modify LLM.
                
                # Let's add a callback hook to LLM in the next step if needed.
                # For now, standard generation.
                
                response = self.llm.generate_response(user_text) # This currently prints to console
                self.response_ready.emit(response)
                self.status_update.emit("Listening...")
                
                self.queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"LLM Processing Error: {e}")
                self.status_update.emit("Error generating response")

    def stop(self):
        self.running = False

    def add_question(self, text):
        self.queue.put(text)


# --- Worker for Audio (Listener) ---
class AudioWorker(QObject):
    text_ready = pyqtSignal(str, str) # role, text
    status_update = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        try:
            self.audio_capture = AudioCapture()
            self.status_update.emit("Loading Whisper...")
            # Switch to faster-whisper (base/tiny managed in stt.py)
            self.stt = SpeechToText(model_size="base") 
            self.status_update.emit("Listening...")
        except Exception as e:
            self.status_update.emit(f"Audio Error: {str(e)}")
            return

        self.audio_capture.start()

        audio_buffer = []
        silence_threshold = 0.0003
        silence_frames = 0
        is_speaking = False
        preview_counter = 0
        
        # Audio processing loop
        while self.running:
            chunk = self.audio_capture.get_audio_chunk()
            if chunk is None:
                time.sleep(0.01)
                continue
            
            # Digital Gain
            chunk = chunk * 5.0
            
            energy = np.mean(np.abs(chunk))
            
            if energy > silence_threshold:
                is_speaking = True
                silence_frames = 0
                audio_buffer.append(chunk)
                
                # Live Preview & Question Detection Logic
                preview_counter += 1
                if preview_counter >= 10: # Check every ~0.6s
                    preview_counter = 0
                    try:
                        temp_audio = np.concatenate(audio_buffer)
                        partial_text = self.stt.transcribe(temp_audio)
                        
                        if partial_text:
                            # 1. Update UI Preview
                            display_text = (partial_text[-40:] + '..') if len(partial_text) > 40 else partial_text
                            self.status_update.emit(f"👂 {display_text}")
                            
                            # 2. Check for Question Mark (Trigger)
                            # "Barge-in" - if we detect a full question, fire it off immediately!
                            if "?" in partial_text[-5:]: # Ends with ? (or close to end)
                                print(f"[Audio] Question Detected: {partial_text}")
                                # Send to Main Thread -> LLM
                                self.text_ready.emit("User", partial_text)
                                
                                # Clear buffer to start listening for NEXT sentence immediately
                                audio_buffer = [] 
                                is_speaking = False # Reset state
                                self.status_update.emit("Listening for next...")
                                
                    except Exception:
                        pass
                        
            else:
                if is_speaking:
                    silence_frames += 1
                    audio_buffer.append(chunk)
                    
                    # Silence duration (~0.7s)
                    if silence_frames > 12: 
                        # Process full phrase if not already caught by ? trigger
                        if len(audio_buffer) > 0:
                            self.process_buffer(audio_buffer)
                            audio_buffer = []
                        
                        is_speaking = False
                        silence_frames = 0
                        preview_counter = 0
                        self.status_update.emit("Listening...")
                else:
                    if len(audio_buffer) > 5:
                        audio_buffer.pop(0)
                    audio_buffer.append(chunk)

    def process_buffer(self, buffer):
        try:
            audio_data = np.concatenate(buffer)
            text = self.stt.transcribe(audio_data)
            if text and len(text.strip()) > 1:
                print(f"[Audio] Final Phrase: {text}")
                self.text_ready.emit("User", text)
        except Exception as e:
            print(f"Transcription error: {e}")

    def stop(self):
        self.running = False
        if hasattr(self, 'audio_capture'):
            self.audio_capture.stop()


# --- Main Application Logic ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentOverlay()
    
    # 1. Setup Audio Thread
    audio_thread = QThread()
    audio_worker = AudioWorker()
    audio_worker.moveToThread(audio_thread)
    
    audio_thread.started.connect(audio_worker.run)
    audio_worker.status_update.connect(window.update_status)
    audio_worker.text_ready.connect(window.append_message) # Show user text
    
    # 2. Setup LLM Thread
    llm_thread = QThread()
    llm_worker = LLMWorker()
    llm_worker.moveToThread(llm_thread)
    
    llm_thread.started.connect(llm_worker.run)
    llm_worker.status_update.connect(window.update_status)
    llm_worker.response_ready.connect(lambda text: window.append_message("Assistant", text))
    
    # 3. Connect Audio -> LLM
    # When Audio detects text, send it to LLM worker queue
    # We use a lambda or slot in window to bridge if needed, or direct connection
    # But QObjects in different threads needs signal/slot. 
    # Let's create a bridge slot in LLMWorker or connect signal directly? 
    # We need to extract the text string from (role, text) signal of audio_worker
    
    def bridge_audio_to_llm(role, text):
        # We only send to LLM if it's worth it? 
        # User wants "answer all questions".
        # So we send everything that looks like a sentence/question.
        if len(text) > 2:
            llm_worker.add_question(text)
            
    audio_worker.text_ready.connect(bridge_audio_to_llm)

    # Start Threads
    audio_thread.start()
    llm_thread.start()
    
    window.show()
    
    # Cleanup on exit
    exit_code = app.exec()
    audio_worker.stop()
    llm_worker.stop()
    audio_thread.quit()
    llm_thread.quit()
    audio_thread.wait()
    llm_thread.wait()
    sys.exit(exit_code)

