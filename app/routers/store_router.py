from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Store"])

PRODUCTS = [
    {
        "id": "consulting_fixed",
        "name": "Fixed Consulting Package",
        "type": "service",
        "price": 199,
        "billing": "one_time",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "consulting_custom",
        "name": "Custom Consulting Package",
        "type": "service",
        "price": 499,
        "billing": "one_time",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "course_intro",
        "name": "Intro to Biosensing & Frequency Noise",
        "type": "course",
        "price": 59,
        "billing": "3_months",
        "active": False,
        "coming_soon": True
    },
    {
        "id": "course_ml_v2",
        "name": "ML V2 Training Course",
        "type": "course",
        "price": 79,
        "billing": "3_months",
        "active": False,
        "coming_soon": True
    },
    {
        "id": "course_ml_v6",
        "name": "ML V6 Training Course",
        "type": "course",
        "price": 99,
        "billing": "3_months",
        "active": False,
        "coming_soon": True
    },
    {
        "id": "course_fullstack_api",
        "name": "Full Stack API Engineering Course",
        "type": "course",
        "price": 799,
        "billing": "3_months",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "ml_v2",
        "name": "ML V2 Model Access",
        "type": "digital",
        "price": 49,
        "billing": "3_months",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "ml_v6",
        "name": "ML V6 Model Access",
        "type": "digital",
        "price": 69,
        "billing": "3_months",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "ml_bundle_v2_v6",
        "name": "ML V2/V6 Bundle",
        "type": "digital",
        "price": 99,
        "billing": "3_months",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "virus_list",
        "name": "Virus Database Subscription",
        "type": "digital",
        "price": 29,
        "billing": "3_months",
        "active": True,
        "coming_soon": False
    },
    {
        "id": "device_lowgrade",
        "name": "Low-Grade Patented Biosensing Device",
        "type": "physical",
        "price": 299,
        "billing": "one_time",
        "active": True,
        "coming_soon": False
    }
]


@router.get("/products")
def get_products():
    return PRODUCTS


@router.get("/product/{item_id}")
def get_product(item_id: str):
    for item in PRODUCTS:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
