"""
Advanced rule-based matching engine.
- Skills matching ab synonym-aware hai (skills_data.py ke SKILL_ALIASES use karke)
- Experience bhi consider hoti hai
- Final score = weighted combination: 70% skills + 30% experience

Asli AI/semantic matching (BERT/Sentence-Transformers, jo synonyms se aage jaake
"meaning" samajhta hai) Part 7-8 (ML Model) mein banega. Ye abhi turant kaam karne
wala "smart rule-based" version hai.
"""
from app.services.skills_data import normalize_skill

SKILL_WEIGHT = 0.7
EXPERIENCE_WEIGHT = 0.3


def calculate_skill_match(resume_skills: list[str], job_required_skills: str) -> float:
    """
    resume_skills: parser se already-canonical skills ki list (jaise ["python", "javascript"])
    job_required_skills: job ke required_skills field ki comma-separated string,
                          jismein user kuch bhi likh sakta hai jaise "JS, ML, Python"

    Dono taraf skills ko normalize karke (synonyms handle karke) compare karta hai.
    """
    if not job_required_skills or not job_required_skills.strip():
        return 0.0

    required_raw = [s.strip() for s in job_required_skills.split(",") if s.strip()]
    required_normalized = [normalize_skill(s) for s in required_raw]
    if not required_normalized:
        return 0.0

    resume_skills_normalized = set(normalize_skill(s) for s in resume_skills)

    matched = [s for s in required_normalized if s in resume_skills_normalized]
    score = (len(matched) / len(required_normalized)) * 100
    return round(score, 2)


def calculate_experience_match(candidate_years: float | None, required_years: float | None) -> float:
    """
    Candidate ke experience ko job ki minimum requirement se compare karta hai.
    - Agar job ko koi minimum experience nahi chahiye (0 ya None), toh full marks (100).
    - Agar candidate ka experience resume se nikal hi nahi paya, toh 50 (neutral score,
      taaki bina experience-mention wale achhe candidates bhi bahut neeche na chale jayein).
    - Agar candidate ka experience requirement se zyada/barabar hai, toh 100.
    - Warna proportional score (jitna kam experience, utna kam score).
    """
    if not required_years or required_years <= 0:
        return 100.0

    if candidate_years is None:
        return 50.0

    if candidate_years >= required_years:
        return 100.0

    return round((candidate_years / required_years) * 100, 2)


def calculate_final_score(skill_score: float, experience_score: float) -> float:
    """Weighted combination: skills ko zyada importance (70%), experience ko kam (30%)."""
    final = (skill_score * SKILL_WEIGHT) + (experience_score * EXPERIENCE_WEIGHT)
    return round(final, 2)


def get_matched_and_missing_skills(resume_skills: list[str], job_required_skills: str) -> dict:
    """Batata hai kaunsi required skills match hui aur kaunsi missing hain (synonym-aware)."""
    if not job_required_skills or not job_required_skills.strip():
        return {"matched": [], "missing": []}

    required_raw = [s.strip() for s in job_required_skills.split(",") if s.strip()]
    required_normalized = [normalize_skill(s) for s in required_raw]
    resume_skills_normalized = set(normalize_skill(s) for s in resume_skills)

    matched = [s for s in required_normalized if s in resume_skills_normalized]
    missing = [s for s in required_normalized if s not in resume_skills_normalized]

    return {"matched": matched, "missing": missing}
