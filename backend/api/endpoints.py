from fastapi import APIRouter, HTTPException
from typing import List
from database.models import ThreatEntry
from database.queries import get_recent_threats
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/threats", response_model=List[ThreatEntry])
async def get_threats(limit: int = 100):
    """Fetch recent threats from the database."""
    try:
        return await get_recent_threats(limit)
    except Exception as e:
        logger.error(f"Failed to fetch threats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/threats/{ip}")
async def get_threat_details(ip: str):
    """Fetch detailed analysis for a specific IP."""
    # Integrate with ThreatAnalyzer here
    return {"ip": ip, "detail": "Placeholder"}