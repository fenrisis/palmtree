from sqlalchemy import Column, Integer, String, Numeric, JSON, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base


class Glamping(Base):
    __tablename__ = 'glamping'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_per_night = Column(Numeric, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(String)
    amenities = Column(JSON)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="glampings")


class Rental(Base):
    __tablename__ = 'rental'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    glamping_id = Column(Integer, ForeignKey("glamping.id"))
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    total_cost = Column(Numeric, nullable=False)
    status = Column(String, nullable=False)
    user = relationship("User", back_populates="rentals")
