# Root file where we connect everything
from fastapi import FastAPI, APIRouter, HTTPException, Path, Depends, Request # Depends -> dependancy injection which in programming means that we need to do something before we execute what we are trying to execute
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="Project3/templates")

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


# Creating db dependancy
def get_db():
    db = SessionLocal()

    # The yield statement execurtes the prior and the code under the yield. The coder under finally is executed after we obtain a response.
    try:
        # These prints show how code is executed in order
        print("from production Here1")
        yield db
    
    finally:
        print("from production Here3")
        db.close() # closing database after we receive a response


db_dependancy = Annotated[Session, Depends(get_db)] # Creating db dependancy, in order for it to work, get_db must be up and running

user_dependancy = Annotated[dict, Depends(get_current_user)] # Creating a user dependency to force user's authentication for every HTTP method

# Additing conditions to the fields of the column variables of our data base
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependancy):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
    
    except: 
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    except: 
        return redirect_to_login

@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, todo_id: int, db:db_dependancy):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request":request, "todo":todo, "user": user})
    except:
        return redirect_to_login()


### Endpoints


"""
Function below relies on our DB opening up (Depends(get_db()))
"""
@router.get("/")
async def read_all(user: user_dependancy, db: db_dependancy):   # type: ignore
    print("Router:todos: Entering read_all")
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    print("Router:todos: user is not null")
    print("Router:todos: Priting query return:", db.query(Todos).all())
    return db.query(Todos).all()
"""
Fetching database items by id
"""
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependancy, 
                    db: db_dependancy, # type: ignore
                    todo_id: int = Path(gt=0)): 
    print("---------->Calling todo!!!, the is is ", todo_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    # Querying by the input id and the user that was autheticated
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()    
    
    print("The query resulted in ", todo_model)
    if todo_model is not None:
        print("---------->entering todo_model not found!!!")
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')
"""
Creating an item on our database using post
"""
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependancy ,
                      db: db_dependancy, # type: ignore
                      todo_request:  TodoRequest): 
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    

    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id')) # grabing client data (new todo)

    db.add(todo_model) # Telling db session we are about to add something, db needs to know ahead of time what functionality is about to hapopen
    db.commit() # makes add functionality automatically to happen to the db

    return HTTPException(status_code=201, detail="New todo item added to the list")


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependancy,
                      db: db_dependancy,  # type: ignore
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todo_model = db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id == user.get('id')).first() # retrieves firs result of the query

    if todo_model == None:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

    raise HTTPException(status_code=204, detail="New todo item updated successfully")



@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependancy, 
                      db: db_dependancy, # type: ignore
                      todo_id: int = Path(gt=0)): 

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()

    if todo_model == None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).delete() # code to delete a todo from the db

    db.commit()

    raise HTTPException(status_code=204, detail="Item deleted successfully")
