from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

class DBBThreatEntry(Base):
    """SQLAlchemy model for the 'threats' table."""
    __tablename__ = "threats"
    
    id = Column(Integer, primary_key=True)
    ip = Column(String(15), nullable=False)
    country = Column(String(50))
    city = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)
    threat_type = Column(String(20))  # e.g., "Trojan", "DDoS"
    timestamp = Column(DateTime, default=datetime.utcnow)

class ThreatEntry(BaseModel):
    """Pydantic model for API responses."""
    ip: str
    country: str
    city: str
    latitude: float
    longitude: float
    threat_type: str
    timestamp: datetime

    class Config:
        orm_mode = True