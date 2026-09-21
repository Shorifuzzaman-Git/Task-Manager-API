from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from datetime import timedelta

from app.core.config import settings

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.email_service import send_otp_email

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.schemas.otp import (
    OTPVerify,
    OTPRequest,
    OTPResponse
)

from app.services.otp_service import (
    create_otp,
    verify_otp,
    resend_otp
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    otp_code = create_otp(db, new_user)

    await send_otp_email(
        recipient_email=new_user.email,
        otp_code=otp_code
    )

    return new_user



@router.post(
    "/verify-otp",
    response_model=OTPResponse
)
def verify_email_otp(
    otp_data: OTPVerify,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == otp_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )

    is_valid = verify_otp(
        db=db,
        user=user,
        otp_code=otp_data.otp_code
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    return {
        "message": "Email verified successfully"
    }


@router.post(
    "/resend-otp",
    response_model=OTPResponse
)
async def resend_email_otp(
    otp_data: OTPRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == otp_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )

    # Generate new OTP and invalidate previous OTPs
    otp_code = resend_otp(
        db=db,
        user=user
    )

    # Send new OTP by email
    await send_otp_email(
        recipient_email=user.email,
        otp_code=otp_code
    )

    return {
        "message": "A new OTP has been sent to your email"
    }

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        },
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }