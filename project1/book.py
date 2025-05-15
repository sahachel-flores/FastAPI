from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

# decorator to expecify endpoint
@app.get("/books")
async def read_all_books():
    return BOOKS

# Here we are using fastApi to past dynamic data, notice how easy it is
@app.get('/books/{book_title: str}')
async def read_all_books(book_title):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


# Using query
@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Using query and dynamic data
@app.get('/books/{book_author}/')
async def read_author_category(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
            book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/crate_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_boo(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book


@app.delete("/books")
async def delete_book(delete_book: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == delete_book.casefold():
            BOOKS.pop(i)

@app.get('/books/author/')
async def get_author(author: str):
