import os
print("RUNNING FROM:", os.path.abspath(__file__))

from dotenv import load_dotenv
load_dotenv()

import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.logging_config import LOGGING_CONFIG
from app.database import Base, engine, SessionLocal
from app.database import init_db

from app.seed.store_seed import seed_store_products

from app.models.students import Student
from app.models.team_model import Team
from app.models.consultations import Consultation
from app.models.course import Course
from app.models.course_module import CourseModule
from app.models.course_content import CourseContent
from app.models.enrollment import Enrollment
from app.models.activity import Activity

from app.models.store_product import StoreProduct
from app.models.cart_item import CartItem
from app.models.receipt import Receipt

from app.models.document import Document
from app.models.consulting_model import ConsultingRequestModel

from app.models.token_model import ServiceToken
from app.models.service_model import Service

from app.routers.home_router import router as home_router
from app.profile_router import router as profile_router

from app.routers import payments
from app.routers.stripe_router import router as stripe_router
from app.routers.cart_router import router as cart_router
from app.routers.payment_webhook import router as payment_webhook_router

# ⭐ ADDED — your real Stripe webhook
from app.routers.webhook import router as stripe_webhook_router

from app.routers.auth import router as auth_router
from app.routers.course_router import router as course_router
from app.routers.course_module_router import router as course_module_router
from app.routers.course_content_router import router as course_content_router
from app.routers.course_access_router import router as course_access_router

from app.routers.enrollment import router as enrollment_router
from app.routers.activity import router as activity_router

from app.routers.consultations import router as consultations_router
from app.routers.consulting_router import router as consulting_router
from app.routers.students import router as students_router
from app.routers.consultation_schedule_router import router as consultation_schedule_router
from app.routers.notification_router import router as notification_router
from app.routers.team_workload_router import router as team_workload_router
from app.routers.calendar_router import router as calendar_router

from app.routers.token_admin import router as token_admin_router

from app.routers.classify_router import router as classify_router
from app.routers.ml_multiclassify_router import router as ml_multiclassify_router
from app.routers.multiclass_dashboard_v6 import router as dashboard_v6_router
from app.routers.virus_multiclass_router import router as virus_multiclass_router
from app.routers.compare_router import router as compare_router

from app.routers.ml_training import router as ml_training_router
from app.routers.versioning_router import router as versioning_router
from app.routers.sensor_live_drift import router as live_router
from app.api.device_routes import router as device_router

from app.routers.virus_list import router as virus_list_router
from app.routers.virus_post import router as virus_post_router
from app.routers.virus_count import router as virus_count_router

from app.routers.store_router import router as store_router
from app.routers.cart_router import router as cart_router, alias_router as cart_alias_router

from app.routers.docs_router import router as docs_router
from app.routers.subscription_routes import router as subscription_router

from app.routers.tokens import router as tokens_router
from app.routers.services import router as services_router

from app.initial_data import run_initial_load

from app.routers.receipts_router import init_receipts
from app.routers.payments_router import router as payments_router


app = FastAPI(
    title="AI Biosensing API",
    version="1.0.0",
    description="Copyright © 2026 Piezo Pico to Femtotechnology Sensors Inc."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logging.config.dictConfig(LOGGING_CONFIG)
    init_db()
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    seed_store_products(db)
    run_initial_load(db)
    db.close()

os.makedirs("static/slides", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, tags=["Auth"])
app.include_router(home_router, tags=["Home"])
app.include_router(profile_router, tags=["Profile"])

app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(stripe_router, prefix="/store", tags=["Stripe"])

# ⭐ ADDED — mount your real Stripe webhook
app.include_router(stripe_webhook_router, tags=["Stripe Webhook"])

app.include_router(course_router, tags=["Course"])
app.include_router(course_module_router, tags=["Course Modules"])
app.include_router(course_content_router, tags=["Course Content"])
app.include_router(course_access_router)

app.include_router(enrollment_router, tags=["Enrollment"])
app.include_router(activity_router, tags=["Activity"])

app.include_router(consultations_router, tags=["Consultations"])
app.include_router(consulting_router)
app.include_router(students_router, tags=["Students"])
app.include_router(classify_router, tags=["ML Model V2"])
app.include_router(ml_multiclassify_router, tags=["ML Models V2 and V6"])
app.include_router(dashboard_v6_router)
app.include_router(compare_router)

app.include_router(virus_multiclass_router, prefix="/virus", tags=["Virus Multiclass"])

app.include_router(ml_training_router, tags=["ML Training"])
app.include_router(live_router, tags=["Sensor Drift"])
app.include_router(device_router, tags=["Device"])

app.include_router(virus_post_router, tags=["Virus"])
app.include_router(virus_count_router, tags=["Virus Count"])
app.include_router(virus_list_router, tags=["Virus List"])

app.include_router(store_router, prefix="/store", tags=["Store"])
app.include_router(cart_router)
app.include_router(cart_alias_router)

app.include_router(docs_router)
app.include_router(subscription_router)
app.include_router(payment_webhook_router)

app.include_router(tokens_router, tags=["Service Tokens"])
app.include_router(services_router, tags=["Subscribed Services"])
app.include_router(token_admin_router)
app.include_router(consultation_schedule_router)
app.include_router(notification_router)
app.include_router(team_workload_router)
app.include_router(calendar_router)

init_receipts(app)
app.include_router(payments_router)


from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailRequest(BaseModel):
    to: str
    subject: str
    message: str

@app.post("/send-email")
def send_email(req: EmailRequest):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = req.subject
    msg["From"] = "selemaniseif1974@gmail.com"
    msg["To"] = req.to

    html = f"""
    <html>
      <body>
        <h2>{req.subject}</h2>
        <p>{req.message}</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(req.message, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("selemaniseif1974@gmail.com", "fgzpiqpsftuzmtdm")
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())

        return {"status": "sent", "to": req.to}

    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/")
def root():
    return {"message": "AI Biosensing API is running"}
