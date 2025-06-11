from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    #print("response is ", response.json())
    assert response.json() == [{'title':'Learn to code', 'description':'Need to learn everyday', 'complete': False, 'priority': 5, 'id': 1, 'owner_id': 1}]
                               

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    response1 = client.get("")
    print("this response1 is ", response1.json())
    print("this response is ", response.json())

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title':'Learn to code', 'description':'Need to learn everyday', 'complete': False, 'priority': 5, 'id': 1, 'owner_id': 1}
    

def test_read_auth_not_found():
    response = client.get("/todo/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo',
        'description': 'New descrip',
        'priority': 1,
        'complete': False
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == 201
    
    # Testing our item is in the database
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        'title': 'New Todo Updated',
        'description': 'New descrip',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/1", json=request_data)

    assert response.status_code == 204

    # Testing our item is in the database
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == "New Todo Updated"
    assert model.priority == 5

def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'New Todo Updated',
        'description': 'New descrip',
        'priority': 5,
        'complete': False
    }

    response = client.put("/todo/99", json=request_data)

    assert response.status_code == 404
    assert response.json() == {'detail': "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete('/todo/1')

    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete('/todo/99')

    assert response.status_code == 404
    assert response.json() == {'detail': "Todo not found"}

