import soundcard as sc
import numpy as np
import time

print("Scanning all devices for audio signal...")
print("Please play a loud video on YouTube now!\n")

try:
    # Get all mics including loopback
    mics = sc.all_microphones(include_loopback=True)
    
    for i, mic in enumerate(mics):
        print(f"[{i}] Testing: {mic.name}")
        try:
            # Record 0.5 seconds
            with mic.recorder(samplerate=16000) as recorder:
                data = recorder.record(numframes=8000) # 0.5s at 16k
                
                # Calculate energy
                if data.shape[1] > 1:
                    data = np.mean(data, axis=1)
                else:
                    data = data.flatten()
                
                energy = np.mean(np.abs(data))
                print(f"    Energy: {energy:.6f}")
                
                if energy > 0.001:
                    print("    *** ACTIVE SIGNAL DETECTED ***")
        except Exception as e:
            print(f"    Error recording: {e}")
        
        print("-" * 30)

except Exception as e:
    print(f"Fatal error: {e}")

print("\nDone.")
