from audio_capture import AudioCapture
import time

print("Testing Audio Capture Logic...")
ac = AudioCapture()
if ac.mic:
    print(f"FINAL SELECTION: {ac.mic.name}")
else:
    print("FINAL SELECTION: None")

ac.stop()
