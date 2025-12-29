from huggingface_hub import snapshot_download
import os

# Define target folder
base_dir = os.path.join(os.getcwd(), "local_models")
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# 1.5B Model (Fast)
model_id = "Qwen/Qwen2.5-1.5B-Instruct"
local_dir = os.path.join(base_dir, "Qwen2.5-1.5B-Instruct")

print(f"Downloading {model_id} to: {local_dir}")
print("This includes the model weights (~3GB). Please wait...\n")

try:
    snapshot_download(
        repo_id=model_id,
        local_dir=local_dir,
        local_dir_use_symlinks=False,
        resume_download=True
    )
    print(f"\nDownload complete: {local_dir}")
except Exception as e:
    print(f"\nError downloading: {e}")
