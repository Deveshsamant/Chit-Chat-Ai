# Chit-Chat AI 🤖✨

**Chit-Chat AI** is a futuristic, transparent, always-on-top AI assistant that lives on your desktop. It listens to your voice or system audio, transcribes it in real-time, and provides intelligent responses using powerful local LLMs (Large Language Models).

Designed for developers, multitaskers, and sci-fi enthusiasts, it features a sleek "Iron Man" style HUD interface.

![Chit Chat UI](ui.png) 

## 🚀 Features

*   **⚡ Ultra-Fast Local Engine**: Powered by **GGUF** models (`llama.cpp`) for extreme performance on consumer GPUs.
    *   **Model**: `Qwen2.5-Coder-3B-Instruct` (Quantized to 4-bit for speed/efficiency balance).
*   **🎙️ Real-time Speech-to-Text**: Uses **Faster-Whisper** (CTranslate2 backend) for lightning-fast, high-accuracy transcription.
*   **🖥️ Transparent Overlay UI**: A frameless, semi-transparent window that stays on top of your work.
*   **🛡️ Screen Capture Protection**: The application window is exclusion-ready for screen recordings.
*   **🎙️ Smart Audio Input**: Automatically detects speech (VAD) and filters background noise.
*   **🕒 History & Live Modes**: Switch between a focused "Live View" (current Q&A) and a full "History View" of your session.
*   **🔒 100% Local Privacy**: All models run **locally**. No data is sent to the cloud.
*   **👨‍💻 Developer Profile**: Integrated credits and social links.

## 🛠️ Installation

### Prerequisites
*   **OS**: Windows 10/11
*   **GPU**: NVIDIA GPU with CUDA support (Recommended).
*   **Python**: 3.10+
*   **FFmpeg**: Must be in PATH for audio processing.

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
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install project requirements
pip install -r requirements.txt
```
*Required packages include: `llama-cpp-python`, `faster-whisper`, `PyQt6`, `soundcard`, `numpy`.*

### Step 4: Download Model
1.  Create a folder named `local_models` in the project root.
2.  Download `qwen2.5-coder-3b-instruct-q4_k_m.gguf` from Hugging Face.
3.  Place it in `local_models/`.

## 🎮 Usage

1.  **Run the Application**:
    ```bash
    python main.py
    ```

2.  **Controls**:
    *   **Drag**: Click and drag anywhere to move.
    *   **🕒 Button**: Toggle History view.
    *   **👨‍💻 Button**: View Developer Profile.
    *   **─ / □ / ✕**: Minimize, Maximize, Close.

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
