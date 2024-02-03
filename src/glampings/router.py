from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import glamping, rental
from schemas import GlampingCreate
from schemas import RentalCreate
router = APIRouter(prefix="/glamping", tags=["Glamping"])


@router.get("/")
async def get_glampings(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(glamping)
        result = await session.execute(query)
        glampings = result.scalars().all()
        return {"status": "success", "data": glampings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def add_glamping(new_glamping: GlampingCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(glamping).values(**new_glamping.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/rental")
async def get_rentals(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(rental)
        result = await session.execute(query)
        rentals = result.scalars().all()
        return {"status": "success", "data": rentals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rental")
async def add_rental(new_rental: RentalCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(rental).values(**new_rental.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))