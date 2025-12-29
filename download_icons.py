import os
import requests

icons = {
    "instagram.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png",
    "x.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/X_logo_2023_original.svg/450px-X_logo_2023_original.svg.png",
    "linkedin.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/LinkedIn_icon.svg/480px-LinkedIn_icon.svg.png",
    "github.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/480px-GitHub_Invertocat_Logo.svg.png"
}

save_dir = r"c:\Users\Abhay\Desktop\Chit_Chat\assets\icons"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

for name, url in icons.items():
    print(f"Downloading {name}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(os.path.join(save_dir, name), "wb") as f:
            f.write(response.content)
        print(f"Saved {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
