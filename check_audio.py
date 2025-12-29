import soundcard as sc

print("Available Microphones (Input):")
for mic in sc.all_microphones(include_loopback=True):
    print(f" - {mic.name} (Loopback: {mic.isloopback})")

print("\nDefault Speaker (Output):")
default_speaker = sc.default_speaker()
print(f" - {default_speaker.name}")
