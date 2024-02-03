from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json


class GlampingBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_night: float
    capacity: int
    location: str
    amenities: Optional[json] = None


class GlampingCreate(GlampingBase):
    pass


class Glamping(GlampingBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class RentalBase(BaseModel):
    user_id: int
    glamping_id: int
    start_date: datetime
    end_date: datetime
    total_cost: float
    status: str


class RentalCreate(RentalBase):
    pass


class Rental(RentalBase):
    id: int

    class Config:
        orm_mode = True
