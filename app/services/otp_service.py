import secrets
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.otp import OTP
from app.models.user import User


def generate_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)


def invalidate_previous_otps(
    db: Session,
    user_id: int
):
    (
        db.query(OTP)
        .filter(
            OTP.user_id == user_id,
            OTP.is_used == False
        )
        .update(
            {
                OTP.is_used: True
            },
            synchronize_session=False
        )
    )

    db.commit()


def create_otp(
    db: Session,
    user: User
) -> str:

    otp_code = generate_otp()

    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp = OTP(
        user_id=user.id,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used=False
    )

    db.add(otp)
    db.commit()

    return otp_code


def resend_otp(
    db: Session,
    user: User
) -> str:

    # Invalidate all previous OTPs
    invalidate_previous_otps(
        db,
        user.id
    )

    # Generate new OTP
    otp_code = generate_otp()

    expires_at = datetime.utcnow() + timedelta(minutes=5)

    otp = OTP(
        user_id=user.id,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used=False
    )

    db.add(otp)
    db.commit()

    return otp_code


def verify_otp(
    db: Session,
    user: User,
    otp_code: str
) -> bool:

    otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user.id,
            OTP.otp_code == otp_code,
            OTP.is_used == False
        )
        .order_by(OTP.created_at.desc())
        .first()
    )

    if not otp:
        return False

    if datetime.utcnow() > otp.expires_at:
        return False

    otp.is_used = True
    user.is_verified = True

    db.commit()

    return True