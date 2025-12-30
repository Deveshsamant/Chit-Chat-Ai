import soundcard as sc
import numpy as np
import time

def test_recording(block_size=1024, duration=5):
    print(f"Testing with Block Size: {block_size}")
    mic = sc.default_microphone()
    print(f"Using Microphone: {mic.name}")
    
    start_time = time.time()
    try:
        with mic.recorder(samplerate=16000) as recorder:
            while time.time() - start_time < duration:
                data = recorder.record(numframes=block_size)
                energy = np.mean(np.abs(data))
                print(f"Recorded block. Energy: {energy:.6f}")
                # Simulate some processing delay to mimic app load
                # time.sleep(0.01) 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("--- Test 1: Standard Block Size (1024) ---")
    test_recording(block_size=1024)
    
    print("\n--- Test 2: Larger Block Size (4096) ---")
    test_recording(block_size=4096)
