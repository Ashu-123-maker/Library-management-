
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List
from models import Librarian,Books,Log_Operations,Category
from schemas import LibrarianDTO, SuccessDTO,LoginDTO,BooksDTO,Log_OperationsDTO,CategoryDTO
from database import get_db
import re
from datetime import timedelta

app = FastAPI()


# Defining a dependency for the database session
db_dependency = Annotated[Session, Depends(get_db)]
#this is an endpoint to creaate a new librarian data
@app.post("/Librarian", response_model=SuccessDTO)
def create_librarian(librarian_dto: LibrarianDTO, db: db_dependency):
    librarian_obj = Librarian(
        name=librarian_dto.name,
        password=librarian_dto.password,
        email=librarian_dto.email,
        phonenumber=librarian_dto.phonenumber,
        address=librarian_dto.address,
        role=librarian_dto.role
    )
#checks if the email has proper validation with "@gmail.com"
    if not librarian_dto.email.endswith("@gmail.com"):
        raise HTTPException(status_code=409, detail="Invalid email address")
#checks if there exists duplicate mail   
    email_check = db.query(Librarian).filter(Librarian.email == librarian_dto.email).first()
    if email_check is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
#checks the sufficient length of password
    if len(librarian_dto.password) < 7:
        raise HTTPException(status_code=400, detail="Password must be more than 6 characters")
#checks if the length of the phone number is between 10 to 12 digits 
    if not re.match(r"^\d{10,12}$", librarian_dto.phonenumber):
        raise HTTPException(status_code=400, detail="Phone number must be between 10 to 12 digits")
    
#add a new librarian to database
    db.add(librarian_obj)
    db.commit()
    db.refresh(librarian_obj)
    

    return SuccessDTO(status_code=201, message="Successfully added")
#An end point to fetch all of the data in librarian
@app.get("/Librarian", response_model=List[LibrarianDTO])
def get_librarians(db: db_dependency):
    result = db.query(Librarian).all()
    return result

