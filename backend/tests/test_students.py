import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_student(client: AsyncClient, auth_headers):
    response = await client.post("/students/", json={
        "name": "Test Student",
        "age": 20,
        "department": "Computer Science",
        "email": "teststudent@example.com",
        "phone": "9876543210",
        "address": "Chennai"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Student"
    assert data["department"] == "Computer Science"


@pytest.mark.asyncio
async def test_get_all_students(client: AsyncClient, auth_headers):
    response = await client.get("/students/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "students" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_student_by_id(client: AsyncClient, auth_headers):
    create_response = await client.post("/students/", json={
        "name": "Get Student",
        "age": 22,
        "department": "Physics",
        "email": "getstudent@example.com"
    }, headers=auth_headers)
    student_id = create_response.json()["id"]

    response = await client.get(f"/students/{student_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == student_id


@pytest.mark.asyncio
async def test_get_nonexistent_student(client: AsyncClient, auth_headers):
    response = await client.get("/students/99999", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_student(client: AsyncClient, auth_headers):
    create_response = await client.post("/students/", json={
        "name": "Update Student",
        "age": 21,
        "department": "Math",
        "email": "updatestudent@example.com"
    }, headers=auth_headers)
    student_id = create_response.json()["id"]

    response = await client.put(f"/students/{student_id}", json={"age": 25}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["age"] == 25


@pytest.mark.asyncio
async def test_delete_student(client: AsyncClient, auth_headers):
    create_response = await client.post("/students/", json={
        "name": "Delete Student",
        "age": 19,
        "department": "Chemistry",
        "email": "deletestudent@example.com"
    }, headers=auth_headers)
    student_id = create_response.json()["id"]

    response = await client.delete(f"/students/{student_id}", headers=auth_headers)
    assert response.status_code == 200

    check_response = await client.get(f"/students/{student_id}", headers=auth_headers)
    assert check_response.status_code == 404
