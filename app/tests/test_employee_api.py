from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient
from app.api import app, employees


@pytest.fixture
def client():
    employees.clear()
    with TestClient(app) as client:
        yield client
    employees.clear()
def test_create_employee_can_be_retrived(client):
    body={
        "name":"simge",
        "last_name":"şahin",
        "department":"Data Engineering",
        "age":25,
    }
    created=client.post("/employees",json=body)
    assert created.status_code ==201
    employee_id=created.json()["id"]
    response=client.get(f"/employees/{employee_id}")

    assert response.status_code==200
    assert response.json()=={"id":employee_id, **body}
def test_patch_update_only_department(client):
    body={
        "name":"Görkem",
        "last_name":"Can",
        "department":"Data Engineer",
        "age":10,
    }
    created= client.post("/employees",json=body)
    assert created.status_code==201
    employee_id= created.json()["id"]

    response=client.patch(f"/employees/{employee_id}",json={"department":"LLM Engineering"},)
    excepted={"id":employee_id,**body,"department":"LLM Engineering", }

    assert response.status_code==200
    assert response.json()== excepted

    saved =client.get(f"/employees/{employee_id}")
    assert saved.status_code==200
    assert saved.json()==excepted
def payload(**changes):
    return {"name": "Galip", "last_name": "Diler", "department": "AI", "age": 26, **changes}


@pytest.mark.parametrize("name,last_name", [
    ("Galip", "Diler"), (" GALIP ", " DİLER "), ("galip", "diler"),
])
def test_duplicate_is_rejected_without_inserting(client, name, last_name):
    first = client.post("/employees", json=payload())
    assert first.status_code == 201
    second = client.post("/employees", json=payload(name=name, last_name=last_name, age=30))
    assert second.status_code == 409
    assert len(employees) == 1
    saved = client.get(f"/employees/{first.json()['id']}")
    assert saved.json()["age"] == 26
    assert saved.json()["last_name"] == "Diler"

@pytest.mark.parametrize("changes", [{"last_name": "Kaya"}, {"name": "Ayşe"}])
def test_different_person_is_accepted(client, changes):
    assert client.post("/employees", json=payload()).status_code == 201
    assert client.post("/employees", json=payload(**changes)).status_code == 201

@pytest.mark.parametrize("field", ["name", "last_name"])
def test_whitespace_only_names_are_rejected(client, field):
    assert client.post("/employees", json=payload(**{field: " \t "})).status_code == 422
    assert not employees

def test_last_name_is_required(client):
    body = payload()
    del body["last_name"]
    assert client.post("/employees", json=body).status_code == 422

def test_internal_spaces_are_normalized(client):
    assert client.post("/employees", json=payload(name=" Ali  Can ")).json()["name"] == "Ali Can"
    assert client.post("/employees", json=payload(name="Ali Can")).status_code == 409

def test_concurrent_duplicates_create_one_record(client):
    with ThreadPoolExecutor(max_workers=4) as pool:
        codes = list(pool.map(lambda _: client.post("/employees", json=payload()).status_code, range(8)))
    assert codes.count(201) == 1
    assert codes.count(409) == 7
    assert len(employees) == 1
def test_deleted_employee_cannot_be_retrieved(client):
    body = {
        "name": "Ayşe",
        "last_name": "Kaya",
        "department": "Data Engineering",
        "age": 28,
    }

    created = client.post("/employees", json=body)
    assert created.status_code == 201
    employee_id = created.json()["id"]

    deleted = client.delete(f"/employees/{employee_id}")

    assert deleted.status_code == 204
    assert deleted.content == b""

    fetched = client.get(f"/employees/{employee_id}")
    assert fetched.status_code == 404

    deleted_again = client.delete(f"/employees/{employee_id}")
    assert deleted_again.status_code == 404
@pytest.mark.parametrize(
    "invalid_body",
    [
        {"department": ""},
        {"department": "   "},
        {},
    ],
)
def test_invalid_employee(client,invalid_body):
    body={
        "name":"Ece",
        "last_name":"Can",
        "department":"ML Engineer",
        "age":4,
    }
    created= client.post("/employees",json=body)
    assert created.status_code==201
    original= created.json()
    employee_id=original["id"]
    response= client.patch(f"employees/{employee_id}",json=invalid_body,)
    assert response.status_code==422
    saved=client.get(f"/employees/{employee_id}")
    assert saved.status_code==200
    assert saved.json()== original