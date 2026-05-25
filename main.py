from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.camp_model import Camp
from app.routes.camp_routes import router as camp_router
from app.models.donation_model import Donation
from app.routes.donation_routes import router as donation_router
from app.routes.chat_routes import router as chat_router
from app.routes.admin_user_routes import router as admin_user_router

from app.database import engine, Base

from app.models.user_model import User
from app.models.request_model import BloodRequest
from app.models.inventory_model import BloodInventory
from app.models.audit_model import AuditLog
from app.models.notification_model import Notification

from app.routes.user_routes import router as user_router
from app.routes.request_routes import router as request_router
from app.routes.inventory_routes import router as inventory_router
from app.routes.audit_routes import router as audit_router
from app.routes.notification_routes import router as notification_router
from app.routes.otp_routes import router as otp_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ROUTES
app.include_router(user_router)
app.include_router(request_router)
app.include_router(inventory_router)
app.include_router(audit_router)
app.include_router(notification_router)
app.include_router(otp_router)
app.include_router(camp_router)
app.include_router(donation_router)
app.include_router(chat_router)
app.include_router(admin_user_router)
@app.get("/")
def home():
    return {"message": "BDMS Backend Running"}