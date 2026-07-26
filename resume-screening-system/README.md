# AI Resume Screening & Candidate Ranking System

An end-to-end system that automatically parses resumes, matches them against a job description, ranks candidates, predicts a suitability score, and generates interview questions — built to save recruiters hours of manual screening.

## Status
🚧 In progress — being built part by part.

- [x] Part 1: Project Planning (folder structure, tech stack, DB schema, architecture)
- [ ] Part 2: Backend Setup
- [ ] Part 3: Authentication
- [ ] Part 4: Resume Parser
- [ ] Part 5: OCR
- [ ] Part 6: NLP
- [ ] Part 7: Matching Engine
- [ ] Part 8: ML Model
- [ ] Part 9: Frontend
- [ ] Part 10: Dashboard
- [ ] Part 11: Deployment
- [ ] Part 12: Testing
- [ ] Part 13: Documentation

## Features (planned)
- Upload multiple resumes (PDF/DOCX)
- OCR for scanned/image resumes
- Compare resumes against a job description
- Rank candidates by suitability score
- Display extracted top skills
- Auto-generate interview questions

## Tech Stack
| Layer | Technology |
|---|---|
| Backend API | FastAPI |
| Frontend | Streamlit |
| Database | SQLite (dev), MySQL (prod) |
| OCR | Tesseract, pdf2image, OpenCV |
| NLP | spaCy, Sentence-Transformers, BERT/DistilBERT |
| ML | XGBoost, Random Forest, scikit-learn |
| Auth | JWT (python-jose), bcrypt |

## Folder Structure
```
resume-screening-system/
├── backend/
│   ├── app/
│   │   ├── routers/        # API route handlers
│   │   ├── models/         # SQLAlchemy DB models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # Business logic (parsing, matching, scoring)
│   │   ├── core/           # Config, security, settings
│   │   └── db/             # DB connection + schema.sql
│   └── requirements.txt
├── frontend/
│   └── pages/               # Streamlit multi-page app
├── ml/
│   ├── training/            # Model training scripts
│   ├── saved_models/        # Trained .pkl/.joblib files
│   └── notebooks/           # Experimentation notebooks
├── data/
│   ├── uploads/              # User-uploaded resumes (gitignored)
│   └── sample_resumes/       # Sample/test resumes
├── docs/                     # Architecture, design docs
├── .gitignore
└── README.md
```

## Setup (to be completed in Part 2)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Database
See [`backend/app/db/schema.sql`](backend/app/db/schema.sql) for the full schema (users, jobs, resumes, resume_skills, scores, interview_questions, feedback).

## Architecture
See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the system design and data flow diagram.
