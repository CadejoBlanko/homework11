from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import Contact, User
from schemas import Contact as ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Get a list of contacts for a specific user.

    Args:
        skip (int): Number of contacts to skip.
        limit (int): Maximum number of contacts to return.
        user (User): The user for whom to retrieve contacts.
        db (Session): The database session.

    Returns:
        List[Contact]: A list of Contact objects.

    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Get a specific contact for a user.

    Args:
        contact_id (int): The ID of the contact.
        user (User): The user for whom to retrieve the contact.
        db (Session): The database session.

    Returns:
        Contact: The Contact object.

    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Create a new contact for a user.

    Args:
        body (ContactModel): The contact information.
        user (User): The user for whom to create the contact.
        db (Session): The database session.

    Returns:
        Contact: The created Contact object.

    """
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        phone_number=body.phone_number,
        email=body.email,
        birthdate=body.birthdate,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    Update an existing contact for a user.

    Args:
        contact_id (int): The ID of the contact to update.
        body (ContactModel): The updated contact information.
        user (User): The user for whom the contact belongs.
        db (Session): The database session.

    Returns:
        Contact | None: The updated Contact object, or None if the contact was not found.

    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone_number = body.phone_number
        contact.email = body.email
        contact.birthdate = body.birthdate
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Remove a contact for a user.

    Args:
        contact_id (int): The ID of the contact to remove.
        user (User): The user for whom the contact belongs.
        db (Session): The database session.

    Returns:
        Contact | None: The removed Contact object, or None if the contact was not found.

    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact