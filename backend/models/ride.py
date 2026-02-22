from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class Ride(BaseModel):
    rideName: str
    rideStartTime: datetime
    rideStartPoint: str
    rideEndPoint: str
    rideDuration: Optional[float] = None
    haltDuration: Optional[float] = None
    routeLink: Optional[str] = None
    maxParticipants: int = 20


