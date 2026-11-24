
from fileinput import filename

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.resume_parser import extract_resume_text
from backend.services.candidate_extractor import extract_candidate_information
from sqlalchemy.orm import Session
from fastapi import Depends

from backend.database import get_db
from backend.models.candidate import Candidate
from backend.dependencies.auth import get_current_user
from backend.models.user import User

router = APIRouter(
    prefix="/resume",
    tags=["Resume Upload"]
)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    filename = file.filename or ""

    file_extension = (
        "." + filename.rsplit(".", 1)[-1].lower()
        if "." in filename else ""
    )

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        extracted_text = extract_resume_text(
            filename,
            file_content
        )
        # Clean unusual bullet characters extracted from PDF files
        extracted_text = extracted_text.replace("(cid:127)", "•")
        extracted_text = extracted_text.replace("(cid:149)", "•")

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read this resume. Please upload a valid PDF or DOCX file."
        )

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the resume."
        )

    candidate_information = extract_candidate_information(
    extracted_text
)
    # Create candidate profile
    
    new_candidate = Candidate(
    user_id=current_user.id,

    # Personal information
    full_name=(
        candidate_information.get("full_name")
        or current_user.full_name
    ),
    email=(
        candidate_information.get("email")
        or current_user.email
    ),

    # Extracted resume information
    summary=candidate_information.get("summary"),
    education=candidate_information.get("education"),
    skills=candidate_information.get("skills"),
    projects=candidate_information.get("projects"),
    experience=candidate_information.get("experience"),
    certifications=candidate_information.get("certifications"),
    activities=candidate_information.get("activities"),

    # Resume file information
    resume_filename=filename
)


    # Save candidate profile in PostgreSQL
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    return {
        "message": "Resume uploaded and candidate information extracted successfully!",
        "candidate_id": new_candidate.id,
        "filename": filename,
        "file_type": file_extension,
        "file_size": len(file_content),
        "candidate_information": candidate_information,
        "extracted_text": extracted_text
    }
