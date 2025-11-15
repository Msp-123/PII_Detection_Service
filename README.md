# PII Detection Service

A lightweight, customizable, and fully local **PII (Personally Identifiable Information) detection and redaction service** built with **FastAPI**, **Microsoft Presidio**, and a **BERT-based NER model**.

This service runs entirely **offline**, without sending your data to any cloud provider.  
Designed for simplicity, flexibility, and developer-friendly extensibility.  
Currently supports **English**, with multi-language support planned for future versions.

---

## Features

- **FastAPI** backend with high-performance asynchronous endpoints  
- **Microsoft Presidio Analyzer** for rule-based PII detection  
- **Custom BERT NER Recognizer** using:  
  - Model: `dslim/bert-base-NER`  
  - Supported entities: `PERSON`, `ORG`, `LOC`  
- **Regex-based Recognizers** for:
  - Email (`EMAIL_ADDRESS`)
  - US phone numbers (`PHONE_NUMBER-R`)
  - US Social Security Numbers (`US_SSN`)
- **Customizable redaction policies:**
  - `template` (e.g., `{{ENTITY_TYPE}}`)
  - `asterisk`
  - `hash`
- **Fully local processing** — no cloud API calls
- Auto-generated API documentation via **Swagger UI** (`/docs`)

---

## Project Structure
```text
PII_Detection_Service/
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── config.py
│   ├── main.py
│   ├── schemas.py
│   ├── security.py
│   └── recognizers/
│       ├── __init__.py
│       ├── bert_ner_recognizer.py
│       └── regex_recognizers.py
│
├── tests/
│   └── __init__.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── setup.cfg

__pycache__, virtual environments, and .env files are intentionally excluded via .gitignore.

---
## Architecture Overview

### 1. BERT NER Recognizer

Located in app/recognizers/bert_ner_recognizer.py

Uses dslim/bert-base-NER with entity mapping:
| Model Label | Presidio Entity |
| ----------- | --------------- |
| PER         | PERSON          |
| ORG         | ORGANIZATION    |
| LOC         | LOCATION        |


### 2. Regex Recognizers

Located in: app/recognizers/regex_recognizers.py

Includes:
  - EMAIL_ADDRESS
  - PHONE_NUMBER-R (US format; will be enhanced)
  - US_SSN

### 3. Analyzer Engine Setup

Located in: app/analyzer.py

Registers:
  - BERT recognizer
  - Regex recognizers
  - Presidio internal recognizers (if needed)

4. API Layer

Defined in: app/main.py

| Endpoint  | Method | Description              |
| --------- | ------ | ------------------------ |
| `/health` | GET    | Health check             |
| `/detect` | POST   | Detect PII entities      |
| `/redact` | POST   | Redact/mask PII entities |
| `/docs`   | GET    | Swagger UI               |


## Installation

### 1. Clone the repository
git clone https://github.com/<username>/PII_Detection_Service.git
cd PII_Detection_Service

### 2. Create & activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
# source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Environment variables
cp .env.example .env


## Running the Application
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

API base URL:
http://127.0.0.1:8000

Swagger documentation:
http://127.0.0.1:8000/docs

## API Endpoints

### 1. Health Check
GET /health
{
  "status": "ok"
}

## 2. Detect PII
POST /detect

Request:
{
  "text": "John Doe lives in New York. Email: john@example.com",
  "entities": ["PERSON", "EMAIL_ADDRESS"],
  "min_score": 0.5
}

Response:
{
  "entities": [
    {
      "type": "PERSON",
      "value": "John Doe",
      "start": 0,
      "end": 8,
      "score": 0.99
    },
    {
      "type": "EMAIL_ADDRESS",
      "value": "john@example.com",
      "start": 33,
      "end": 50,
      "score": 0.94
    }
  ]
}

### 3. Redact PII
POST /redact

Request:
{
  "text": "John Doe lives in New York.",
  "policy": {
    "mask_mode": "template",
    "template": "{{ENTITY_TYPE}}",
    "entities_to_mask": ["PERSON"]
  }
}

Response:
{
  "masked_text": "{{PERSON}} lives in New York."
}

## Customization
You can easily:
  - Add new regex recognizers
  - Add new ML-based recognizers
  - Replace the NER model (e.g., multilingual BERT)
  - Modify masking templates
  - Extend the FastAPI endpoints

## Roadmap
  - Turkish PII support
  - Device & domain-specific fine-tuned models
  - Stronger phone number regex
  - Docker support
  - Unit & integration tests
  - API key authentication
  - Multi-language support (EN/TR/DE/FR)

## Contributing
Contributions are not open yet — the project is in early development. 