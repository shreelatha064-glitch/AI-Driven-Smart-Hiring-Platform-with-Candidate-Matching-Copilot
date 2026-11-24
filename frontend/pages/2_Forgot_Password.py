
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.api import forgot_password

st.set_page_config(
    page_title="HireMatrix | Forgot Password",
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

    .reset-title {
        color: #173b70;
        font-size: 34px;
        font-weight: 750;
    }

    .reset-subtitle {
        color: #64748b;
        font-size: 16px;
        line-height: 1.6;
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
        min-height: 430px;
    ">
        <h1 style="font-size:42px;">HireMatrix</h1>

        <h2>Account Recovery</h2>

        <p style="
            font-size:18px;
            line-height:1.7;
            color:#e0edff;
        ">
            Don't worry! You can request a password reset
            and regain access to your HireMatrix account.
        </p>

        <br>

        <h3>✦ Secure Account Recovery</h3>
        <h3>✦ Simple Reset Process</h3>
    </div>
    """)


with right_column:
    st.write("")
    st.write("")

    st.markdown(
        '<div class="reset-title">Forgot Password?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="reset-subtitle">'
        'Enter your registered email address to request '
        'a password reset.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    with st.form("forgot_password_form"):
        email = st.text_input(
            "Email Address",
            placeholder="Enter your registered email"
        )

        submit_button = st.form_submit_button(
            "Request Password Reset",
            use_container_width=True
        )

    if submit_button:
        if not email.strip():
            st.warning("Please enter your email address.")

        else:
            response = forgot_password(email.strip())

            if response is None:
                st.error(
                    "Unable to connect to the HireMatrix server."
                )

            elif response.status_code == 200:
                data = response.json()

                st.success(data["message"])

                # Development prototype only:
                # Display the token for testing.
                if "reset_token" in data:
                    st.session_state["reset_token"] = data["reset_token"]
                    st.session_state["reset_token_ready"] = True

                    st.warning(
                    "Development mode: Your reset token "
                    "is displayed below. Keep it private."
            )

                    st.code(data["reset_token"])

                    st.caption(
                    "This token expires in 15 minutes."
           )

            else:
                st.error(
                    f"Password reset request failed: {response.text}"
                )

    st.write("")
    if st.session_state.get("reset_token_ready", False):

     if st.button("Continue to Reset Password"):
        st.switch_page("pages/3_Reset_Password.py")
    if st.button("Back to Login"):
        st.switch_page("app.py")

    st.caption("© 2026 HireMatrix | AI-Driven Smart Hiring Platform")
