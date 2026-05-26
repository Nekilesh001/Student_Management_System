import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "role": "student"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "student"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "password123",
        "role": "student"
    })
    response = await client.post("/auth/register", json={
        "username": "dupuser2",
        "email": "dup@example.com",
        "password": "password123",
        "role": "student"
    })
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "password123",
        "role": "student"
    })
    response = await client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    response = await client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401