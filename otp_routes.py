import random
import os
import smtplib

from dotenv import load_dotenv

from email.message import EmailMessage

from fastapi import APIRouter, HTTPException

from pydantic import BaseModel, EmailStr

from app.auth import create_access_token

load_dotenv()

router = APIRouter()

# OTP STORE
otp_store = {}

# SMTP CONFIG
SMTP_EMAIL = os.getenv("SMTP_EMAIL")

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587


# =========================
# PYDANTIC SCHEMAS
# =========================

class SendOTPRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


# =========================
# SEND OTP
# =========================

@router.post("/send-otp")
async def send_otp(data: SendOTPRequest):

    email = data.email

    otp = str(random.randint(100000, 999999))

    otp_store[email] = otp

    try:

        message = EmailMessage()

        message["Subject"] = "Your OTP Code"

        message["From"] = SMTP_EMAIL

        message["To"] = email

        message.set_content(f"Your OTP is: {otp}")

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        server.send_message(message)

        server.quit()

        return {
            "message": "OTP sent successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# VERIFY OTP
# =========================

@router.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest):

    email = data.email

    otp = data.otp

    stored_otp = otp_store.get(email)

    if not stored_otp:

        raise HTTPException(
            status_code=400,
            detail="OTP expired or not found"
        )

    if stored_otp != otp:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    token = create_access_token({
        "sub": email
    })

    del otp_store[email]

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "user"
    }