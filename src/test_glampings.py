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
    assert len(response.json()['data']) == 2  # Например, если вы вставили два глемпинга