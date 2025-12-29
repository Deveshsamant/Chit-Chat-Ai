import os
import shutil
from huggingface_hub import snapshot_download
import whisper

def download_qwen_models():
    models = {
        "Qwen2.5-Coder-3B-Instruct": "Qwen/Qwen2.5-Coder-3B-Instruct",
        "Qwen2.5-1.5B-Instruct": "Qwen/Qwen2.5-1.5B-Instruct"
    }
    
    base_dir = os.path.join(os.getcwd(), "local_models")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    for local_name, repo_id in models.items():
        print(f"\n[1/3] Processing {local_name}...")
        model_path = os.path.join(base_dir, local_name)
        
        if os.path.exists(model_path):
            print(f"   - {local_name} already exists at {model_path}")
            # Optional: Check for completeness or just skip
        else:
            print(f"   - Downloading {local_name} from Hugging Face...")
            try:
                snapshot_download(repo_id=repo_id, local_dir=model_path)
                print(f"   - Download complete!")
            except Exception as e:
                print(f"   - Error downloading {local_name}: {e}")

def download_whisper_model():
    print(f"\n[3/3] Processing Whisper (Base)...")
    try:
        # Define local path
        local_whisper_path = os.path.join(os.getcwd(), "local_models", "whisper")
        if not os.path.exists(local_whisper_path):
            os.makedirs(local_whisper_path)
            
        # This triggers the download if not present
        print(f"   - Downloading/Loading Whisper base model to {local_whisper_path}...")
        whisper.load_model("base", download_root=local_whisper_path)
        print("   - Whisper download complete!")
    except Exception as e:
        print(f"   - Error downloading Whisper: {e}")

if __name__ == "__main__":
    print("=== Chit-Chat AI Model Downloader ===")
    print("This script will download all necessary AI models to 'local_models/'.")
    print("Total size: ~5-6 GB. Please ensure you have stable internet.\n")
    
    download_qwen_models()
    download_whisper_model()
    
    print("\n=== All Downloads Finished! ===")
    print("You can now run 'run_chit_chat.bat' to start the application.")
