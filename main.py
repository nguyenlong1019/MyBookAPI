from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional

import json

app = FastAPI()

class Book(BaseModel):
    id: Optional[int] = None
    book_name: str
    author: str
    type: str
    page_numbers: int 

with open('books.json', 'r') as f:
    books = json.load(f)

# print(books)

@app.get('/', status_code=200)
def get_status_code():
    return {"Status code": 200}


@app.get('/book/{book_id}', status_code=200)
def get_book(book_id: int):
    book = [book for book in books if book['id'] == book_id]
    return book[0] if len(book) > 0 else {}


@app.get('/search', status_code=200)
def search_book(type: Optional[str] = Query(None, title="Type", description="The type to filter for"),
                book_name: Optional[str] = Query(None, title="Book_Name", description="The book name to filter for")):
                book1 = [book for book in books if book['type'] == type]

                if book_name is None:
                    if type is None:
                        return books
                    else:
                        return book1
                else:
                    book2 = [book for book in books if book_name.lower() in book['book_name'].lower()]
                    if type is None:
                        return book2
                    else:
                        combined = [book for book in book1 if book in book2]
                        return combined

@app.post('/add_book', status_code=201)
def add_book(book: Book):
    book_id = max([book['id'] for book in books]) + 1
    new_book = {
        "id": book_id,
        "book_name": book.book_name,
        "author": book.author,
        "type": book.type,
        "page_numbers": book.page_numbers
    }

    books.append(new_book)

    with open('books.json', 'w') as f:
        json.dump(books, f)
    
    return new_book


@app.put('/change_book', status_code=204)
def change_book(book: Book):
    new_book = {
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "type": book.type,
        "page_numbers": book.page_numbers
    }

    book_list = [b for b in books if b['id'] == book.id]
    if len(book_list) > 0:
        books.remove(book_list[0])
        books.append(new_book)
        with open('books.json', 'w') as f:
            json.dump(books, f)
        return new_book
    else:
        return HTTPException(status_code=404, detail=f"Book with id {book.id} does not exist!")

@app.delete('/delete/{book_id}')
def delete_book(book_id: int):
    book = [book for book in books if book['id'] == book_id]

    if len(book) > 0:
        books.remove(book[0])
        with open('books.json', 'w') as f:
            json.dump(books, f)
    else:
        raise HTTPException(status_code=404, detail=f"There is no book with id {book_id}")