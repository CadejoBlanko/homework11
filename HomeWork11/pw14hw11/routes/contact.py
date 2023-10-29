from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models import User
from schemas import Contact as ContactModel
from routes.auth import auth_service
from repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/")
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Get Contacts

    Retrieve a list of contacts for the authenticated user.

    Args:
        skip (int, optional): Number of items to skip. Defaults to 0.
        limit (int, optional): Maximum number of items to retrieve. Defaults to 100.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        List[ContactModel]: List of contact models.

    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}")
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Get Contact by ID

    Retrieve a specific contact by its ID.

    Args:
        contact_id (int): The ID of the contact to retrieve.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ContactModel: The requested contact model.

    Raises:
        HTTPException: If the contact is not found.

    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/")
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Create Contact

    Create a new contact for the authenticated user.

    Args:
        body (ContactModel): Contact details.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ContactModel: The created contact model.

    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}")
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Update Contact

    Update an existing contact for the authenticated user.

    Args:
        contact_id (int): The ID of the contact to update.
        body (ContactModel): New contact details.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ContactModel: The updated contact model.

    Raises:
        HTTPException: If the contact is not found.

    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}")
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Remove Contact

    Remove an existing contact for the authenticated user.

    Args:
        contact_id (int): The ID of the contact to remove.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        ContactModel: The removed contact model.

    Raises:
        HTTPException: If the contact is not found.

    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact