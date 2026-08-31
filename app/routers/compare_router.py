from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils.token_utils import is_token_active   # ⭐ FIXED IMPORT
from app.routers.classify_router import run_v2_model
from app.routers.ml_multiclassify_router import run_v6_model

router = APIRouter(
    prefix="/classify",
    tags=["Compare Models"]
)

# ---------------------------------------------------------
# REQUIRE V6 TOKEN (RESTORED)
# ---------------------------------------------------------
def require_v6_token(token: str, db: Session = Depends(get_db)):
    """
    Only V6 tokens can access the compare endpoint.
    """
    if is_token_active(db, token, "v6"):
        return True
    raise HTTPException(status_code=403, detail="V6 token required")


# ---------------------------------------------------------
# COMPARE V2 vs V6 MODELS
# ---------------------------------------------------------
@router.post("/compare")
def compare_v2_v6(
    payload: dict,
    _ = Depends(require_v6_token),   # ⭐ FIXED — now works
    db: Session = Depends(get_db)
):
    features = payload.get("features")
    threshold_hz = payload.get("threshold_hz", 0.1)

    if not features:
        raise HTTPException(status_code=400, detail="Missing 'features' in payload")

    v2_result = run_v2_model(features, threshold_hz)
    v6_result = run_v6_model(features, threshold_hz)

    return {
        "v2": v2_result,
        "v6": v6_result
    }
