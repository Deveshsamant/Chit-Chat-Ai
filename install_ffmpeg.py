import os
import zipfile
import urllib.request
import shutil

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
DEST_DIR = os.path.join(os.getcwd(), "ffmpeg")

def download_ffmpeg():
    if os.path.exists(DEST_DIR):
        print("FFmpeg directory already exists. Skipping download.")
        return

    print(f"Downloading FFmpeg from {FFMPEG_URL}...")
    zip_path = "ffmpeg.zip"
    try:
        urllib.request.urlretrieve(FFMPEG_URL, zip_path)
        print("Download complete. Extracting...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        # Rename the extracted folder to 'ffmpeg'
        extracted_dirs = [d for d in os.listdir(".") if d.startswith("ffmpeg-") and os.path.isdir(d)]
        if extracted_dirs:
            shutil.move(extracted_dirs[0], "ffmpeg")
            
        print("Extraction complete.")
    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == "__main__":
    download_ffmpeg()
