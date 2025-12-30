import soundcard as sc

print("--- Available Input Devices ---")
mics = sc.all_microphones(include_loopback=True)
for i, mic in enumerate(mics):
    print(f"Index: {i}")
    print(f"  Name: {mic.name}")
    print(f"  ID: {mic.id}")
    print(f"  Is Loopback: {mic.isloopback}")
    print("-" * 30)

print("\n--- Default System Mic ---")
try:
    default = sc.default_microphone()
    print(f"Name: {default.name}")
except:
    print("None")
