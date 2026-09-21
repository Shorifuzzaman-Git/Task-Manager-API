from email.message import EmailMessage

import aiosmtplib

from app.core.config import settings


async def send_otp_email(
    recipient_email: str,
    otp_code: str
):
    message = EmailMessage()

    message["From"] = settings.MAIL_FROM
    message["To"] = recipient_email
    message["Subject"] = "Task Manager - Email Verification OTP"

    message.set_content(
        f"""
Hello,

Thank you for registering with Task Manager.

Your email verification OTP is:

{otp_code}

This OTP will expire in 5 minutes.

If you did not create this account, please ignore this email.

Regards,
Task Manager Team
"""
    )

    await aiosmtplib.send(
        message,
        hostname=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        start_tls=True,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD
    )