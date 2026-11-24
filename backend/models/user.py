
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    # Unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)

    # User's personal information
    full_name = Column(String(100), nullable=False)

    # Email must be unique
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Store the hashed password, never the original password
    hashed_password = Column(String(255), nullable=False)

    # User role: candidate, recruiter, or hr_manager
    role = Column(String(30), nullable=False, default="candidate")

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)

    # Account creation timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
