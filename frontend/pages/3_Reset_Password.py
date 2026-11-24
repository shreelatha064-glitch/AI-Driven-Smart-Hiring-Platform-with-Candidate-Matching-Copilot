
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import requests
from utils.api import API_URL

st.set_page_config(
    page_title="HireMatrix | Reset Password",
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

    .stButton > button {
        background-color: #1769aa;
        color: white;
        border-radius: 8px;
        border: none;
        height: 45px;
        font-weight: 600;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

left_column, right_column = st.columns([1, 1.1], gap="large")

with left_column:
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, #123b75, #1769aa);
        padding: 60px 40px;
        border-radius: 18px;
        color: white;
        min-height: 430px;
    ">
        <h1 style="font-size:42px;">HireMatrix</h1>
        <h2>Create a New Password</h2>
        <p style="font-size:18px;line-height:1.7;color:#e0edff;">
            Choose a new password to secure your account
            and continue using HireMatrix.
        </p>
        <br>
        <h3>✦ Secure Password Reset</h3>
        <h3>✦ Protected User Accounts</h3>
    </div>
    """, unsafe_allow_html=True)

with right_column:
    st.write("")
    st.write("")

    st.markdown(
        '<div class="reset-title">Reset Password</div>',
        unsafe_allow_html=True
    )

    st.write("Enter your reset token and choose a new password.")

    with st.form("reset_password_form"):
        token = st.text_area(
        "Password Reset Token",
        value=st.session_state.get("reset_token", ""),
        placeholder="Paste your reset token here"
)

        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Enter new password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            placeholder="Re-enter new password"
        )

        reset_button = st.form_submit_button(
            "Reset Password",
            use_container_width=True
        )

    if reset_button:
        if not token.strip() or not new_password or not confirm_password:
            st.warning("Please fill in all fields.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        elif len(new_password) < 8:
            st.error("Password must contain at least 8 characters.")

        else:
            try:
                response = requests.post(
                    f"{API_URL}/auth/reset-password",
                    json={
                        "token": token.strip(),
                        "new_password": new_password
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    st.success("Password reset successfully!")
                    st.info("You can now log in using your new password.")

                elif response.status_code == 400:
                    st.error("Your reset token is invalid or expired.")

                else:
                    st.error(f"Password reset failed: {response.text}")

            except requests.exceptions.RequestException:
                st.error("Unable to connect to the HireMatrix server.")

    st.write("")

    if st.button("Back to Login"):
        st.switch_page("app.py")

    st.caption("© 2026 HireMatrix | AI-Driven Smart Hiring Platform")
