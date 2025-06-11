from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    print("Test_returh_user starting...")
    response = client.get("/users")
    print("test_return_user's response is ", response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'sachel'
    assert response.json()['email'] == 'sachel@gmail.com'
    assert response.json()['first_name'] == 'sachel'
    assert response.json()['last_name'] == 'flores'
    assert response.json()['role'] == 'admin'

def test_change_password_success(test_user):
    response = client.put("/users/password", json={"password": "test1234",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid(test_user):
    response = client.put("/users/password", json={"password": "test",
                                                "new_password": "newpassword"})
    print(response.json())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password"}