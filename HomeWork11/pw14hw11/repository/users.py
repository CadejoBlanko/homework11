from libgravatar import Gravatar
from sqlalchemy.orm import Session

from models import User
from schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user.
        db (Session): The database session.

    Returns:
        User: The User object if found, otherwise None.

    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user.

    Args:
        body (UserModel): The user information.
        db (Session): The database session.

    Returns:
        User: The created User object.

    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update the refresh token for a user.

    Args:
        user (User): The user object.
        token (str | None): The new refresh token, or None to clear the token.
        db (Session): The database session.

    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Mark a user's email as confirmed.

    Args:
        email (str): The email address to confirm.
        db (Session): The database session.

    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()