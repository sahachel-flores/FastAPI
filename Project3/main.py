# Root file where we connect everything
from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# This will only run if the database is not created 
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="Project3/static"), name="static") # Creating static file within our directory



@app.get("/")
def test(request: Request):
   return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router) # Code to include our router file
app.include_router(todos.router) # Code to include our router file
app.include_router(admin.router)
app.include_router(users.router)

# go to terminal and run uvicorn main:app ---reload --port 5000, this will create a database file named todo.db
# then open other terminal cd to project 3 and run sqlite todo.db, now you can interact with the database

