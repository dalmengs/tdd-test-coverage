import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager
from DalmengSimpleTodo.main import app

@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac