# AI-Desktop-Pet-Local — Your AI Desktop Companion

&gt; "She is not a tool, but a little soul living inside your computer."

**AI-Desktop-Pet-Local** is an AI desktop pet project built on **Electron + FastAPI + DeepSeek V4**. She can understand your voice (local speech recognition), remember things about you (memory system), proactively initiate conversations (autonomous consciousness), and even view screenshots (multimodal interface reserved).

Inspired by Vedal / Neuro-sama, this project is entirely independently developed by an individual and serves as an AI desktop pet prototype for learning, experimentation, and companionship.

---

## ✨ Features

- 🎤 **Voice Interaction (Local Recognition)**

  Supports two modes: always-on microphone (real-time listening) and push-to-talk (hold to record, release to send). Speech recognition is powered by the local **Qwen3-ASR** model, requiring no internet connection.

- 🧠 **Powered by DeepSeek V4**

  Utilizes DeepSeek V4 as the "brain," supporting emotion recognition, memory read/write, proactive speech, and character persona.

- 💾 **Memory System**

  Short-term conversation history + long-term factual memory. She will remember important things you've told her.

- 🖥️ **Transparent Desktop Window**

  A transparent, always-on-top, borderless window based on Electron — like a true "desktop spirit."

- 🔔 **System Notification Integration**

  Mode switching and recording status are indicated via native Windows notifications for stronger immersion.

- 🧩 **Proactive Consciousness Loop**

  After a period of idleness, she will proactively bring up topics so the conversation never goes cold.

- 👁️ **Visual Capability Reserved**

  A screenshot interface has been reserved, allowing integration with multimodal models (e.g., Gemini / Gemma) to enable "speaking from images."

---

## 🛠️ Tech Stack

| Module | Technology |
|--------|------------|
| Desktop Frontend | `Electron + React + Vite` |
| Backend Service | `FastAPI + WebSocket` |
| LLM Brain | `DeepSeek V4 (OpenAI-compatible format)` |
| Speech Recognition (STT) | `Qwen3-ASR-0.6B (Local ONNX + FunASR)` |
| Text-to-Speech (TTS) | `Reserved interface (supports Edge TTS / SiliconFlow)` |
| Memory System | `JSON local storage + vector retrieval (reserved)` |
| Real-time Communication | `WebSocket (bidirectional)` |

---

## 📦 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lanxianxun/AI-Desktop-Pet-Local.git
cd AI-Desktop-Pet-Local
```

### 2. Backend Configuration & Startup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your DeepSeek API Key:

```env
LLM_BASE_URL="https://api.deepseek.com/v1"
LLM_API_KEY="sk-your-key"
LLM_MODEL="deepseek-v4-flash"
```

Start the backend:

```bash
python main.py
```

### 3. Voice Model Configuration (Optional)

This project uses local speech recognition. The model will be automatically downloaded on first run (approximately 1.8 GB):

- **Model Source:** ModelScope — [Qwen/Qwen3-ASR-0.6B](https://www.modelscope.cn/models/Qwen/Qwen3-ASR-0.6B)
- **Cache Path:** `~/.cache/modelscope/`

For offline usage, manually download the model files and modify the model path in `services.py` to the local folder address.

### 4. Frontend Startup

```bash
cd frontend
npm install
npm run dev
```

### 5. Desktop App Packaging

```bash
npm run build
npm run electron
```

---

## 📁 Project Structure

```text
AI-Desktop-Pet-Local/
├── backend/
│   ├── main.py              # FastAPI main application
│   ├── services.py          # AI services (LLM + STT)
│   ├── memory.py            # Memory system
│   ├── tools.py             # Screenshot and other tools
│   └── voice_service.py     # Local speech recognition wrapper
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # WebSocket / audio hooks
│   │   └── pages/           # Main interface
│   ├── electron-main.cjs    # Electron main process
│   └── package.json
└── README.md
```

---

## 🎮 Interaction Guide

| Operation | Description |
|-----------|-------------|
| `Alt + T` | Toggle mode (Always-on / Push-to-talk) |
| `Alt + P` | Push-to-talk (Hold to record, release to send) |
| Click 🎤 button | Manual control for recording start/stop |
| Text input box | Supports text chat (fallback) |

---

## 🙏 Acknowledgements

- **Vedal & Neuro-sama** — For the original inspiration and direction
- **DeepSeek** — For providing a powerful and affordable AI brain
- **ModelScope** — For supporting local speech models
- **Electron & FastAPI** — For making desktop AI applications possible

---

## 🌟 Closing Words

If you like this project, feel free to ⭐ Star, Fork, and submit PRs.  
If you have any ideas or suggestions, open an Issue or reach out directly via email (see GitHub Profile).

&gt; *"She may not be perfect, but she was created by my own hands."*
