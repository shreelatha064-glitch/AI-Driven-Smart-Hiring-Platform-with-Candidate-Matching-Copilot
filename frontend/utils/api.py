import requests

API_URL = "http://127.0.0.1:8000"


def login_user(email, password):
    """Send login details to the FastAPI backend."""

    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        return response

    except requests.exceptions.ConnectionError:
        return None

    except requests.exceptions.Timeout:
        return None


def register_user(full_name, email, password, role):
    """Send registration details to the FastAPI backend."""

    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "full_name": full_name,
                "email": email,
                "password": password,
                "role": role
            },
            timeout=10
        )

        return response

    except requests.exceptions.RequestException:
        return None


def forgot_password(email):
    """Request a password reset."""

    try:
        response = requests.post(
            f"{API_URL}/auth/forgot-password",
            json={
                "email": email
            },
            timeout=10
        )

        return response

    except requests.exceptions.RequestException:
        return None
    
def upload_resume(uploaded_file):
    try:
        response = requests.post(
            f"{API_URL}/resume/upload",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            },
            timeout=60
        )
        return response

    except requests.exceptions.RequestException:
        return None
