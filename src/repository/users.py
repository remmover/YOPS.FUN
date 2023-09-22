import logging

from libgravatar import Gravatar
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.models import User
from src.schemas import UserSchema


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Retrieves an user with the unique specific email address.
    Email is searched in case insensitive way. For example, emails
    hero@example.com, Hero@example.com, HERO@EXAMPLE.COM, etc,
    are the same.

    :param email: The email address to retrieve user for.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: An user which is identified by email address.
    :rtype: User
    """
    sq = select(User).filter(func.lower(User.email) == func.lower(email))
    result = await db.execute(sq)
    user = result.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession) -> User:
    """
    Create a new user.

    :param body: UserSchema object containing user information.
    :param db: AsyncSession instance for database operations.
    :return: The newly created user object.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)

    num_users = await db.execute(select(func.count(User.id)))
    num_users = num_users.scalar()

    if num_users == 0:
        new_user.role = "admin"

    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
    Update the refresh token for a user.

    :param user: User object for whom to update the token.
    :param token: New refresh token value or None.
    :param db: AsyncSession instance for database operations.
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Mark a user's email as confirmed.

    :param email: Email address of the user to mark as confirmed.
    :param db: AsyncSession instance for database operations.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
    Update a user's avatar URL.

    :param email: Email address of the user whose avatar to update.
    :param url: New avatar URL.
    :param db: AsyncSession instance for database operations.
    :return: The updated user object.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    return user


async def update_user_password(
    user: User, hashed_password: str, db: AsyncSession
) -> None:
    """
    Update a user's password.

    :param user: User object to update.
    :param hashed_password: New hashed password value.
    :param db: AsyncSession instance for database operations.
    """
    user.password = hashed_password
    await db.commit()
