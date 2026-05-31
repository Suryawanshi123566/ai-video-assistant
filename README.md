<div align="center">

# 🎬 InsightFlow
### AI-Powered Meeting & Video Intelligence Platform

**Transform any YouTube video or meeting recording into structured, actionable intelligence.**  
Transcribe → Summarise → Extract → Query — all in one pipeline.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Mistral AI](https://img.shields.io/badge/Mistral-AI-FF7000?style=flat-square)](https://mistral.ai)
[![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/r/sakshis164/insightflow)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

</div>

---

## 📌 What is InsightFlow?

InsightFlow is an end-to-end AI pipeline that takes a **YouTube URL or local audio/video file** and returns:

- 📝 **Full transcript** (supports English and Hinglish)
- 📋 **Concise summary** of the content
- ✅ **Action items** extracted automatically
- 🔑 **Key decisions** made during the meeting
- ❓ **Open questions** that remain unresolved
- 💬 **RAG-powered chat** — ask anything about the transcript

Built with **OpenAI Whisper** (local STT), **Mistral AI** (LLM), **LangChain** (orchestration), and **ChromaDB** (vector store) — all surfaced through a clean **Streamlit** UI.

---

## 🖼️ Demo

> Paste a YouTube URL → click **Run Analysis** → get full intelligence breakdown + chat with your transcript.

```
InsightFlow
├── Sidebar: Paste URL / Select Language / Run Analysis
├── Main Panel: Title Banner + Summary + Full Transcript
├── Cards: Action Items | Key Decisions | Open Questions
└── Chat: Ask the transcript via RAG
```

---

## 🏗️ Architecture

```
Input (YouTube URL / Local File)
        │
        ▼
┌───────────────────┐
│  Audio Processor  │  ← yt-dlp + pydub + ffmpeg
└────────┬──────────┘
         │  audio chunks
         ▼
┌───────────────────┐
│    Transcriber    │  ← OpenAI Whisper (local) / Sarvam (Hinglish)
└────────┬──────────┘
         │  raw transcript
         ▼
┌─────────────────────────────────────────┐
│            LangChain + Mistral AI        │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │Summarizer│  │Extractor │  │  RAG   │ │
│  │          │  │ Actions  │  │ Engine │ │
│  │          │  │Decisions │  │ChromaDB│ │
│  │          │  │Questions │  │        │ │
│  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
         │
         ▼
  Streamlit UI (InsightFlow)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit |
| **Audio Extraction** | yt-dlp, pydub, ffmpeg |
| **Speech-to-Text** | OpenAI Whisper (local, CPU) |
| **Translation** | deep-translator (Hinglish support) |
| **LLM** | Mistral AI via LangChain |
| **Search / RAG** | Tavily API + ChromaDB + HuggingFace Embeddings |
| **Orchestration** | LangChain LCEL |
| **Containerisation** | Docker |

---

## 🚀 Quick Start

### Option 1 — Docker (Recommended, no setup needed)

```bash
docker pull sakshis164/insightflow:latest

docker run -p 8501:8501 \
  -e MISTRAL_API_KEY=your_mistral_key \
  -e TAVILY_API_KEY=your_tavily_key \
  sakshis164/insightflow:latest
```

Open **http://localhost:8501** in your browser. Done.

---

### Option 2 — Run Locally

#### 1. Clone the repo

```bash
git clone https://github.com/Suryawanshi123566/ai-video-assistant.git
cd ai-video-assistant
```

#### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r Requirements.txt
```

> ⚠️ **FFmpeg** must be installed separately on your system.  
> Windows: `winget install ffmpeg` | macOS: `brew install ffmpeg` | Linux: `sudo apt install ffmpeg`

#### 4. Set up environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your keys:
- Mistral → [console.mistral.ai](https://console.mistral.ai)
- Tavily → [app.tavily.com](https://app.tavily.com)

#### 5. Run the app

```bash
# Streamlit UI
streamlit run app.py

# OR CLI mode
python main.py
```

---

## 📁 Project Structure

```
ai-video-assistant/
│
├── app.py                  # Streamlit web UI (InsightFlow)
├── main.py                 # CLI entry point
├── test.py                 # Quick pipeline test script
├── Requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── .dockerignore           # Docker build exclusions
├── .gitignore
│
├── core/
│   ├── transcriber.py      # Whisper / Sarvam STT
│   ├── summarizer.py       # LLM summarization + title generation
│   ├── extractor.py        # Action items, decisions, questions
│   └── rag_engine.py       # ChromaDB vector store + RAG chain
│
└── utils/
    └── audio_processor.py  # yt-dlp download + audio chunking
```

---

## 🌐 Language Support

| Language | Engine | Notes |
|---|---|---|
| **English** | OpenAI Whisper (local) | Default, runs fully offline |
| **Hinglish** | Sarvam AI / deep-translator | Hindi-English mixed speech |

---

## 🐳 Docker Details

The Docker image uses **PyTorch CPU-only** to keep the image lean (~2.7 GB).  
Whisper model is downloaded on first transcription run.

**Persist Whisper model cache** (avoids re-download on container restart):

```bash
docker run -p 8501:8501 \
  -e MISTRAL_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  -v whisper_cache:/root/.cache/whisper \
  sakshis164/insightflow:latest
```

**Docker Hub:** [hub.docker.com/r/sakshis164/insightflow](https://hub.docker.com/r/sakshis164/insightflow)

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `MISTRAL_API_KEY` | ✅ Yes | Mistral AI API key for LLM tasks |
| `TAVILY_API_KEY` | ✅ Yes | Tavily API key for RAG search |

---

## 📦 Key Dependencies

```
openai-whisper       # Local speech-to-text
langchain            # LLM orchestration
langchain-mistralai  # Mistral integration
chromadb             # Local vector store
sentence-transformers # HuggingFace embeddings
yt-dlp               # YouTube audio download
streamlit            # Web UI
deep-translator      # Hinglish translation
```

Full list → [`Requirements.txt`](Requirements.txt)

---

## 🛣️ Roadmap

- [x] YouTube URL support
- [x] Local file support (mp4, mp3, wav)
- [x] English transcription (Whisper)
- [x] Hinglish support
- [x] Summarization + extraction pipeline
- [x] RAG-powered Q&A chat
- [x] Streamlit UI
- [x] Docker support
- [ ] Speaker diarization (who said what)
- [ ] PDF / DOCX export of results
- [ ] Multi-language support beyond Hinglish
- [ ] Cloud deployment (Streamlit Cloud / HuggingFace Spaces)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Suryawanshi** — [@Suryawanshi123566](https://github.com/Suryawanshi123566)

---

<div align="center">

⭐ **Star this repo if you found it useful!** ⭐

</div>
