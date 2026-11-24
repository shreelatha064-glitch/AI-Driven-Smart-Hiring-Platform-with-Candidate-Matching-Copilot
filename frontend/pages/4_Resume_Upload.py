
import streamlit as st
import requests
import sys
import re
from pathlib import Path

# Allow importing utilities from the frontend folder
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.api import API_URL


# -------------------------------
# Page configuration
# -------------------------------

st.set_page_config(
    page_title="HireMatrix - Candidate Profiling",
    page_icon="📄",
    layout="wide"
)


# -------------------------------
# Custom styling
# -------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fc;
}

.main-title {
    color: #173b70;
    font-size: 34px;
    font-weight: 700;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

.profile-heading {
    color: #173b70;
    font-size: 21px;
    font-weight: 700;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# Header
# -------------------------------

st.markdown(
    '<div class="main-title">HireMatrix</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Driven Smart Hiring Platform</div>',
    unsafe_allow_html=True
)

st.divider()

st.title("Resume Upload & Candidate Profiling")

st.write(
    "Upload a candidate resume in PDF or DOCX format. "
    "HireMatrix will extract information and generate a structured candidate profile."
)


# -------------------------------
# Resume upload
# -------------------------------

uploaded_file = st.file_uploader(
    "Choose a resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)


if uploaded_file is not None:

    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("Upload and Generate Candidate Profile"):

        access_token = st.session_state.get("access_token")

        if not access_token:
            st.error(
                "Your session has expired. Please log in again."
            )
            st.stop()

        with st.spinner(
            "Uploading resume and generating candidate profile..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/resume/upload",

                    headers={
                        "Authorization": f"Bearer {access_token}"
                    },

                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    },

                    timeout=60
                )

                # -------------------------------
                # Successful upload
                # -------------------------------

                if response.status_code == 200:

                    data = response.json()

                    candidate = data.get(
                        "candidate_information", {}
                    )

                    st.success(data.get(
                        "message",
                        "Resume processed successfully!"
                    ))

                    # -------------------------------
                    # Profile fields
                    # -------------------------------

                    profile_fields = {
                        "Full Name": candidate.get("full_name"),
                        "Email": candidate.get("email"),
                        "Professional Summary": candidate.get("summary"),
                        "Education": candidate.get("education"),
                        "Skills": candidate.get("skills"),
                        "Projects": candidate.get("projects"),
                        "Work Experience": candidate.get("experience"),
                        "Certifications": candidate.get("certifications"),
                        "Leadership & Activities": candidate.get("activities")
                    }

                    total_fields = len(profile_fields)

                    extracted_fields = sum(
                        1 for value in profile_fields.values()
                        if value and str(value).strip()
                    )

                    completeness = (
                        extracted_fields / total_fields
                        if total_fields else 0
                    )

                    missing_fields = [
                        field
                        for field, value in profile_fields.items()
                        if not value or not str(value).strip()
                    ]

                    # -------------------------------
                    # Candidate profile header
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Candidate Profile</div>',
                        unsafe_allow_html=True
                    )

                    full_name = (
                        candidate.get("full_name")
                        or "Name not detected"
                    )

                    email = (
                        candidate.get("email")
                        or "Email not detected"
                    )

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.subheader(full_name)
                        st.write(f"✉️ {email}")

                    with col2:
                        st.metric(
                            "Candidate ID",
                            data.get("candidate_id", "N/A")
                        )

                    st.caption(
                        f"Resume: {data.get('filename', uploaded_file.name)}"
                    )

                    # -------------------------------
                    # Parsing completeness
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Resume Parsing Completeness</div>',
                        unsafe_allow_html=True
                    )

                    metric_col1, metric_col2 = st.columns(2)

                    with metric_col1:
                        st.metric(
                            "Fields populated",
                            f"{extracted_fields}/{total_fields}"
                        )

                    with metric_col2:
                        st.metric(
                            "Fields requiring review",
                            len(missing_fields)
                        )

                    st.progress(
                        completeness,
                        text=f"{completeness * 100:.1f}% field completeness"
                    )

                    st.caption(
                        "This measures the proportion of expected fields "
                        "that contain extracted information. It is not a "
                        "verified parsing-accuracy score."
                    )

                    if missing_fields:
                        st.warning(
                            "Some information was not detected: "
                            + ", ".join(missing_fields)
                        )
                    else:
                        st.success(
                            "All expected profile fields contain information."
                        )

                    # -------------------------------
                    # Personal information
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Personal Information</div>',
                        unsafe_allow_html=True
                    )

                    personal_col1, personal_col2 = st.columns(2)

                    with personal_col1:
                        st.write("**Full Name**")
                        st.write(full_name)

                    with personal_col2:
                        st.write("**Email Address**")
                        st.write(email)

                    # -------------------------------
                    # Professional summary
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Professional Summary</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        candidate.get("summary")
                        or "No professional summary detected."
                    )

                    # -------------------------------
                    # Education
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Education</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        candidate.get("education")
                        or "No education information detected."
                    )

                    # -------------------------------
                    # Skills
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Technical Skills</div>',
                        unsafe_allow_html=True
                    )

                    skills = candidate.get("skills")

                    if skills:

                        skill_items = [
                            item.strip(" •▪●◦\t")
                            for item in re.split(r"[,;\n•]", skills)
                            if item.strip(" •▪●◦\t")
                        ]

                        if skill_items:
                            st.write("  |  ".join(
                                f"**{skill}**"
                                for skill in skill_items
                            ))
                        else:
                            st.write(skills)

                    else:
                        st.info("No skills detected.")

                    # -------------------------------
                    # Projects
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Projects</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        candidate.get("projects")
                        or "No project information detected."
                    )

                    # -------------------------------
                    # Work experience
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Work Experience</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        candidate.get("experience")
                        or "No work experience detected."
                    )

                    # -------------------------------
                    # Certifications
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Certifications</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        candidate.get("certifications")
                        or "No certifications detected."
                    )

                    # -------------------------------
                    # Leadership and activities
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Leadership & Activities</div>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        candidate.get("activities")
                        or "No leadership or extracurricular information detected."
                    )

                    # -------------------------------
                    # Resume details
                    # -------------------------------

                    st.divider()

                    st.markdown(
                        '<div class="profile-heading">Resume Details</div>',
                        unsafe_allow_html=True
                    )

                    detail_col1, detail_col2, detail_col3 = st.columns(3)

                    with detail_col1:
                        st.write("**Filename**")
                        st.write(data.get("filename", "N/A"))

                    with detail_col2:
                        st.write("**File Type**")
                        st.write(data.get("file_type", "N/A"))

                    with detail_col3:
                        st.write("**File Size**")
                        st.write(
                            f'{data.get("file_size", 0):,} bytes'
                        )

                    # -------------------------------
                    # Complete extracted text
                    # -------------------------------

                    with st.expander(
                        "View Complete Extracted Resume Text"
                    ):

                        st.text(
                            data.get("extracted_text", "")
                        )

                    st.divider()

                    st.success(
                        "Candidate profile generated successfully!"
                    )

                # -------------------------------
                # Upload errors
                # -------------------------------

                else:

                    st.error(
                        f"Upload failed ({response.status_code}): "
                        f"{response.text}"
                    )

                    if response.status_code == 401:
                        st.warning(
                            "Your login token may have expired. "
                            "Please log in again."
                        )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to HireMatrix backend. "
                    "Please make sure the FastAPI server is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Resume processing timed out. Please try again."
                )

            except Exception as e:

                st.error(
                    f"An unexpected error occurred: {e}"
                )


# -------------------------------
# Footer
# -------------------------------

st.divider()

st.caption(
    "HireMatrix | AI-Driven Smart Hiring Platform"
)
