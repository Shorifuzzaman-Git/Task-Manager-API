from pydantic import BaseModel, EmailStr, Field


class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str = Field(
        min_length=6,
        max_length=6
    )


class OTPRequest(BaseModel):
    email: EmailStr

class OTPResponse(BaseModel):
    message: str