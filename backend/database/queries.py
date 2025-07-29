from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import DBBThreatEntry, ThreatEntry
from typing import List

async def get_recent_threats(session: AsyncSession, limit: int = 100) -> List[ThreatEntry]:
    """Fetch the most recent threats from the database."""
    result = await session.execute(
        select(DBBThreatEntry).order_by(DBBThreatEntry.timestamp.desc()).limit(limit)
    return [ThreatEntry.from_orm(entry) for entry in result.scalars()]