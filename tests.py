import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient

from main import app
from main import database

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture
async def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture(scope="function", autouse=True)
async def db():
    async with database:
        yield


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


async def test_app(client) -> None:
    # note: you _must_ set `base_url` for relative urls like "/" to work
    r = await client.get("/")
    assert r.status_code == 200
    assert r.text == "Hello World!"
    data = await database.execute("select 'Hello World!'")
    assert data == "Hello World!"
