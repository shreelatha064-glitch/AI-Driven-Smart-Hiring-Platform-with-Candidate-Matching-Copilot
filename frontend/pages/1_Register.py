
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.api import register_user

st.set_page_config(
    page_title="HireMatrix | Register",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fc;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .register-title {
        color: #173b70;
        font-size: 34px;
        font-weight: 750;
    }

    .register-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .stButton > button {
        background-color: #1769aa;
        color: white;
        border-radius: 8px;
        border: none;
        height: 45px;
        font-weight: 600;
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #123b75;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

left_column, right_column = st.columns([1, 1.1], gap="large")


with left_column:
    st.html("""
    <div style="
        background: linear-gradient(145deg, #123b75, #1769aa);
        padding: 60px 40px;
        border-radius: 18px;
        color: white;
        min-height: 540px;
    ">
        <h1 style="font-size:42px;">Join HireMatrix</h1>

        <h2>Build Your Future With Smarter Hiring.</h2>

        <p style="
            font-size:18px;
            line-height:1.7;
            color:#e0edff;
        ">
            Create your account and experience intelligent
            recruitment powered by AI.
        </p>

        <br>

        <h3>✦ Smart Candidate Profiling</h3>
        <h3>✦ Intelligent Recruitment</h3>
        <h3>✦ Better Career Opportunities</h3>
    </div>
    """)


with right_column:
    st.write("")
    st.markdown(
        '<div class="register-title">Create Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="register-subtitle">'
        'Fill in your details to get started.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("register_form"):
        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        role = st.selectbox(
            "Select Your Role",
            ["candidate", "recruiter", "hr_manager"],
            format_func=lambda x: {
                "candidate": "Candidate",
                "recruiter": "Recruiter",
                "hr_manager": "HR Manager"
            }[x]
        )

        register_button = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if register_button:
        if not full_name.strip() or not email.strip() or not password:
            st.warning("Please fill in all required fields.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        elif len(password) < 8:
            st.error("Password must contain at least 8 characters.")

        else:
            response = register_user(
                full_name.strip(),
                email.strip(),
                password,
                role
            )

            if response is None:
                st.error(
                    "Unable to connect to the HireMatrix server."
                )

            elif response.status_code == 201:
                st.success("Account created successfully!")
                st.info(
                    "You can now return to the login page and sign in."
                )

            elif response.status_code == 409:
                st.error("An account with this email already exists.")

            elif response.status_code == 422:
                st.error(
                    "Please check your name, email and password details."
                )

            else:
                st.error(f"Registration failed: {response.text}")

    st.write("")

    if st.button("Back to Login"):
        st.switch_page("app.py")

    st.caption("© 2026 HireMatrix | AI-Driven Smart Hiring Platform")
