
import streamlit as st
import sys
import textwrap
from pathlib import Path

# Make the frontend folder available for imports
sys.path.append(str(Path(__file__).parent))

from utils.api import login_user

# Page configuration
st.set_page_config(
    page_title="HireMatrix | Login",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fc;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .brand-section {
        background: linear-gradient(145deg, #123b75, #1769aa);
        padding: 65px 45px;
        border-radius: 18px;
        color: white;
        min-height: 540px;
    }

    .brand-section h1 {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 25px;
    }

    .brand-section h2 {
        font-size: 25px;
    }

    .brand-section p {
        font-size: 18px;
        line-height: 1.7;
        color: #e0edff;
    }

    .brand-section h3 {
        font-size: 19px;
    }

    .login-heading {
        color: #173b70;
        font-size: 34px;
        font-weight: 750;
    }

    .login-subtitle {
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


# Main page layout
left_column, right_column = st.columns([1.1, 1], gap="large")


# Left branding section

with left_column:
    st.html("""
    <div style="
        background: linear-gradient(145deg, #123b75, #1769aa);
        padding: 60px 40px;
        border-radius: 18px;
        color: white;
        min-height: 540px;
    ">
        <h1 style="font-size:42px;">HireMatrix</h1>

        <h2>Smarter Hiring. Better Matches.</h2>

        <p style="font-size:18px; line-height:1.7; color:#e0edff;">
            An AI-driven smart hiring platform that helps
            recruiters discover the right talent through
            intelligent candidate matching and profiling.
        </p>

        <br>

        <h3>✦ Intelligent Candidate Matching</h3>
        <h3>✦ AI-Powered Resume Analysis</h3>
        <h3>✦ Data-Driven Recruitment</h3>
    </div>
    """)


    


# Right login section
with right_column:
    st.write("")
    st.write("")

    st.markdown(
        '<div class="login-heading">Welcome Back!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Sign in to continue to your HireMatrix account.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if login_button:
        if not email or not password:
            st.warning("Please enter both email and password.")

        else:
            response = login_user(email, password)

            if response is None:
                st.error(
                    "Unable to connect to HireMatrix server. "
                    "Please check whether the backend is running."
                )

            elif response.status_code == 200:
                data = response.json()

                st.session_state["access_token"] = data["access_token"]
                st.session_state["user"] = data["user"]

                st.success(
                    f"Welcome, {data['user']['full_name']}!"
                )

                st.info(
                    f"Logged in as: {data['user']['role']}"
                )
                st.switch_page("pages/4_Resume_Upload.py")
            elif response.status_code == 401:
                st.error("Invalid email or password.")

            else:
                st.error(
                    f"Login failed: {response.text}"
                )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Forgot Password?"):
            st.switch_page("pages/2_Forgot_Password.py")

    with col2:
        if st.button("Create Account"):
            st.switch_page("pages/1_Register.py")

    st.write("")

    st.caption(
        "© 2026 HireMatrix | AI-Driven Smart Hiring Platform"
    )
