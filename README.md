# Chit-Chat AI 🤖✨

**Chit-Chat AI** is a futuristic, transparent, always-on-top AI assistant that lives on your desktop. It listens to your voice or system audio, transcribes it in real-time, and provides intelligent responses using powerful local LLMs (Large Language Models).

Designed for developers, multitaskers, and sci-fi enthusiasts, it features a sleek "Iron Man" style HUD interface.

![Chit Chat UI](ui.png) 
*(Add a real screenshot here!)*

## 🚀 Features

*   **🎙️ Real-time Speech-to-Text**: Uses OpenAI's **Whisper** model (running locally) to capture your voice or system audio with high accuracy.
*   **🧠 Dual AI Brains**:
    *   **Smart Mode (3B)**: Powered by `Qwen2.5-Coder-3B-Instruct` for coding, logic, and complex reasoning.
    *   **Fast Mode (1.5B)**: Powered by `Qwen2.5-1.5B-Instruct` for quick, conversational speed.
    *   **Dynamic Switching**: Toggle between models instantly with a single click to balance speed vs. intelligence.
*   **🖥️ Transparent Overlay UI**: A frameless, semi-transparent window that stays on top of your work but lets you click through (interactive parts only).
*   **🕒 History & Live Modes**: Switch between a focused "Live View" (current Q&A) and a full "History View" of your session.
*   **🔒 100% Local Privacy**: All models run **locally** on your GPU. No data is sent to the cloud.
*   **👨‍💻 Developer Profile**: Integrated credits and social links.

## 🛠️ Installation

### Prerequisites
*   **OS**: Windows 10/11
*   **GPU**: NVIDIA GPU with CUDA support (Recommended: 6GB+ VRAM for 3B model, 4GB+ for 1.5B).
*   **Python**: 3.10+
*   **FFmpeg**: Must be installed and added to PATH (or let the app handle it).

### Step 1: Clone the Repository
```bash
git clone https://github.com/Deveshsamant/Chit-Chat-AI.git
cd Chit-Chat-AI
```

### Step 2: Set up Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```
*(Note: Create a `requirements.txt` based on your env, e.g., `transformers`, `accelerate`, `PyQt6`, `openai-whisper`, `soundcard`, `numpy`)*

### Step 4: Download Models
Run the included script to automatically download all necessary models (Qwen 3B, Qwen 1.5B, Whisper) to the `local_models/` directory.
```bash
python download_models.py
```
*This may take some time (~5-6 GB total).*

### Step 5: Download Icons (Optional)
To get the official social media icons for the profile:
```bash
python download_icons.py
```

## 🎮 Usage

1.  **Run the Application**:
    Double-click `run_chit_chat.bat` OR run:
    ```bash
    python main.py
    ```

2.  **Controls**:
    *   **Drag**: Click and drag anywhere on the window background to move it.
    *   **🧠 / ⚡ Button**: Toggle between the "Smart" (3B) and "Fast" (1.5B) model.
    *   **🕒 Button**: Toggle between Live Chat and History view.
    *   **👨‍💻 Button**: View Developer Profile.
    *   **─ / □ / ✕**: Minimize, Maximize/Restore, Close.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author
Made with ❤️ by **Devesh Samant**.

*   [Instagram](https://www.instagram.com/devesh.samant/)
*   [X (Twitter)](https://x.com/DeveshSama32978)
*   [LinkedIn](https://www.linkedin.com/in/devesh-samant-b78376258/)
*   [GitHub](https://github.com/Deveshsamant)
