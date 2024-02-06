import pytest
from database import async_session_maker
from httpx import AsyncClient
from main import app
from fixtures import insert_test_data
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def test_db_session():

    async with async_session_maker() as session:
        await insert_test_data(session)
        yield session

        await session.rollback()


@pytest.mark.asyncio
async def test_get_glampings(test_db_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/glamping/")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    # Проверка, что данные соответствуют вашим тестовым данным
    assert len(response.json()['data']) == 2


@pytest.mark.asyncio
async def test_add_glamping(test_db_session):
    new_glamping = {
        "name": "New Glamping",
        "description": "Test Description",
        "price_per_night": 120.00,
        "capacity": 3,
        "location": "Test Location",
        "amenities": {"Wi-Fi": True},
        "owner_id": 1
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/glamping/", json=new_glamping)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


@pytest.mark.asyncio
async def test_get_rentals(test_db_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/glamping/rental")
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    # Проверка, что данные соответствуют вашим тестовым данным
    assert len(response.json()['data']) == 2  # Если вы вставили две аренды