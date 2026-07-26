import streamlit as st
import requests

API_BASE_URL = "https://resume-screening-system-8v3e.onrender.com"
st.set_page_config(page_title="View Candidates", page_icon="👥", layout="wide")

# ---------- LOGIN CHECK ----------
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.warning("Pehle 'Home' page pe jaake login karo.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
st.title("👥 Candidates Dekho")

# ---------- THODI SI CUSTOM CSS - CARDS ACHE DIKHEIN ISLIYE ----------
st.markdown("""
<style>
.candidate-card {
    background-color: #1a1c24;
    border: 1px solid #2d2f3a;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 18px;
}
.rank-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color: white;
    font-weight: 700;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 14px;
}
.skill-matched {
    display: inline-block;
    background-color: #14532d;
    color: #86efac;
    padding: 3px 10px;
    border-radius: 14px;
    font-size: 13px;
    margin: 3px 4px 3px 0;
}
.skill-missing {
    display: inline-block;
    background-color: #450a0a;
    color: #fca5a5;
    padding: 3px 10px;
    border-radius: 14px;
    font-size: 13px;
    margin: 3px 4px 3px 0;
}
.stars {
    color: #facc15;
    font-size: 20px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)


def score_to_stars(score: float) -> str:
    """Match score (0-100) ko 5-star rating mein convert karta hai.
    Har star = 20%. Half star bhi dikhate hain agar beech mein ho."""
    stars_out_of_5 = score / 20
    full_stars = int(stars_out_of_5)
    half_star = 1 if (stars_out_of_5 - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    return ("★" * full_stars) + ("⯨" * half_star) + ("☆" * empty_stars)


def normalize(text: str) -> str:
    return text.strip().lower()


# ---------- JOBS DROPDOWN ----------
try:
    jobs_response = requests.get(f"{API_BASE_URL}/jobs/", headers=headers)
    jobs = jobs_response.json() if jobs_response.status_code == 200 else []
except requests.exceptions.ConnectionError:
    st.error("Backend server se connect nahi ho paya. Check karo 'uvicorn app.main:app --reload' chal raha hai kya.")
    jobs = []

if not jobs:
    st.info("Abhi tak koi job nahi bani. Pehle 'Upload Resume' page se job banao.")
    st.stop()

job_options = {f"#{job['id']} — {job['title']}": job["id"] for job in jobs}
selected_job_label = st.selectbox("Job select karo", options=list(job_options.keys()))
selected_job_id = job_options[selected_job_label]

selected_job = next(j for j in jobs if j["id"] == selected_job_id)
required_skills_raw = selected_job.get("required_skills") or ""
required_skills_list = [normalize(s) for s in required_skills_raw.split(",") if s.strip()]

if required_skills_raw:
    st.caption(f"**Required Skills for this job:** {required_skills_raw}")

# ---------- CANDIDATES FETCH KARO ----------
candidates_response = requests.get(
    f"{API_BASE_URL}/candidates/{selected_job_id}",
    headers=headers,
    params={"page": 1, "page_size": 50}
)

if candidates_response.status_code != 200:
    st.error(f"Candidates load nahi ho paye: {candidates_response.text}")
    st.stop()

data = candidates_response.json()
results = data.get("results", [])

st.write(f"**Total candidates uploaded for this job: {data.get('total', 0)}**")
st.caption("Candidates best-match-first order mein dikh rahe hain. Match Score = 70% Skills + 30% Experience.")

if not results:
    st.info("Is job ke liye abhi tak koi resume upload nahi hui.")
    st.stop()

# ---------- HAR CANDIDATE KA CARD BANAO ----------
for r in results:
    match_score = r.get("match_score") or 0.0
    skill_score = r.get("skill_match_score") or 0.0
    exp_score = r.get("experience_match_score") or 0.0
    candidate_skills_raw = r.get("skills") or []
    candidate_skills_normalized = set(normalize(s) for s in candidate_skills_raw)

    # ---------- MATCHED VS MISSING SKILLS NIKALO ----------
    # Job ki required skills mein se, candidate ke paas kaunsi hain aur kaunsi nahi
    matched_skills = [s for s in required_skills_list if s in candidate_skills_normalized]
    missing_skills = [s for s in required_skills_list if s not in candidate_skills_normalized]

    with st.container():
        st.markdown('<div class="candidate-card">', unsafe_allow_html=True)

        col_left, col_right = st.columns([3, 1])

        with col_left:
            st.markdown(
                f'<span class="rank-badge">Rank #{r.get("rank")}</span>',
                unsafe_allow_html=True
            )
            st.markdown(f"### {r.get('candidate_name') or 'Not Found'}")
            st.write(f"📧 {r.get('candidate_email') or 'Not Found'}  |  📞 {r.get('candidate_phone') or 'Not Found'}")

        with col_right:
            st.markdown(f'<div class="stars">{score_to_stars(match_score)}</div>', unsafe_allow_html=True)
            st.markdown(f"### {match_score:.1f}% Match")

        st.progress(min(int(match_score), 100) / 100)

        col_a, col_b = st.columns(2)
        with col_a:
            st.caption(f"Skill Match: **{skill_score:.1f}%**")
        with col_b:
            st.caption(f"Experience Match: **{exp_score:.1f}%**")

        # ---------- MATCHED / MISSING SKILLS DIKHAO (agar job mein required skills set hain) ----------
        if required_skills_list:
            st.write("")
            if matched_skills:
                st.write("**✅ Matched Skills:**")
                st.markdown(
                    "".join([f'<span class="skill-matched">{s}</span>' for s in matched_skills]),
                    unsafe_allow_html=True
                )
            if missing_skills:
                st.write("**❌ Missing Skills:**")
                st.markdown(
                    "".join([f'<span class="skill-missing">{s}</span>' for s in missing_skills]),
                    unsafe_allow_html=True
                )

        # ---------- CANDIDATE KI SAARI SKILLS (collapsible, agar dekhni ho) ----------
        with st.expander("View All Extracted Skills"):
            if candidate_skills_raw:
                st.write(", ".join(s.title() for s in candidate_skills_raw))
            else:
                st.write("No skills found.")

        st.caption(f"Uploaded: {r.get('uploaded_at', '')[:19].replace('T', ' ')} · Experience: {r.get('total_experience_years') or '-'} yrs")

        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- INTERVIEW QUESTIONS SECTION ----------
st.subheader("🎤 Interview Question Generator")
st.caption("Select a candidate to automatically generate interview questions based on their skills and the job requirements.")
candidate_options = {
    f"#{r.get('rank')} — {r.get('candidate_name') or 'Unknown'} ({r.get('match_score', 0)}% match)": r["id"]
    for r in results
}
selected_candidate_label = st.selectbox(
    "Candidate select karo", options=list(candidate_options.keys()), key="candidate_select"
)
selected_resume_id = candidate_options[selected_candidate_label]

if st.button(" Generate Interview Questions"):
    with st.spinner("Generating questions..."):
        q_response = requests.get(
            f"{API_BASE_URL}/interview-questions/{selected_resume_id}", headers=headers
        )
    if q_response.status_code == 200:
        questions = q_response.json()
        category_labels = {
            "skill-gap": "🔴 Skill Gap (Missing Skill)",
            "technical": "🟢 Technical (Matched Skill)",
            "behavioral": "🔵 Behavioral",
        }
        for cat_key, cat_label in category_labels.items():
            cat_questions = [q["question"] for q in questions if q["category"] == cat_key]
            if cat_questions:
                st.markdown(f"**{cat_label}**")
                for q in cat_questions:
                    st.write(f"- {q}")
    else:
        st.error(f"Failed to generate questions.: {q_response.text}")
