import zipfile
import os
import shutil

def extract_ffmpeg():
    zip_path = "ffmpeg.zip"
    if not os.path.exists(zip_path):
        print("ffmpeg.zip not found!")
        return

    print("Extracting ffmpeg.zip...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        extracted_dirs = [d for d in os.listdir(".") if d.startswith("ffmpeg-") and os.path.isdir(d)]
        if extracted_dirs:
            # remove existing ffmpeg folder if exists
            if os.path.exists("ffmpeg"):
                 shutil.rmtree("ffmpeg")
            
            shutil.move(extracted_dirs[0], "ffmpeg")
            print("FFmpeg extracted to ./ffmpeg")
        else:
            print("Could not find extracted ffmpeg folder.")
            
    except zipfile.BadZipFile:
        print("Error: Bad Zip File. Download might be incomplete.")
    except Exception as e:
        print(f"Error extracting: {e}")

if __name__ == "__main__":
    extract_ffmpeg()
