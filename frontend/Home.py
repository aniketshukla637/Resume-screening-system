import streamlit as st
import requests

# ---------- CONFIG ----------
# Backend FastAPI server ka base URL - agar backend kisi aur port/host pe hai toh yahan badlo
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Resume Screening System", page_icon="📄", layout="centered")

# ---------- SESSION STATE SETUP ----------
# session_state Streamlit ka tarika hai data ko yaad rakhne ka jab tak browser tab khula hai
# (warna har button click pe page reload hoke sab data reset ho jaata)
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None


def is_logged_in() -> bool:
    return st.session_state.access_token is not None


# ---------- HEADER ----------
st.title("📄 AI Resume Screening System")
st.caption("Upload resumes, analyze candidate-job compatibility, and rank the best matches.")
# ---------- AGAR LOGIN HAI TOH WELCOME SCREEN DIKHAO ----------
if is_logged_in():
    st.success(f"Logged in as **{st.session_state.user_name}** ({st.session_state.user_email})")
    st.write("Use the left sidebar to access the 'Upload Resume' and 'View Candidates' pages.")

    if st.button("Logout"):
        # Sab session data clear kar do - wapas logged-out state mein aa jayega
        st.session_state.access_token = None
        st.session_state.user_name = None
        st.session_state.user_email = None
        st.rerun()          # Page ko refresh kar do taaki login form wapas dikhe

# ---------- AGAR LOGIN NAHI HAI TOH LOGIN/SIGNUP TABS DIKHAO ----------
else:
    tab_login, tab_signup = st.tabs(["🔑 Login", "🆕 Sign Up"])

    # ===== LOGIN TAB =====
    with tab_login:
        st.subheader("Login to Your Account")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            if not login_email or not login_password:
                st.warning("Please enter both email and password to continue.")
            else:
                try:
                    # OAuth2 login form-data format expect karta hai, JSON nahi
                    response = requests.post(
                        f"{API_BASE_URL}/auth/login",
                        data={"username": login_email, "password": login_password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.access_token = data["access_token"]

                        # Login ke baad /auth/me call karke user ka naam/email nikal lo
                        me_response = requests.get(
                            f"{API_BASE_URL}/auth/me",
                            headers={"Authorization": f"Bearer {data['access_token']}"}
                        )
                        if me_response.status_code == 200:
                            me_data = me_response.json()
                            st.session_state.user_name = me_data.get("full_name", "User")
                            st.session_state.user_email = me_data.get("email", login_email)

                        st.rerun()          # Page refresh - ab welcome screen dikhega
                    else:
                        st.error("Login failed. Please check your email and password and try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the backend server. Please make sure the FastAPI server is running.")
    # ===== SIGNUP TAB =====
    with tab_signup:
        st.subheader("make new account")
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up", key="signup_btn"):
            if not signup_name or not signup_email or not signup_password:
                st.warning("Please fill in all required fields.")
            else:
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/auth/signup",
                        json={
                            "full_name": signup_name,
                            "email": signup_email,
                            "password": signup_password
                        }
                    )
                    if response.status_code in (200, 201):
                        st.success("Account created successfully! Please go to the 'Login' tab to continue.")
                    else:
                        st.error(f"Signup failed. {response.json().get('detail', 'Please try again later.')}")
                except requests.exceptions.ConnectionError:
                   st.error("Failed to connect to the backend server. Please ensure the backend is running using: 'uvicorn app.main:app --reload'.")