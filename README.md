# 🎥 AI Video Assistant

An AI-powered application that converts **YouTube videos and local audio/video files into searchable, structured knowledge** using speech recognition, LLMs, embeddings, vector databases, and RAG.

The application automatically processes video/audio, extracts and prepares the audio, generates a transcript, creates an AI-powered summary, identifies action items, key decisions, and open questions, and builds a Retrieval-Augmented Generation (RAG) knowledge base that allows users to chat with the processed video.

## ✨ Key Features

- 🎬 **YouTube & Local File Support** — Process YouTube URLs and local MP3, WAV, M4A, MP4, WebM, and MOV files.
- 🎙️ **AI Transcription** — Uses **Faster-Whisper** for English and **Sarvam AI** for Hinglish-to-English transcription.
- 📝 **AI Summarization** — Automatically generates concise professional summaries from long transcripts.
- 📌 **Meeting Title Generation** — Generates a short title based on the video content.
- ✅ **Action Item Extraction** — Identifies tasks, owners, and deadlines from conversations.
- 🔑 **Decision Extraction** — Extracts important decisions made during the meeting.
- ❓ **Open Question Detection** — Identifies unresolved questions and follow-up topics.
- 🔎 **RAG-Based Search** — Converts transcripts into embeddings and stores them in **Chroma** for semantic retrieval.
- 💬 **Chat With Your Video** — Ask natural-language questions and receive answers based on the transcript.
- 🖥️ **Streamlit UI** — Interactive interface for processing videos, viewing results, and chatting with the processed content.
- 🖤 **Dark UI** — Black background with a clean white-text interface.

## 🏗️ Architecture

```text
Video / Audio
     ↓
Audio Processing & Chunking
     ↓
Faster-Whisper / Sarvam AI
     ↓
Transcript
     ↓
┌──────────────┬──────────────┬──────────────┐
│   Summary    │ Action Items │  Decisions   │
└──────────────┴──────────────┴──────────────┘
                     ↓
              Text Embeddings
                     ↓
                  Chroma
                     ↓
              Similarity Search
                     ↓
                 Groq LLM
                     ↓
                RAG Chat
```

## 🛠️ Tech Stack

**Python · Streamlit · Faster-Whisper · Sarvam AI · LangChain · Groq · Chroma · Hugging Face · PyTorch · FFmpeg**

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-video-assistant.git
cd AI-video-assistant
```

### 2. Create virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
SARVAM_STT_MODEL=saaras:v2.5
WHISPER_MODEL=base
```

### 5. Run the application

```powershell
streamlit run app.py
```

## 💬 Example Questions

After processing a video, you can ask:

```text
What was the main topic of the meeting?
What decisions were made?
Who was assigned each task?
What are the unresolved questions?
What was discussed about the project deadline?
```

## 🔐 Note

Do not commit your `.env`, API keys, `venv/`, downloaded media, or local vector database to GitHub.

---

### 🚀 Project Goal

Transform long-form video and meeting content into **structured summaries, actionable insights, and searchable knowledge through RAG**.
