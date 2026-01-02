# Chit-Chat AI 🤖✨

**Chit-Chat AI** is a futuristic, transparent, always-on-top AI assistant that lives on your desktop. It listens to your voice or system audio, transcribes it in real-time, and provides intelligent responses using powerful local LLMs (Large Language Models).

Designed for developers, multitaskers, and sci-fi enthusiasts, it features a sleek "Iron Man" style HUD interface.

![Chit Chat UI](ui.png) 

## 🚀 Key Features

*   **⚡ Fast Interview Mode**: Optimized for rapid-fire Q&A with **token-by-token streaming**, giving you answers the moment they are generated.
*   **🧠 Strict Code Generator**: Built for efficiency—provides **optimized code solutions** immediately with complexity analysis (Time/Space O-notation), cutting out all conversational fluff.
*   **📝 Edit & Correct**: Misheard query? Instantly **edit your last spoken request** using the pencil icon to get the right answer without repeating yourself.
*   **🎙️ Smart Speech Recognition**: Powered by **Faster-Whisper (Small Model)**, finetuned for better understanding of diverse accents (including Indian English) and fast detection.
*   **🖥️ Transparent Overlay UI**:
    *   **Frameless Design**: Floats seamlessly over your IDE or browser.
    *   **Click-Through**: Drag via Title Bar only, ensuring you can select and copy text easily.
    *   **Compact Mode**: Reduced font sizes and minimalist controls for less distraction.
*   **🛡️ Privacy First**: Runs **100% Locally**. No data leaves your machine.
*   **📦 Ready to Run**: Models are included via Git LFS—no manual downloads required!

## 🛠️ Installation

### Prerequisites
*   **OS**: Windows 10/11
*   **GPU**: NVIDIA GPU with CUDA support (Recommended).
*   **Python**: 3.10+
*   **Git LFS**: Required for downloading models.

### Step 1: Clone with LFS
```bash
# Make sure you have Git LFS installed
git lfs install

# Clone the repository (this will download the ~2GB models automatically)
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

## 🎮 Usage

1.  **Run the Application**:
    ```bash
    python main.py
    ```

2.  **Controls**:
    *   **✏️ Edit**: Click the pencil icon to correct the last question.
    *   **Drag**: Move the window by dragging the **Title Bar**.
    *   **Right-Click**: Copy text from the chat window.
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
