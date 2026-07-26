"""
Simple rule-based interview question generator (matches original plan feature:
'Generate interview questions'). Baad mein isko LLM-based bhi banaya ja sakta hai,
abhi ke liye skill-gap aur matched-skill based questions banate hain.
"""
from app.services.matching_service import get_matched_and_missing_skills


def generate_questions(resume_skills: list[str], job_required_skills: str, job_title: str) -> list[dict]:
    """
    Resume ki skills aur job ki required skills compare karke interview questions banata hai:
    - Missing skills ke liye 'skill-gap' questions (candidate se pucho unhone kya kiya hai us area mein)
    - Matched skills ke liye 'technical' questions (candidate se project detail pucho)
    - Kuch general 'behavioral' questions har candidate ke liye
    """
    gaps = get_matched_and_missing_skills(resume_skills, job_required_skills or "")
    questions = []

    for skill in gaps["missing"]:
        questions.append({
            "question": f"Is role ke liye {skill.title()} ka experience chahiye, lekin humein aapke resume mein "
                        f"ye nahi mila. Kya aapko {skill.title()} ka koi exposure ya learning experience hai?",
            "category": "skill-gap",
        })

    for skill in gaps["matched"][:3]:  # zyada se zyada 3 matched-skill questions, taaki list lambi na ho
        questions.append({
            "question": f"Kya aap {skill.title()} use karke banaye gaye kisi project ke baare mein bata sakte hain?",
            "category": "technical",
        })

    questions.append({
        "question": f"{job_title} role mein aapki interest kyun hai?",
        "category": "behavioral",
    })
    questions.append({
        "question": "Recent mein aapne koi challenging problem kaise solve kiya, ek example dijiye.",
        "category": "behavioral",
    })

    return questions
