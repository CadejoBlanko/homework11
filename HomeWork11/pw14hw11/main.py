from datetime import date, timedelta

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from models import Contact
from database.connection import get_db
from schemas import ContactCreate, Contact as ContactSchema

app = FastAPI()


@app.post("/contacts/", response_model=ContactSchema)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts/", response_model=list[ContactSchema])
def get_contacts(search_name: str = Query(None), search_email: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(Contact)
    if search_name:
        query = query.filter(Contact.first_name.contains(search_name) | Contact.last_name.contains(search_name))
    if search_email:
        query = query.filter(Contact.email.contains(search_email))
    return query.all()


@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
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
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact


@app.get("/upcoming_birthdays", response_model=list[ContactSchema])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        (Contact.birthdate >= today) & (Contact.birthdate <= end_date)
    ).all()