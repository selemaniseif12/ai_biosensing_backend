# app/routers/analyzer_v1.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.crud import analyzer_v1 as crud_analyzer

router = APIRouter(tags=["Analyzer v1"])
logger = logging.getLogger("analyzers")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", summary="Analyze V1")
def analyze_v1(data: dict, db: Session = Depends(get_db)):
    logger.info(f"[Analyzer v1] analyze_v1 called with data={data}")

    try:
        result = crud_analyzer.run_analysis(db, data)
        logger.info(f"[Analyzer v1] Analysis completed: {result}")
        return result
    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in analyze_v1: {str(e)}")
        raise HTTPException(status_code=500, detail="Analyzer v1 failed")


@router.get("/devices", summary="Get All Devices")
def get_devices(db: Session = Depends(get_db)):
    logger.info("[Analyzer v1] get_devices called")

    try:
        return crud_analyzer.get_devices(db)
    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in get_devices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch devices")


@router.get("/devices/{device_id}", summary="Get Device")
def get_device(device_id: int, db: Session = Depends(get_db)):
    logger.info(f"[Analyzer v1] get_device called for device_id={device_id}")

    try:
        return crud_analyzer.get_device(db, device_id)
    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in get_device: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch device")


@router.get("/outputs", summary="Get All Outputs")
def get_outputs(db: Session = Depends(get_db)):
    logger.info("[Analyzer v1] get_outputs called")

    try:
        return crud_analyzer.get_outputs(db)
    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in get_outputs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch outputs")


@router.get("/outputs/{device_id}", summary="Get Output")
def get_output(device_id: int, db: Session = Depends(get_db)):
    logger.info(f"[Analyzer v1] get_output called for device_id={device_id}")

    try:
        return crud_analyzer.get_output(db, device_id)
    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in get_output: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch output")


@router.get("/device_full/{device_id}", summary="Get Full Device Data")
def get_full_device(device_id: int, db: Session = Depends(get_db)):
    logger.info(f"[Analyzer v1] get_full_device called for device_id={device_id}")

    try:
        return crud_analyzer.get_full_device(db, device_id)
    except Exception as e:
        logger.error(f"[Analyzer v1] ERROR in get_full_device: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch full device data")
