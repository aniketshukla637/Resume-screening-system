# 🤖 AI Resume Screening & Candidate Ranking System

An end-to-end system that automates resume screening for recruiters — upload resumes, automatically extract candidate details and skills, match them against a job description, and get a ranked, explainable shortlist of the best-fit candidates.

## 🎯 Problem It Solves

Recruiters spend a huge amount of time manually reading through resumes to shortlist candidates. This system automates that process: it parses resumes, scores each candidate against a job's requirements, and ranks them — so recruiters can focus on interviewing the best matches instead of screening everything by hand.

## ✨ Features

- 🔐 **Secure Authentication** — JWT-based signup/login for recruiters
- 📄 **Resume Parsing** — Upload PDF/DOCX resumes; automatically extracts candidate name, email, phone, and skills
- 🎯 **Job–Candidate Matching** — Rule-based, synonym-aware scoring engine (70% skill match + 30% experience match)
- 🏆 **Candidate Ranking** — Candidates are automatically ranked best-match-first for each job
- ✅❌ **Skill Gap Analysis** — See exactly which required skills a candidate has and which they're missing
- 🎤 **Interview Question Generator** — Auto-generates technical, skill-gap, and behavioral interview questions per candidate
- 🖥️ **Clean Web UI** — Card-based candidate view with star ratings and progress bars (Streamlit)
- 🗂️ **Domain Templates** — Quick-start job creation for common IT roles (Data Science, Backend, Frontend, DevOps, etc.)

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | Streamlit |
| Database | SQLite + SQLAlchemy ORM |
| Auth | JWT (python-jose / bcrypt) |
| Resume Parsing | pdfplumber, python-docx |
| Matching Engine | Custom rule-based NLP (synonym-aware skill matching) |

> **Planned:** Upgrading the matching engine with ML (XGBoost/Random Forest) and semantic similarity (BERT / Sentence-Transformers) for smarter, meaning-aware candidate–job matching.

## 📂 Project Structure

```
resume-screening-system/
├── backend/
│   └── app/
│       ├── core/         # config, security, JWT auth dependencies
│       ├── db/           # database connection setup
│       ├── models/       # SQLAlchemy ORM models
│       ├── routers/      # API endpoints (auth, jobs, resumes)
│       ├── schemas/      # Pydantic request/response schemas
│       ├── services/     # resume parsing, matching engine, file handling
│       └── main.py       # FastAPI app entry point
├── frontend/
│   ├── Home.py           # Login / Signup page
│   └── pages/
│       ├── 1_Upload_Resume.py     # Job creation + resume upload
│       └── 2_View_Candidates.py   # Ranked candidate cards + interview Qs
├── data/
│   ├── uploads/           # uploaded resumes (gitignored)
│   └── sample_resumes/    # sample resumes for testing
├── ml/                    # future ML model training + saved models
└── docs/
    └── ARCHITECTURE.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ai-resume-screening-system.git
cd ai-resume-screening-system/resume-screening-system
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at `http://127.0.0.1:8000` — API docs available at `http://127.0.0.1:8000/docs`

### 3. Set up the frontend
Open a new terminal:
```bash
cd frontend
pip install -r requirements.txt
streamlit run Home.py
```
Frontend opens automatically in your browser.

## 📸 How It Works

1. **Sign up / Log in** as a recruiter
2. **Create a job** — either pick a domain template (Data Science, Backend, Frontend, etc.) or enter details manually
3. **Upload resumes** (PDF/DOCX) against that job — the system extracts candidate details automatically
4. **View ranked candidates** — sorted by match score, with matched/missing skills clearly shown
5. **Generate interview questions** for any candidate based on their skill gaps

## 🗺️ Roadmap

- [x] Authentication (JWT)
- [x] Resume parsing (PDF/DOCX)
- [x] Rule-based job matching & ranking
- [x] Interview question generation
- [x] Card-based candidate UI
- [ ] ML-based suitability prediction (XGBoost/Random Forest)
- [ ] Semantic matching with BERT / Sentence-Transformers
- [ ] Deployment (Render + Streamlit Community Cloud)

## 👤 Author

Aniket Shukla — Final-year B.Tech CSE (AI) student, Babu Banarasi Das University, Lucknow

## 📄 License

This project is open source and available for educational use.
