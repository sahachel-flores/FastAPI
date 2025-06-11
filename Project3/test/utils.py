from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

print("Entering utils ")
SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    print("Test: enter get_db")
    db = TestingSessionLocal()
    print("Test: done DB TestingSessionLocal")
    try:
        yield db
        
    finally:
        print("Test: closing test DB")
        db.close()

def override_get_current_user():
    print("Test: overriding current current_user ")
    return {'username': 'sachel', 'id': 1, 'user_role': 'admin', 'last_name': "flores", "first_name": "sachel"}

client = TestClient(app)

@pytest.fixture
def test_todo():
    #print("Enter test_todo")
    todo = Todos(
        title = "Learn to code",
        description = "Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        print("Deleting from db")
        connection.execute(text("DELETE FROM todosapp;"))
        connection.commit()

@pytest.fixture
def test_user():
    print("Staring test_user fixture")

    user = Users(
        username = "sachel",
        email = "sachel@gmail.com",
        first_name = "sachel", 
        last_name = "flores",
        hashed_password = bcrypt_context.hash("test1234"),
        role = "admin"
    )
    print(f"the user is {user.username}")
    print("Test: Done creating user, adding to db ....")
    db_test = TestingSessionLocal()
    print("Test: Done creating DB starting session")
    db_test.add(user)
    print("Test: Done adding user")

    db_test.commit()
    print("Test: Done commiting")
    print(db_test.query(Users).filter(Users.username == "sachel").first())
    #print(db.query(Users).filter(Users.id == user.ge('id')).first())
    # code below deletes all the users from database 
    yield user
    with engine.connect() as connection:
        print("Deleting from db")
        #print(db.query(Users).filter(Users.id == user.ge('id')).first())
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
        print("Test: done deleting test DB")