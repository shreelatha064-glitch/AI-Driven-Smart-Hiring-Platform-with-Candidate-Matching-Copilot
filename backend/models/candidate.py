
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from backend.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Personal information
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)

    # Extracted resume information
    summary = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    projects = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    certifications = Column(Text, nullable=True)
    activities = Column(Text, nullable=True)

    # Original resume information
    resume_filename = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
