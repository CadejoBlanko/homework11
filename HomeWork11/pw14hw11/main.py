"""
FastAPI Application
===================

This is a FastAPI application for managing contacts.

It includes endpoints for sign up, login, creating, retrieving,
updating, and deleting contacts.

"""

from datetime import date, timedelta

from fastapi import FastAPI, HTTPException, status, Depends, Query, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import uvicorn

from models import Contact, User
from database.connection import get_db
from schemas import ContactCreate, Contact as ContactSchema, UserModel
from routes.auth import auth_service
from routes import auth, contact

app = FastAPI()
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix='/api')
app.include_router(contact.router, prefix='/api')


@app.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    """
    Sign Up Endpoint

    Register a new user.

    Args:
        body (UserModel): User registration information.

    Returns:
        dict: A dictionary containing the email of the newly registered user.

    Raises:
        HTTPException: If the account already exists.

    """
    exist_user = db.query(User).filter(User.email == body.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = User(email=body.username, password=auth_service.get_password_hash(body.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}


@app.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login Endpoint

    Log in an existing user.

    Args:
        body (OAuth2PasswordRequestForm): User login information.

    Returns:
        dict: Access and refresh tokens along with the token type.

    Raises:
        HTTPException: If the email or password is invalid.

    """
    user = db.query(User).filter(User.email == body.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh Token Endpoint

    Refresh an expired access token.

    Args:
        credentials (HTTPAuthorizationCredentials): User credentials with refresh token.

    Returns:
        dict: Access and refresh tokens along with the token type.

    Raises:
        HTTPException: If the refresh token is invalid.

    """
    token = credentials.credentials
    email = await auth_service.create_refresh_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get("/")
async def root():
    """
    Root Endpoint

    A simple message to indicate the server is running.

    Returns:
        dict: A message indicating the server is running.

    """
    return {"message": "Hello World"}


@app.get("/secret")
async def read_item(current_user: User = Depends(auth_service.get_current_user)):
    """
    Secret Endpoint

    Access a secret route for authenticated users.

    Args:
        current_user (User): The currently authenticated user.

    Returns:
        dict: A secret message along with the owner's email.

    """
    return {"message": 'secret router', "owner": current_user.email}


@app.post("/contacts/", response_model=ContactSchema)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Create Contact Endpoint

    Create a new contact.

    Args:
        contact (ContactCreate): Contact information.

    Returns:
        ContactSchema: The created contact.

    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/", response_model=list[ContactSchema])
def get_contacts(search_name: str = Query(None), search_email: str = Query(None), db: Session = Depends(get_db)):
    """
    Get Contacts Endpoint

    Retrieve a list of contacts.

    Args:
        search_name (str, optional): Filter contacts by name. Defaults to None.
        search_email (str, optional): Filter contacts by email. Defaults to None.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[ContactSchema]: List of contacts.

    """
    query = db.query(Contact)
    if search_name:
        query = query.filter(Contact.first_name.contains(search_name) | Contact.last_name.contains(search_name))
    if search_email:
        query = query.filter(Contact.email.contains(search_email))
    return query.all()


@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Get Contact by ID Endpoint

    Retrieve a contact by its ID.

    Args:
        contact_id (int): The ID of the contact.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        ContactSchema: The requested contact.

    Raises:
        HTTPException: If the contact is not found.

    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Update Contact by ID Endpoint

    Update a contact's information.

    Args:
        contact_id (int): The ID of the contact to be updated.
        contact (ContactCreate): New contact information.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        ContactSchema: The updated contact.

    Raises:
        HTTPException: If the contact is not found.

    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for attr, value in contact.dict().items():
        setattr(db_contact, attr, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.delete("/contacts/{contact_id}", response_model=ContactSchema)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Delete Contact by ID Endpoint

    Delete a contact by its ID.

    Args:
        contact_id (int): The ID of the contact to be deleted.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        ContactSchema: The deleted contact.

    Raises:
        HTTPException: If the contact is not found.

    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact


@app.get("/upcoming_birthdays", response_model=list[ContactSchema])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    """
    Get Upcoming Birthdays Endpoint

    Retrieve a list of contacts with upcoming birthdays.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        list[ContactSchema]: List of contacts with upcoming birthdays.

    """
    today = date.today()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        (Contact.birthdate >= today) & (Contact.birthdate <= end_date)
    ).all()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)