from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

# uvicorn books_two:app --reload
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=2026)
    # Creating config schema to add default values 
    model_config = {
            "json_schema_extra":{
                "example":{
                    "title":"A new book",
                    "author":"coding",
                    "description":"A new description of a book",
                    "rating":5
                }
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2012),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2016),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2025),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2000),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 1978),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2025)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}") # creating endpoint with book_id, which is passed by the user 
async def read_book(book_id: int = Path(gt=0)): # book_id is an integer
    for book in BOOKS: 
        if book.id == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="item not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0,lt=6)):
    return_books = []
    for book in BOOKS:
        if book.rating == book_rating:
            return_books.append(book)
    return return_books

@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_year(published_year:int = Query(gt=0, lt=2026)):
    return_books = []
    for i in range( len(BOOKS)):
        if BOOKS[i].published_date == published_year:
            return_books.append(BOOKS[i])
    return return_books


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
     # ** unpack the dictionary, key/value pairs are separed by comma, thus an easy way to popula the dictionary
     # Doing this to change the type of the book request
    new_book = Book(**book_request.model_dump())
 
    # Appending newly created book
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    # book.id = BOOKS[-1] + 1 if len(BOOKS) > 0 else book.id = 1
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change=True
    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False 
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            book_change = True
            BOOKS.pop(i)
            break
    if not book_change:
        raise HTTPException(status_code=404, detail="Item not found")
