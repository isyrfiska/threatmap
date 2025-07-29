from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from database.queries import get_attack_stats, get_recent_attacks, get_country_stats

app = FastAPI(title="Trojan ThreatMap API",
              description="Real-time Trojan attack data API",
              version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
async def get_stats(hours: int = 24):
    try:
        stats = get_attack_stats(hours)
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recent-attacks")
async def recent_attacks(limit: int = 20):
    try:
        attacks = get_recent_attacks(limit)
        return {"status": "success", "data": attacks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/country-stats")
async def country_stats(hours: int = 24):
    try:
        stats = get_country_stats(hours)
        return {"status": "success", "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))