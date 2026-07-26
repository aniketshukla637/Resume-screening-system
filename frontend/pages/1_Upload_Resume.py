import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Upload Resume", page_icon="📤", layout="wide")

# ---------- LOGIN CHECK ----------
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.warning("Please log in first.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.access_token}"}

st.title("📤 Upload Your Resume")

# ==================================================================
# DOMAIN TEMPLATES - IT sector ke common roles, unki standard skills ke saath
# Ye sab pre-filled hain taaki tumhe manually skills type na karni padein
# ==================================================================
DOMAIN_TEMPLATES = {
    "Data Science": {
        "title": "Data Scientist",
        "description": "Data Science role requiring strong Python, ML, and statistical analysis skills to build predictive models and extract insights from data.",
        "skills": "python, machine learning, deep learning, nlp, pandas, numpy, tensorflow, pytorch, scikit-learn, sql, statistics",
        "min_exp": 0.0,
    },
    "Data Analytics": {
        "title": "Data Analyst",
        "description": "Data Analytics role focused on cleaning, visualizing, and interpreting data to support business decisions.",
        "skills": "python, sql, excel, power bi, tableau, pandas, statistics, data visualization, mysql",
        "min_exp": 0.0,
    },
    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "description": "ML Engineer role to design, train, and deploy machine learning models into production systems.",
        "skills": "python, machine learning, deep learning, tensorflow, pytorch, scikit-learn, docker, aws, mlops, sql",
        "min_exp": 1.0,
    },
    "Frontend Developer": {
        "title": "Frontend Developer",
        "description": "Frontend role building responsive, user-facing web interfaces.",
        "skills": "html, css, javascript, react, typescript, tailwind, git, rest api",
        "min_exp": 0.0,
    },
    "Backend Developer": {
        "title": "Backend Developer",
        "description": "Backend role building APIs, business logic, and database-driven services.",
        "skills": "python, java, node.js, django, flask, fastapi, sql, mongodb, rest api, git, docker",
        "min_exp": 0.0,
    },
    "Full Stack Developer": {
        "title": "Full Stack Developer",
        "description": "Full Stack role handling both frontend UI and backend services end-to-end.",
        "skills": "javascript, react, node.js, html, css, python, sql, mongodb, rest api, git, docker",
        "min_exp": 0.5,
    },
    "DevOps Engineer": {
        "title": "DevOps Engineer",
        "description": "DevOps role managing CI/CD pipelines, infrastructure automation, and cloud deployments.",
        "skills": "docker, kubernetes, aws, git, ci/cd, linux, terraform, jenkins, python, bash",
        "min_exp": 1.0,
    },
    "Cloud Engineer": {
        "title": "Cloud Engineer",
        "description": "Cloud Engineer role designing and managing scalable cloud infrastructure.",
        "skills": "aws, azure, gcp, docker, kubernetes, terraform, linux, python, networking",
        "min_exp": 1.0,
    },
    "Cybersecurity Analyst": {
        "title": "Cybersecurity Analyst",
        "description": "Security role focused on identifying vulnerabilities and protecting systems from threats.",
        "skills": "network security, penetration testing, siem, linux, python, firewalls, cryptography, incident response",
        "min_exp": 0.5,
    },
    "Mobile App Developer": {
        "title": "Mobile App Developer",
        "description": "Mobile role building native or cross-platform Android/iOS applications.",
        "skills": "java, kotlin, swift, flutter, react native, android, ios, git, rest api",
        "min_exp": 0.0,
    },
    "QA / Software Tester": {
        "title": "QA Engineer",
        "description": "Quality Assurance role for manual and automated testing of software applications.",
        "skills": "selenium, python, java, manual testing, automation testing, test cases, jira, api testing",
        "min_exp": 0.0,
    },
    "Business Analyst (IT)": {
        "title": "Business Analyst",
        "description": "IT Business Analyst role bridging business requirements and technical implementation.",
        "skills": "sql, excel, power bi, requirement gathering, agile, jira, communication, data analysis",
        "min_exp": 0.5,
    },
}

