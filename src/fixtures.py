import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import asyncio
from database import async_session_maker
from glampings.models import Glamping, Rental

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def insert_test_data(session: AsyncSession):
    try:
        # Check if the Glamping data already exists
        existing_glamping = await session.execute(select(Glamping))
        existing_glamping = existing_glamping.scalars().all()
        existing_glamping_names = {g.name: g for g in existing_glamping}

        # Prepare new Glamping instances to be added
        glampings_to_add = []
        if 'Forest Retreat' not in existing_glamping_names:
            glampings_to_add.append(Glamping(
                name='Forest Retreat',
                description='A cozy retreat in the forest with all the amenities.',
                price_per_night=100.00,
                capacity=2,
                location='Forest Location',
                amenities={"Wi-Fi": True, "Hot Tub": True},
                owner_id=1
            ))

        if 'Lakeview Cabin' not in existing_glamping_names:
            glampings_to_add.append(Glamping(
                name='Lakeview Cabin',
                description='Beautiful cabin with a view of the lake and mountains.',
                price_per_night=150.00,
                capacity=4,
                location='Lake Location',
                amenities={"Wi-Fi": True, "Air Conditioning": True},
                owner_id=1
            ))

        # Add Glamping instances to the session if they are new
        if glampings_to_add:
            session.add_all(glampings_to_add)
            await session.flush()  # Populate the IDs

        # Check if the Rental data already exists
        existing_rentals = await session.execute(select(Rental))
        existing_rentals = existing_rentals.scalars().all()
        existing_rental_combinations = {(r.user_id, r.glamping_id) for r in existing_rentals}

        # Prepare new Rental instances to be added
        rentals_to_add = []
        glamping1 = existing_glamping_names.get('Forest Retreat')
        glamping2 = existing_glamping_names.get('Lakeview Cabin')

        if glamping1 and (2, glamping1.id) not in existing_rental_combinations:
            rentals_to_add.append(Rental(
                user_id=2,
                glamping_id=glamping1.id,
                start_date=datetime(2024, 7, 1, 14, 0),
                end_date=datetime(2024, 7, 5, 11, 0),
                total_cost=400.00,
                status='confirmed'
            ))

        if glamping2 and (3, glamping2.id) not in existing_rental_combinations:
            rentals_to_add.append(Rental(
                user_id=3,
                glamping_id=glamping2.id,
                start_date=datetime(2024, 8, 10, 15, 0),
                end_date=datetime(2024, 8, 15, 10, 0),
                total_cost=750.00,
                status='confirmed'
            ))

        # Add Rental instances to the session if they are new
        if rentals_to_add:
            session.add_all(rentals_to_add)

        # Commit all the new instances
        await session.commit()
        logger.info("Inserted test data")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await session.rollback()
        logger.info("Transaction rolled back")

# Running the script function
async def main():
    async with async_session_maker() as session:
        await insert_test_data(session)

# Run the script asynchronously
if __name__ == "__main__":
    asyncio.run(main())
