# 🌐 Vernacular AI — Next-Gen Multimodal Vernacular Education & Cinema Dubbing Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg?logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203-003B57.svg?logo=sqlite)](https://sqlite.org/)
[![Languages](https://img.shields.io/badge/Supported%20Languages-51%20Total-success.svg)](#-51-supported-languages)
[![Offline](https://img.shields.io/badge/Offline%20Engine-100%25%20Resilient-orange.svg)](#-zero-connectivity-offline-resilience)
[![NEP 2020](https://img.shields.io/badge/NEP%202020-Mother%20Tongue%20Compliant-purple.svg)](#-nep-2020-alignment)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Empowering non-English speakers across India and the globe to learn STEM concepts and enjoy world cinema in their true mother tongue.**

---

## 🌟 Key Features & Innovations

### 1. 📚 Mother-Tongue Pedagogy Deconstruction
* **Not just verbatim translation**: Automatically breaks down educational lessons into:
  * 🧪 **Scientific Vocabulary Glossary Table** (Original concept term vs. Vernacular meaning).
  * 💡 **Child-Friendly Conceptual Explanation** (Explains "Why & How" in simple mother tongue).
  * 🎯 **Interactive 2-Question Mini-Quizzes** (Tests student comprehension in their native language).
  * 💬 **Mother-Tongue Doubt Assistant** (Students ask doubts and get pedagogical native explanations).

### 2. ⚡ Zero-Connectivity Offline Resilience Layer
* **100% Offline Functional**: Never crashes when the internet goes down.
* **Embedded Vernacular Lexicon**: Includes local offline dictionaries for essential STEM terms, question templates, and cinema dialogue across Tamil, Hindi, Telugu, Malayalam, and more.
* **Instant SQLite Cache Lookup**: Repeated queries retrieve in `<2ms` from local SQLite without hitting external APIs.

### 3. 🎬 Cinema AI Vernacular Dubbing & Subtitle Studio
* **English Movies for Non-English Audiences**:
  * Upload your own English video file (`.mp4`, `.webm`, `.mkv`) or select iconic cinema scenes (*The Pursuit of Happyness, Interstellar, Oppenheimer, BBC Planet Earth*).
  * **Bilingual Dynamic Subtitles**: English source + Large stylized Vernacular subtitles overlaid in real-time.
  * **AI Voice Dubbing**: Synchronized vernacular voiceover audio ducking with adjustable volume.
  * **Cultural & Idiom Decoder**: Explains American/British cinema slang and idioms (e.g., *"Period"*, *"Break a leg"*, *"Piece of cake"*) into intuitive vernacular meaning.
  * **Download `.SRT` Subtitle Files**: Export standard subtitle files ready for VLC, MX Player, or YouTube.

### 4. 📹 Live Video / Webcam AR Subtitle Studio
* Real-time camera feed with futuristic AR floating vernacular subtitles.
* WebkitSpeechRecognition + SpeechSynthesis synchronization for live classroom lectures.

### 5. 📡 4-Language Simultaneous Broadcast Grid
* Input 1 lesson in English and broadcast it concurrently into **4 regional languages** (e.g. Tamil, Hindi, Telugu, Malayalam) in real-time using parallel thread workers.

### 6. 📄 Formatted PDF Study-Sheet & JSON Export
* 1-Click generation of printable, school-ready revision study sheets (`window.print`) with official header, vocabulary glossary table, explanation, and mini-quiz.

### 7. 📑 Academic & Technical Project Report Generator
* Generates publication-grade IEEE/ACM-style academic project reports with Abstract, Architecture, Benchmarks, and NEP 2020 analysis in printable PDF and downloadable Markdown format.

### 8. 🗄️ Zero-Config Local SQLite Database
* Persistent local database stored at `backend/vernacular_ai.db`.
* In-app database explorer modal to inspect records, toggle favorites, and export data as CSV/JSON.

---

## 🏗️ System Architecture

```
                                  +---------------------------------------+
                                  |         Web Frontend (SPA)            |
                                  |  HTML5 Canvas, Web Speech API (TTS/STT)|
                                  +-------------------+-------------------+
                                                      |
                                                      | HTTP / REST
                                                      v
                                  +---------------------------------------+
                                  |         Flask Backend API             |
                                  |        (http://127.0.0.1:5000)        |
                                  +-------------------+-------------------+
                                                      |
                   +----------------------------------+----------------------------------+
                   |                                  |                                  |
                   v                                  v                                  v
+------------------------------------+ +-------------------------------+ +--------------------------------+
|      Multi-Tier Translation        | |    Multimodal Studios         | |   Embedded SQLite Database     |
| • Tier 1: Local SQLite Cache       | | • Cinema Dubbing & Subtitles  | | • vernacular_ai.db             |
| • Tier 2: Neural Translation APIs  | | • AR Webcam Subtitle Studio   | | • Full History & Starred Cards |
| • Tier 3: Offline Lexicon & Rules  | | • Classroom Lecture Sim       | | • CSV / JSON Data Exporter     |
+------------------------------------+ +-------------------------------+ +--------------------------------+
```

---

## 🌐 51 Supported Languages

### Indian Regional Vernaculars (26)
| Language | Script / Native | Region | Language | Script / Native | Region |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tamil** | தமிழ் | Tamil Nadu | **Hindi** | हिन्दी | Pan-India |
| **Telugu** | తెలుగు | Andhra / Telangana | **Malayalam** | മലയാളം | Kerala |
| **Kannada** | ಕನ್ನಡ | Karnataka | **Bengali** | বাংলা | West Bengal |
| **Marathi** | मराठी | Maharashtra | **Gujarati** | ગુજરાતી | Gujarat |
| **Punjabi** | ਪੰਜਾਬੀ | Punjab | **Odia** | ଓଡ଼ିଆ | Odisha |
| **Urdu** | اردو | Pan-India | **Assamese** | অসমীয়া | Assam |
| **Sanskrit**| संस्कृतम् | Classical | **Nepali** | नेपाली | North/Sikkim |
| **Sindhi** | سنڌي | Sindh / Kutch | **Maithili** | मैथिली | Bihar |
| **Konkani** | कोंकणी | Goa / Coastal | **Manipuri**| মৈতৈলোন্ | Manipur |
| **Bodo** | बर' | Assam | **Dogri** | डोगरी | Jammu |
| **Kashmiri**| کٲشُر | Kashmir | **Santali** | ᱥᱟᱱᱛᱟᱲᱤ | Jharkhand |
| **Bhojpuri**| भोजपुरी | UP / Bihar | **Tulu** | ತುಳು | Coastal Karnataka|
| **Rajasthani**| राजस्थानी| Rajasthan | **Haryanvi** | हरियाणवी | Haryana |

### Global Languages (25)
English, French, German, Spanish, Arabic, Japanese, Chinese, Russian, Korean, Italian, Portuguese, Turkish, Dutch, Swedish, Polish, Persian, Indonesian, Thai, Vietnamese, Malay, Greek, Hebrew, Ukrainian, Czech, Romanian.

---

## 🚀 Quickstart Guide

### Option 1: 1-Click Launcher (Windows)
Double-click [`run_project.bat`](run_project.bat) in the project root. It will:
1. Verify Python virtual environment (`backend/venv`).
2. Install dependencies automatically if missing.
3. Launch the server on `http://127.0.0.1:5000`.
4. Open the application directly in your default browser!

### Option 2: Manual Setup
```bash
# 1. Clone repository
git clone https://github.com/<your-username>/Vernacular_AI.git
cd Vernacular_AI

# 2. Enter backend and setup virtualenv
cd backend
python -m venv venv

# Windows activate:
venv\Scripts\activate
# Linux/macOS activate:
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Start Flask Server
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | Service status, total languages, and database statistics |
| `/api/languages` | `GET` | List of all 51 supported languages with flags and speech tags |
| `/api/translate` | `POST` | Translates lesson text, generates vocabulary glossary, explanation, and mini-quiz |
| `/api/translate/broadcast`| `POST`| Concurrently translates single input into 4 regional target languages |
| `/api/ask_doubt` | `POST` | Answers student questions based on lesson context in their mother tongue |
| `/api/cinema/scenes` | `GET` | Retrieves pre-loaded cinema scenes and metadata |
| `/api/cinema/translate` | `POST` | Translates movie dialogue with cultural idiom explanations |
| `/api/cinema/export_srt` | `POST` | Exports translated subtitles as standard `.srt` file |
| `/api/project/report` | `GET` | Generates comprehensive academic & technical evaluation report |
| `/api/project/report/download`| `GET`| Downloads academic report as Markdown document |
| `/api/history` | `GET` / `DELETE`| Inspect or clear local SQLite translation history |
| `/api/favorite/<id>` | `POST` | Toggles star / bookmark status of an educational card |
| `/api/database/info` | `GET` | Inspects exact SQLite file path, disk size, and table schema |
| `/api/database/export` | `GET` | Exports all database records as CSV or JSON |

---

## 🏛️ NEP 2020 Alignment

India's **National Education Policy (NEP 2020)** emphasizes:
* **Section 4.11**: Medium of instruction in the home language / mother tongue wherever possible until at least Grade 8.
* **Section 4.13**: Multilingualism and the power of language in cognitive learning.
* **Vernacular AI** serves as an open, accessible reference implementation bridging academic literature and classroom reality.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
