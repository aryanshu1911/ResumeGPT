# 🚀 ResumeGPT: AI-Powered Career Path Analyzer

A full-stack application that parses resumes, extracts key entities using NLP, and recommends career paths using semantic embeddings.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?logo=chartdotjs&logoColor=white)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Resume Parsing** | Upload PDF, DOCX, or TXT resumes |
| **Entity Extraction** | Detects Skills, Projects, Achievements, Extracurriculars |
| **Career Matching** | Semantic similarity using Sentence Transformers (all-MiniLM-L6-v2) |
| **Skill Gap Analysis** | Identifies missing skills for recommended career paths |
| **Interactive Charts** | Bar & Radar charts via Chart.js |
| **Premium UI** | Dark-mode glassmorphism design with animations |

---

## 📁 Folder Structure

```
ResumeGPT/
├── backend/
│   ├── app.py                              # FastAPI main (REST API)
│   ├── requirements.txt                    # Python dependencies
│   └── models/
│       ├── resume_parser.py                # PDF/DOCX/TXT parsing
│       ├── resume_ner_model/
│       │   └── extractor.py                # Entity extraction (spaCy + regex)
│       └── career_match_model/
│           └── matcher.py                  # Semantic career matching
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.js                          # Main React component
│       ├── App.css                         # Styling
│       └── components/
│           ├── ResumeUpload.js             # File upload (drag & drop)
│           ├── SkillList.js                # Skills display
│           ├── ProjectAnalysis.js          # Projects + achievements
│           └── CareerChart.js              # Career fit charts
├── data/
│   ├── career_roles.json                   # 10 predefined career roles
│   └── sample_resumes/
│       └── sample_resume.txt               # Sample resume for testing
└── README.md
```

---

## 🛠️ Quick Start

### Prerequisites
- **Python 3.9+** with pip
- **Node.js 16+** with npm

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app:app --reload --port 8000
```

> **Note:** The first request will download the Sentence Transformers model (~80 MB). Subsequent requests are fast.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The app opens at **http://localhost:3000**.

### 3. Test

Upload `data/sample_resumes/sample_resume.txt` through the UI, or test the API directly:

```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@data/sample_resumes/sample_resume.txt"
```

---

## 🔌 API Reference

### `POST /analyze`

Upload a resume file and get structured analysis.

**Request:** `multipart/form-data` with field `file` (PDF/DOCX/TXT)

**Response:**
**Response:**

A structured analysis object containing:

- **`filename`** *(string)*: Name of the uploaded resume.
- **`skills`** *(array of strings)*: Extracted key technical skills.
- **`projects`** *(array of objects)*: Detected projects including:
  - `name`: Project title.
  - `tech_stack`: Array of technologies used.
  - `domain`: Broad functional area (e.g., Computer Vision).
- **`achievements`** *(array of strings)*: Extracted distinct awards, ranks, or accomplishments.
- **`extracurriculars`** *(array of strings)*: Extracted leadership roles, volunteer work, or clubs.
- **`career_suggestions`** *(array of objects)*: Ranked list of recommended career paths containing:
  - `role`: Recommended job title.
  - `score`: Confidence percentage (e.g., 78.3).
  - `skill_gaps`: Array of missing skills required for this role.

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| NLP/ML | spaCy, Sentence Transformers, scikit-learn, NLTK |
| Resume Parsing | pdfminer.six, docx2txt |
| Frontend | React 18, Chart.js, Axios |

---

## 📄 License

This is an open-source project licensed under the MIT License.

---
