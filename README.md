# 📦 AI Backend Service (FastAPI)

A scalable **Python FastAPI-based backend** that powers AI-driven features across **web and mobile applications**.
This service integrates with local/cloud LLMs, supports prompt-based workflows, and enables **document generation with preview and download capabilities**.

---

## 🚀 Features

* 🤖 **AI Prompt Processing**

  * Connects to local (e.g., Ollama) or external LLM APIs
  * Supports structured prompts via reusable templates (`.md` files)
  * Customizable system + user prompt architecture

* 📄 **Document Generation**

  * Generate dynamic documents (text, formatted content)
  * Supports job descriptions, personalized content, etc.

* 📑 **PDF Preview & Download**

  * Generate PDFs from processed content
  * Preview before download (via API endpoints)
  * Stream-based response handling

* 🌐 **Multi-Client Support**

  * Designed for both **mobile apps** and **web apps**
  * Clean REST API interface

* ⚙️ **Modular Architecture**

  * Prompt templates separated from code
  * Pluggable LLM providers
  * Scalable service structure

---

## 🧠 Architecture Overview

```
Client (Web/Mobile)
        ↓
FastAPI Backend
        ↓
Prompt Loader (.md templates)
        ↓
LLM (Ollama / API)
        ↓
Response Processing
        ↓
PDF Generation / JSON Response
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd project
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment variables

Create a `.env` file:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=mistral

# Optional
API_KEY=
```

---

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

---

## 🔗 LLM Integration

Supports:

* Local models via Ollama
* External APIs (OpenAI-compatible)

### Example (Ollama)

```python
POST /api/chat
{
  "model": "mistral",
  "messages": [...]
}
```

---

## 📄 PDF Generation

* Converts AI-generated content → formatted PDF
* Supports:

  * Preview (stream)
  * Download (file)

Libraries commonly used:

* `reportlab` / `weasyprint` / `pdfkit`

---

## 🛡️ Best Practices

* Keep prompts modular (`/prompts`)
* Use low temperature for deterministic outputs
* Validate input before sending to LLM
* Cache repeated requests when possible

---

## ⚠️ Limitations

* LLM responses depend on prompt quality
* Local models may require stronger constraints
* Some websites restrict scraping (if integrated)

---

## 🚀 Future Improvements

* Authentication & user sessions
* Prompt versioning system
* Multi-model routing (fallback strategy)
* Streaming responses
* RAG (Retrieval-Augmented Generation)

---

## 🤝 Contribution

Feel free to contribute by:

* Improving prompts
* Adding new endpoints
* Enhancing performance

---

## 📜 License

MIT License

---

## 💡 Summary

This backend acts as a:

```
AI Orchestrator + Prompt Engine + Document Generator
```

Designed to be reusable across platforms and extensible for future AI workflows.

---
