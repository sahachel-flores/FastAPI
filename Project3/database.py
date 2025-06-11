from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
print("Entering development database")
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
POSTGRES_DATABASE_URL = 'postgresql://postgres:postgres@localhost/TodoApplicationDatabase'


# Creating our enginer, need database path, connect_args allows to define some kind of connection to a database
# We have false for check_same_thread to prevent accident sharing of the same connection
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# The sessionLocal is an instance of the database 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating database object with can interact with
Base = declarative_base()
print("Exiting development database")

