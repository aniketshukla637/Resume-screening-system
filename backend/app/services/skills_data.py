"""
Skills master list — har skill ka ek 'canonical' (standard) naam hai, aur uske common
aliases/synonyms. Isse "JS" aur "JavaScript" dono ko same skill maana jayega,
"ML" aur "Machine Learning" dono same, wagera.

Ye file resume_parser.py (resume se skills nikaalne ke liye) aur matching_service.py
(job ki required_skills ko normalize karne ke liye) — dono use karte hain, taaki
matching hamesha consistent rahe.
"""

# canonical_name -> [aliases jo resume/job text mein mil sakte hain]
SKILL_ALIASES: dict[str, list[str]] = {
    "python": ["python", "py"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": ["c language", "c programming"],
    "javascript": ["javascript", "js", "es6", "ecmascript"],
    "sql": ["sql"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs", "node js"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi", "fast api"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "xgboost": ["xgboost"],
    "git": ["git", "github", "version control"],
    "docker": ["docker", "containerization"],
    "aws": ["aws", "amazon web services"],
    "excel": ["excel", "ms excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "streamlit": ["streamlit"],
    "rest api": ["rest api", "restful api", "rest apis"],
    "mongodb": ["mongodb", "mongo"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
}


def normalize_skill(raw_skill: str) -> str:
    """
    Kisi bhi skill text ko uske canonical naam mein convert karta hai.
    Agar match nahi mila (unknown skill), toh cleaned lowercase text hi wapas kar deta hai.
    Isse job ki required_skills field mein bhi "JS" likha ho, toh wo "javascript" ke
    barabar treat hoga.
    """
    cleaned = raw_skill.strip().lower()
    if not cleaned:
        return ""
    for canonical, aliases in SKILL_ALIASES.items():
        if cleaned == canonical or cleaned in aliases:
            return canonical
    return cleaned
