# app/models/__init__.py

from .activity import Activity
from .analysis import Analysis
from .analysis_log_model import AnalysisLog
from .analysis_result import AnalysisResult

# Removed ApiKey — class does not exist
# Removed Auth — class does not exist

from .cart_item import CartItem
from .consultation_schedule import ConsultationSchedule

# KEEP ONLY the real Consultation model
from .consultations import Consultation

# Removed Consulting — duplicate table definition
# Removed ConsultingRequestModel — not a DB model

from .course import Course
from .course_content import CourseContent
from .course_module import CourseModule
from .customer import Customer
from .detection import Detection
from .device import Device
from .document import Document
from .enrollment import Enrollment
from .measurement import Measurement
from .ml_log import MLLog
from .notification import Notification
from .payment_receipt import PaymentReceipt
from .receipt import Receipt
from .sample import Sample
from .service_model import Service

# ⭐ KEEP ONLY THIS — the real service_tokens table
from .service_token_model import ServiceToken

# ❌ REMOVE token_model — duplicate table definition

from .store_product import StoreProduct
from .students import Student
from .subscription import Subscription
from .team_model import Team
from .token_model import TokenModel   # <-- This is NOT the service_tokens table; safe to keep
from .usage_log import UsageLog
from .user import User
from .virus import Virus
