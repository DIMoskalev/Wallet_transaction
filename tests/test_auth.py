from httpx import AsyncClient

from app.models import User
from app.users.auth import get_password_hash
from tests.conftest import async_session_maker


async def test_register_user(ac: AsyncClient):
    data = {
        "full_name": "Test",
        "email": "Test@test.ru",
        "phone": "+79999999999",
        "hashed_password": "Testtesttest!",
    }
    response = await ac.post("/users/register/", json=data)
    assert response.status_code == 200


async def test_register_user_again(ac: AsyncClient):
    data = {
        "full_name": "Test",
        "email": "Test@test.ru",
        "phone": "+79999999999",
        "hashed_password": "Testtesttest!"
    }
    response = await ac.post("/users/register/", json=data)
    assert response.status_code == 409


async def test_login_fail_incorrect_data(ac: AsyncClient):
    response = await ac.post("/users/login/", json={
        "full_name": "Test",
        "email": "Test@test.ru",
        "phone": "+79999999999",
        "hashed_password": "Testtesttest1!"
    }
                             )
    assert response.status_code == 401


async def test_login_success(ac: AsyncClient):
    response = await ac.post("/users/login/", json={
        "full_name": "Test",
        "email": "Test@test.ru",
        "phone": "+79999999999",
        "hashed_password": "Testtesttest!"
    }
                             )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_me(ac: AsyncClient):
    response = await ac.get("/users/me/")
    assert response.status_code == 200
    assert response.json()["email"] == "Test@test.ru"


async def test_get_all_not_admin(ac: AsyncClient):
    response = await ac.get("/users/all_users/")
    assert response.status_code == 403


async def test_logout(ac: AsyncClient):
    response = await ac.post("/users/logout/")

    assert response.status_code == 200


async def test_me_when_logout(ac: AsyncClient):
    response = await ac.get("/users/me/")
    assert response.status_code == 401


async def test_register_admin(ac: AsyncClient):
    async with async_session_maker() as session:
        user = User(
            full_name="Admin",
            email="Admin@admin.ru",
            phone="+71111111111",
            hashed_password=get_password_hash("Adminadmin!"),
            is_admin=True,
        )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    await session.close()
    assert user.is_admin is True


async def test_login_admin(ac: AsyncClient):
    response = await ac.post("/users/login/", json={
        "full_name": "Admin",
        "email": "Admin@admin.ru",
        "phone": "+71111111111",
        "hashed_password": "Adminadmin!",
    }
                             )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_get_all(ac: AsyncClient):
    response = await ac.get("/users/all_users/")
    assert response.status_code == 200
    assert len(response.json()) > 0
