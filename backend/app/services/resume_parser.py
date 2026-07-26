import re
import pdfplumber
import docx
from app.services.skills_data import SKILL_ALIASES


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text(file_path: str, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif filename.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Sirf .pdf aur .docx files supported hain")


def extract_email(text: str) -> str:
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    match = re.search(r'(\+91[\-\s]?)?[6-9]\d{9}', text)
    return match.group(0) if match else ""


def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        if len(first_line.split()) <= 5:
            return first_line
    return "Not Found"


def extract_skills(text: str) -> list:
    """
    NAYA: Ab sirf exact naam nahi, balki aliases/synonyms bhi dhoondta hai
    (jaise 'JS' -> 'javascript', 'ML' -> 'machine learning'), aur word-boundary
    ke saath match karta hai taaki galat partial-match na ho (jaise 'c' kahi
    bhi na match ho jaye).
    Result mein hamesha canonical (standard) naam store hota hai.
    """
    text_lower = text.lower()
    found_skills = []
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(canonical)
                break  # ek canonical skill ek hi baar list mein aaye
    return found_skills


def extract_experience_years(text: str) -> float | None:
    """
    NAYA: Resume text se total years of experience nikaalne ki koshish karta hai.
    Patterns jaise "3 years of experience", "5+ years experience", "experience: 2 years"
    ko dhoondta hai. Agar kuch matches milte hain, sabse bada number leta hai
    (usually total/overall experience hoti hai).
    Agar kuch nahi mila, None return karta hai (frontend mein '-' dikhega).
    """
    text_lower = text.lower()

    patterns = [
        r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
        r'experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)',
        r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work\s*)?exp\b',
    ]

    found_numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        found_numbers.extend(float(m) for m in matches)

    if found_numbers:
        return max(found_numbers)
    return None


def parse_resume(file_path: str, filename: str) -> dict:
    raw_text = extract_text(file_path, filename)
    return {
        "raw_text": raw_text,
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "skills": extract_skills(raw_text),
        "experience_years": extract_experience_years(raw_text),
    }
