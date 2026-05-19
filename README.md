# 🕵️ App Review Auditor

A local AI-powered tool that scrapes live Google Play Store reviews and uses **Llama 3** (running on-device via Ollama) to identify the top UX and technical failures — no cloud API keys required.

## Features
- 🔍 Search any app by name or package ID
- 📅 Filter reviews by Last 7 / 30 / 90 Days or All Time
- 🧠 On-device LLM analysis (fully private)
- 📥 One-click report download

## Setup

1. Install [Ollama](https://ollama.com) and pull the model:
```bash
ollama pull llama3
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run:
```bash
streamlit run researcher.py
```

## Tech Stack
Python · Streamlit · LangChain · Ollama · Llama 3 · Google Play Scraper