# ---------- SECTION 1: EXISTING JOBS DEKHO ----------
st.subheader("1️⃣ Existing Jobs")
try:
    jobs_response = requests.get(f"{API_BASE_URL}/jobs/", headers=headers)
    jobs = jobs_response.json() if jobs_response.status_code == 200 else []
except requests.exceptions.ConnectionError:
    st.error("Unable to connect to the backend server. Please make sure the backend service is running.")
    jobs = []

if jobs:
    job_options = {f"#{job['id']} — {job['title']}": job["id"] for job in jobs}
else:
    job_options = {}
    st.info("No job postings are available yet. Create a new job posting below.")
# ---------- SECTION 2: DOMAIN TEMPLATE SE JOB CREATE KARO ----------
with st.expander("➕ Create a New Job Posting", expanded=True):
    st.write("**🎯 Select a domain — the relevant skills will be populated automatically:**")
    selected_domain = st.selectbox(
    "Domain",
    ["-- Enter Details Manually --"] + list(DOMAIN_TEMPLATES.keys()),
    label_visibility="collapsed",
)

    if selected_domain != "-- Enter Details Manually --":
        tmpl = DOMAIN_TEMPLATES[selected_domain]
    else:
        tmpl = {"title": "", "description": "", "skills": "", "min_exp": 0.0}

    # Key mein domain naam daala hai taaki domain badalte hi fields fresh values ke saath refresh ho jaayein
    field_key = selected_domain.replace(" ", "_")

    new_title = st.text_input("Job Title", value=tmpl["title"], key=f"title_{field_key}")
    new_description = st.text_area("Job Description", value=tmpl["description"], key=f"desc_{field_key}")
    new_skills = st.text_input(
        "Required Skills (comma-separated, editable)",
        value=tmpl["skills"], key=f"skills_{field_key}"
    )
    new_exp = st.number_input(
        "Minimum Experience (years)", min_value=0.0, step=0.5,
        value=tmpl["min_exp"], key=f"exp_{field_key}"
    )

    if st.button("Create Job", type="primary"):
        if not new_title or not new_description:
            st.warning("Job title and description are required.")
        else:
            payload = {
                "title": new_title,
                "description": new_description,
                "required_skills": new_skills,
                "min_experience_years": new_exp,
            }
            create_response = requests.post(f"{API_BASE_URL}/jobs/", headers=headers, json=payload)
            if create_response.status_code in (200, 201):
                st.success("Job posting created successfully! Select it from the dropdown below to upload resumes.")
                st.rerun()
            else:
                st.error(f"Failed to create the job posting: {create_response.text}")

# ---------- SECTION 3: RESUME UPLOAD KARO ----------
st.subheader("2️⃣ Upload Resume")

if job_options:
    selected_job_label = st.selectbox("Select a Job Posting", options=list(job_options.keys()))
    selected_job_id = job_options[selected_job_label]

    uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

    if uploaded_file is not None:
        if st.button("Upload & Parse Resume"):
            with st.spinner("Parsing resume..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                upload_response = requests.post(
                    f"{API_BASE_URL}/upload-resume/{selected_job_id}",
                    headers=headers,
                    files=files
                )

            if upload_response.status_code == 201:
                result = upload_response.json()
                st.success("Resume uploaded and parsed successfully! ✅")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Candidate Name", result.get("candidate_name") or "Not Found")
                    st.metric("Email", result.get("candidate_email") or "Not Found")
                with col2:
                    st.metric("Phone", result.get("candidate_phone") or "Not Found")

                st.write("**Skills Detected:**")
                skills = result.get("skills", [])
                if skills:
                    st.write(" ".join([f"`{skill}`" for skill in skills]))
                else:
                    st.write("No matching skills found.")

                st.info("👉 Visit the 'View Candidates' page to review the match score and skill gap.")
            else:
                st.error(f"Failed to upload the resume: {upload_response.text}")
else:
    st.info("Please create a job posting first before uploading resumes.")
