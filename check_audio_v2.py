import soundcard as sc

try:
    default_speaker = sc.default_speaker()
    print(f"Default Speaker: {default_speaker.name} (ID: {default_speaker.id})")
except Exception as e:
    print(f"Error getting default speaker: {e}")

print("\nAll Microphones (include_loopback=True):")
try:
    mics = sc.all_microphones(include_loopback=True)
    for i, mic in enumerate(mics):
        print(f"[{i}] Name: {mic.name}")
        print(f"    ID: {mic.id}")
        print(f"    Is Loopback: {mic.isloopback}")
except Exception as e:
    print(f"Error listing microphones: {e}")
