import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from glampings.models import glamping, rental
from datetime import datetime
import asyncio

from database import async_session_maker

# loging init
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def insert_test_data(session: AsyncSession):
    try:
        # Inserting data in glampig table & return id
        glamping_insert = insert(glamping).returning(glamping.c.id).values([
            {'name': 'Forest Retreat', 'description': 'A cozy retreat in the forest with all the amenities.',
             'price_per_night': 100.00, 'capacity': 2, 'location': 'Forest Location',
             'amenities': {"Wi-Fi": True, "Hot Tub": True}, 'owner_id': 1},
            {'name': 'Lakeview Cabin', 'description': 'Beautiful cabin with a view of the lake and mountains.',
             'price_per_night': 150.00, 'capacity': 4, 'location': 'Lake Location',
             'amenities': {"Wi-Fi": True, "Air Conditioning": True}, 'owner_id': 1}
        ])
        result = await session.execute(glamping_insert)
        glamping_ids = [row[0] for row in result.fetchall()]  # return of data
        await session.flush()  # drop without transaction
        logger.info(f"Inserted glamping data with IDs: {glamping_ids}")

        # initialization of data to insert in rental table
        rental_data = [
            {'user_id': 1, 'glamping_id': glamping_ids[0], 'start_date': datetime(2024, 7, 1, 14, 0), 'end_date': datetime(2024, 7, 5, 11, 0), 'total_cost': 400.00, 'status': 'confirmed'},
            {'user_id': 2, 'glamping_id': glamping_ids[1], 'start_date': datetime(2024, 8, 10, 15, 0), 'end_date': datetime(2024, 8, 15, 10, 0), 'total_cost': 750.00, 'status': 'confirmed'}
        ]

        # Insert into rentals
        rental_insert = insert(rental).values(rental_data)
        await session.execute(rental_insert)
        logger.info("Inserted rental data")

        await session.commit()
        logger.info("Committed the transaction")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await session.rollback()
        logger.info("Transaction rolled back")


# Running script function
async def main():
    async with async_session_maker() as session:
        await insert_test_data(session)

# Run Async
if __name__ == "__main__":
    asyncio.run(main())
