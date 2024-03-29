from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class GlampingBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_night: float
    capacity: int
    location: str
    amenities: Optional[Dict[str, Any]] = None
    owner_id: int

    class Config:
        from_attributes = True


class GlampingCreate(GlampingBase):
    pass


class Glamping(GlampingBase):
    id: int


class RentalBase(BaseModel):
    user_id: int
    glamping_id: int
    start_date: datetime
    end_date: datetime
    total_cost: float
    status: str

    class Config:
        from_attributes = True


class RentalCreate(RentalBase):
    pass


class Rental(RentalBase):
    id: int
