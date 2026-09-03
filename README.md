# 🤖 ReneroBot - Desktop AI Chatbot with Persistent Memory

**ReneroBot** is a modern Python desktop conversational chatbot application built with **CustomTkinter**, powered by the **Google Gemini API (`gemini-1.5-flash`)**, and integrated with **OpenCV** for dynamic video background rendering.

Designed with both user experience and clean software architecture in mind, ReneroBot features short-term conversation context tracking, persistent long-term memory storage, dynamic typewriter text animations, and an asynchronous non-blocking GUI architecture.

---

## ✨ Features

- 🤖 **Google Gemini 1.5 Flash Integration:** Delivers fast, context-aware AI responses.
- 🧠 **Persistent Long-Term Memory:** Automatically recognizes and retains user memories (e.g., preferences, facts) saved to structured JSON storage across app sessions.
- 💬 **Conversation Context Buffer:** Maintains recent message history for natural multi-turn conversations.
- 🎨 **Modern Desktop UI:** Built using `CustomTkinter` with dark/light mode toggling, custom styling, typing speed effects, and clean chat box layout.
- 🎥 **Animated Video Background:** Dynamically streams background animations frame-by-frame via `OpenCV` and `Pillow`.
- ⚡ **Asynchronous Threading:** Offloads API network operations to background threads, guaranteeing that the user interface never freezes or stutters during responses.
- 🔐 **Secure Configuration:** Zero hardcoded credentials—managed cleanly through `.env` environment variables using `python-dotenv`.

---

## 🛠️ Project Structure

```text
.
├── main.py                     # Main application entry point
├── requirements.txt            # Minimal required Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules for secrets and runtime data
├── ChatBot/
│   ├── __init__.py
│   ├── chatbot.py              # Gemini API interaction and long-term memory logic
│   ├── InterfaceGrafic.py      # CustomTkinter GUI layout, event handling & threading
│   ├── Perguntas.py            # Welcome greeting generator
│   └── CustomSearch.py         # Google Custom Search API client module
├── Arquivos TxT e Pdfs/        # UX research assets (Persona profiles, Style guide, Mood board)
└── imagens/                    # Visual assets (Background video, favicons, UI icons)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed on Windows.
- A **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/)).

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/ReneroBot.git
   cd ReneroBot
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows Command Prompt / PowerShell:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and add your Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

5. **Run the Application:**
   ```bash
   python main.py
   ```

---

## 💡 How Memory Works

ReneroBot actively tracks key user information during conversations.
- **Short-term memory:** Keeps up to 20 recent conversation turns in memory buffer for immediate context.
- **Long-term memory:** When the AI outputs a memory keyword (formatted as `Memória: key=value`), ReneroBot automatically extracts and updates `memoria_bot/memorias.json`. Subsequent sessions load these memories into the system prompt context.

---

## 📐 UX Design & Research Assets

This project was built following structured user experience design principles:
- **Personas (`Arquivos TxT e Pdfs/PERSONA.txt`):** Target user research and expectations defined during initial design.
- **Style Guide & Mood Board (`Arquivos TxT e Pdfs/`):** Color palette definitions, typography choices (`COCOMAT`, `Inter`, `Michroma`), and visual themes.

---

## 📜 License

Distributed under the MIT License. Feel free to modify and adapt for personal or educational use!


Btw, this was my ever fist project, so don't expect much.
