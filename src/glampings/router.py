from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_async_session
from glampings.models import Glamping, Rental
from glampings.schemas import GlampingCreate, RentalCreate, GlampingBase, RentalBase

router = APIRouter(prefix="/glamping", tags=["Glamping"])

@router.get("/")
async def get_glampings(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Glamping)
        result = await session.execute(query)
        glampings_list = result.scalars().all()
        return {"status": "success", "data": [GlampingBase.from_orm(g).dict() for g in glampings_list]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def add_glamping(new_glamping: GlampingCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        glamping_data = new_glamping.dict(exclude_unset=True)
        new_glamping_obj = Glamping(**glamping_data)  # You create a new ORM model instance here
        session.add(new_glamping_obj)
        await session.commit()
        await session.refresh(new_glamping_obj)
        return {"status": "success", "data": new_glamping_obj}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rental")
async def get_rentals(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Rental))
        rentals_list = result.scalars().all()
        return {"status": "success", "data": [RentalBase.from_orm(r).dict() for r in rentals_list]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rental")
async def add_rental(new_rental: RentalCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        rental_obj = Rental(**new_rental.dict())
        session.add(rental_obj)
        await session.commit()

        # Возврат данных с учетом вновь созданного объекта
        return {"status": "success", "data": rental_obj.dict()}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
