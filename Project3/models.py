# Database model is a way for SQL alchemy to be understand what kind of database tables we are going to create within our database table
from .database import Base # creating this model for database.py file
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String) # Encrypted password 
    is_active = Column(Boolean, default=True) # option for active and unactive users
    role = Column(String)
    #phone_number = Column(String)


class Todos(Base):
    __tablename__ = 'todosapp' # Way for SQL alchemy to know what to name this table inside our database

    # Columns of our
    id = Column(Integer, primary_key=True, index=True) # Want index true to improve performance and thi primary_key true since this is the identifier 
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id")) # foreign key that reference the user