#An end point to fetch  librarian data by ID
@app.get("/Librarian/{librarian_id}", response_model=LibrarianDTO)
def get_librarian_by_id(librarian_id: int, db: db_dependency):
    result = db.query(Librarian).filter(Librarian.id == librarian_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

#An Endpoint to delete a librarian by ID
@app.delete("/Librarian/{librarian_id}", response_model=SuccessDTO)
def delete_librarian(librarian_id: int, db: db_dependency):
    librarian = db.query(Librarian).filter(Librarian.id == librarian_id).first()
    if librarian is None:
        raise HTTPException(status_code=404, detail="Librarian not found")
    
    db.delete(librarian)
    db.commit()
    
    return SuccessDTO(status_code=200, message="Successfully deleted")


# Endpoint to handle librarian login
@app.post("/login")
def login(login_dto: LoginDTO, db: db_dependency):
    # Retrieve the librarian from the database based on the provided email
    database= db.query(Librarian).filter(Librarian.email == login_dto.email).first()
    
    if database is None:
        raise HTTPException(status_code=401, detail={"status_code":401,"message":"User not found"})

    # Check if the provided password matches the password stored in the database
    if Librarian.password != database.password:
        raise HTTPException(status_code=401,detail={"status_code":401,"message":"Invalid password"})

    return SuccessDTO(status_code=200, message="Login successful")

#an end point to add a new book
@app.post("/Books", response_model=SuccessDTO)
def create_book(book_dto: BooksDTO, db: db_dependency):
    book_obj= Books(
        ISBN=book_dto.ISBN,
        title=book_dto.title,
        author=book_dto.author,
        category_id=book_dto.category_id
    )
#add a book to the database
    db.add(book_obj)
    db.commit()
    return SuccessDTO(status_code=201, message="Book added successfully")

# Endpoint to get a list of all books
@app.get("/Books", response_model=List[BooksDTO])
def get_books(db: db_dependency):
    book = db.query(Books).all()
    return book


# Endpoint to get a book by ISBN
@app.get("/Books/{isbn}", response_model=BooksDTO)
def get_book_by_isbn(isbn: str, db: db_dependency):
    book = db.query(Books).filter(Books.ISBN ==isbn ).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/Books/Category/{category_id}", response_model=List[BooksDTO])
def get_books_by_category(category_id: int, db: Session = Depends(get_db)):

    books = db.query(Books).filter(Books.category_id == category_id).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this category")
    return books 


@app.put("/Books/{isbn}", response_model=SuccessDTO)
def update_book(isbn: str, book_dto: BooksDTO, db: db_dependency):
    book = db.query(Books).filter(Books.ISBN == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.title = book_dto.title
    book.author = book_dto.author
    
    db.commit()
    return SuccessDTO(status_code=200, message="Book updated successfully")


# Endpoint to delete a book by ISBN
@app.delete("/Books/{isbn}", response_model=SuccessDTO)
def delete_book(isbn: str, db: db_dependency):
    book = db.query(Books).filter(Books.ISBN == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    
    return SuccessDTO(status_code=200, message="Book deleted successfully")


# Create a new log operation
@app.post("/Log_Operations", response_model=SuccessDTO)
def create_log_operation(log_operations_dto: Log_OperationsDTO, db: db_dependency):
    return_date = log_operations_dto.borrow_date + timedelta(days=15)
    log_operation = Log_Operations(
        id=log_operations_dto.id,
        name=log_operations_dto.name,
        title=log_operations_dto.title,
       # borrow_date=log_operations_dto.borrow_date,

        return_date=return_date
    )
    
    db.add(log_operation)
    db.commit()
    db.refresh(log_operation)

    return SuccessDTO(status_code=201, message="Log operation added successfully")

# Get all log operations
@app.get("/Log_Operations", response_model=List[Log_OperationsDTO])
def get_log_operations(db: db_dependency):
    log_operations = db.query(Log_Operations).all()
    print(log_operations)
    return log_operations


# Get a log operation by log_id
@app.get("/Log_Operations/{log_id}", response_model=Log_OperationsDTO)
def get_log_operation(log_id: int, db: db_dependency):
    log_operation = db.query(Log_Operations).filter(Log_Operations.log_id == log_id).first()
    if log_operation is None:
        raise HTTPException(status_code=404, detail="Log operation not found")
    return log_operation

# Update a log operation
@app.put("/Log_Operations/{log_id}", response_model=SuccessDTO)
def update_log_operation(log_id: int, log_operations_dto: Log_OperationsDTO, db: db_dependency):
    log_operation = db.query(Log_Operations).filter(Log_Operations.log_id == log_id).first()
    if log_operation is None:
        raise HTTPException(status_code=404, detail="Log operation not found")


    log_operation.name = log_operations_dto.name
    log_operation.title = log_operations_dto.title
 
  
    db.commit()

    return SuccessDTO(status_code=200, message="Log operation updated successfully")


# Delete a log operation
@app.delete("/Log_Operations/{log_id}", response_model=SuccessDTO)
def delete_log_operation(log_id: int, db: db_dependency):
    log_operation = db.query(Log_Operations).filter(Log_Operations.log_id == log_id).first()
    if log_operation is None:
        raise HTTPException(status_code=404, detail="Log operation not found")

    db.delete(log_operation)
    db.commit()

    return SuccessDTO(status_code=200, message="Log operation deleted successfully")

# create a  new category

@app.post("/Category/", response_model=SuccessDTO)
def create_category(category_dto: CategoryDTO, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.category_name == category_dto.category_name).first()
    if existing_category is not None:
        raise HTTPException(status_code=400, detail={"status_code": 400, "message": "Category name already exists"})

    category_obj = Category(
        category_name=category_dto.category_name,
        shelf_no=category_dto.shelf_no,

    )
    
    db.add(category_obj)
    db.commit()
    db.refresh(category_obj)  
    
    return {"status_code": 200, "message": "Category created successfully"}

#update category name

@app.put("/Category/{category_id}", response_model=SuccessDTO)
def update_category(category_id: int, category_dto: CategoryDTO, db: Session = Depends(get_db)):
    category_obj = db.query(Category).filter(Category.category_id == category_id).first()

    if category_obj is None:
        raise HTTPException(status_code=404, detail="Category not found")

    category_obj.category_name = category_dto.category_name
    category_obj.shelf_no = category_dto.shelf_no

    db.commit()
    db.refresh(category_obj)

    return SuccessDTO(status_code=200, message="Category updated successfully")

#Retrive data of category table
@app.get("/Category/", response_model=List[CategoryDTO])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories