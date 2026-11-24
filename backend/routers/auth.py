
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.schemas.user import UserRegister, UserResponse, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from backend.services.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    # Check whether the email already exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create the new user
    new_user = User(
        full_name=user_data.full_name,
        email=str(user_data.email).lower(),
        hashed_password=hashed_password,
        role=user_data.role
    )

    # Save user in PostgreSQL
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
@router.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    # Find user by email
    normalized_email = str(user_data.email).lower()

    user = db.query(User).filter(
        User.email == normalized_email
    ).first()

    # Check whether user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check whether password is correct
    if not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check whether account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive"
        )

    # Generate JWT access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
    }
@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    normalized_email = str(request.email).lower()

    user = db.query(User).filter(
        User.email == normalized_email
    ).first()

    # Use a generic response to avoid revealing
    # whether an email is registered.
    if not user:
        return {
            "message": "If the account exists, a password reset request has been created."
        }

    reset_token = create_password_reset_token(user.id)

    # Development only: return the token for testing.
    return {
        "message": "Password reset token generated successfully",
        "reset_token": reset_token,
        "expires_in_minutes": 15
    }
@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    # Verify the password reset token
    user_id = verify_password_reset_token(request.token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token"
        )

    # Find the user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Hash the new password
    new_hashed_password = hash_password(
        request.new_password
    )

    # Update the password
    user.hashed_password = new_hashed_password

    db.commit()

    return {
        "message": "Password reset successfully. You can now log in with your new password."
    }