
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
                
                # Define callback to emit tokens
                def stream_callback(token):
                    self.token_ready.emit(token)

                # Generate with streaming
                response = self.llm.generate_response(user_text, stream_callback=stream_callback)
                
                # Signal completion (optional, or just ready)
                self.response_ready.emit("") # Empty string or special signal to say "Done" if needed by UI to finalize
                self.status_update.emit("Listening...")
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
                if preview_counter >= 5: # Check every ~0.3s (Faster detection)
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
    
    # Streaming Connections
    # 1. Start of message (triggered when we send text? or we can signal it)
    # Actually, we should trigger "Assistant" header when LLM starts thinking or first token arrives.
    # Let's trigger it when LLM *starts* generating? 
    # Or simpler: When token_ready fires, if it's the first one?
    # Better: Add a signal in LLMWorker "generation_started"
    
    # For now, let's just use the fact that we can call start_streaming_message before adding question?
    # Or let LLMWorker emit a signal.
    
    # We will just hook token_ready to stream_token, but we need to initialize the block.
    # Let's hack it: user message is added -> we expect assistant response.
    # Let's signal "Assistant" start when we send the question? No, that's too early.
    
    # Let's add a "start_generation" signal to LLMWorker logic above?
    # Or just use the lambda for now to start it on first token?
    # No, that's messy.
    
    # Let's just modify the response_ready connection to "end_streaming_message"
    llm_worker.response_ready.connect(lambda x: window.end_streaming_message())
    llm_worker.token_ready.connect(window.stream_token)
    
    # We need to call window.start_streaming_message("Assistant") sometime.
    # LLMWorker should emit it.
    # Let's add a line in LLMWorker.run before generate_response calls.
    # Since I missed adding that signal in the previous step, I will use a partial fix here:
    # Connect status_update: if status is "Thinking...", start assistant stream?
    # No.
    
    # Let's just update LLMWorker class above to emit 'response_started' or similar?
    # I can't easily edit class *definition* from here without re-writing the whole chunk.
    # But I can modify the `run` method chunk I touched above.
    
    # Actually, I can use the existing `status_update` signal.
    # If LLMWorker emits "Thinking...", we can trigger window.start_streaming_message("Assistant")
    def handle_llm_status(status):
        window.update_status(status)
        if status == "Thinking...":
            window.start_streaming_message("Assistant")
            
    llm_worker.status_update.disconnect() # Disconnect the direct one
    llm_worker.status_update.connect(handle_llm_status)
    
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

    # 4. Connect Correction Signal
    # Correction signal only sends 'text', but bridge expects 'role, text'.
    # We need a separate handler or lambda.
    def handle_correction(text):
         # Treat correction as user input
         if len(text) > 0:
             llm_worker.add_question(text)
             
    window.correction_ready.connect(handle_correction)

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

