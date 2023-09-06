from datetime import datetime
from sqlalchemy import ( select
                       # , func
                       , and_
                       ,)
from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List


from src.database.models import Image, User
from src.schemas import ImageAboutUpdateSchema


async def image_create(image_url: str, small_image_url: str,
                       cloud_public_id: str, cloud_version: str,
                       user: User, db: AsyncSession) -> Image:
    '''
    Creates a new image for a specific user.

    :param image_url: Cloudinary url for the image to create.
    :type image_url: str
    :param small_image_url: cloudinary url for the small image to create.
                            It is useful for image navigation on the site
                            3D Tag Cloud.
    :type small_image_url: str
    :param asset_id: Asset ID in Cloudinary.
    :type asset_id: str
    :param user: The user to create the image item for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created image.
    :rtype: Image
    '''
    image = Image(image=image_url,
                  small_image=small_image_url,
                  cloud_public_id=cloud_public_id,
                  cloud_version=cloud_version,
                  user_id=user.id)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def image_about_update(body: ImageAboutUpdateSchema,
                             user: User, db: AsyncSession) -> Image:
    '''
    Updates 'about' description of image by ID for a specific image owner.

    :param body: Data for updating.
    :type body: ImageAboutUpdateSchema
    :param user: The user to create 'about' image description for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated image.
    :rtype: Image
    '''
    sq = select(Image).filter(and_(Image.id == body.image_id,
                                   Image.user_id == user.id))
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image:
        image.about = body.about
        image.updated_at = datetime.now()
        await db.commit()
    return image


# async def get_contacts(user: User, db: Session) -> List[Contact]:
#     '''
#     Retrieves a list of contacts for a specific user.

#     :param user: The user to retrieve contacts for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: A list of contacts.
#     :rtype: List[Contact]
#     '''
#     return db.query(Contact).filter(Contact.user_id == user.id).all()


# async def get_contact_id(contact_id: int, user: User, db: Session) -> Contact:
#     '''
#     Retrieves a single contact with the specified ID for a specific user.

#     :param contact_id: The ID of the contact to retrieve.
#     :type contact_id: int
#     :param user: The user to retrieve the contact for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: The contact with the specified ID, or None if it does not exist.
#     :rtype: Contact | None
#     '''
#     return db.query(Contact).filter(and_(Contact.user_id == user.id,
#                                          Contact.id == contact_id)).first()


# async def get_contact_name(contact_name: str,
#                            user: User, db: Session) -> List[Contact]:
#     '''
#     Retrieves a list of contact with the specified name for a specific user.

#     :param contact_name: The name of the contact to retrieve.
#     :type contact_name: str
#     :param user: The user to retrieve the contacts for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: A list of contacts with the specified name.
#     :rtype: List[Contact]
#     '''
#     return db.query(Contact).filter(and_(Contact.user_id == user.id,
#                 func.lower(Contact.name) == func.lower(contact_name))).all()


# async def get_contact_lastname(contact_lastname: str, user: User, db: Session) \
#             -> List[Contact]:
#     '''
#     Retrieves a list of contact with the specified lastname for a specific user.

#     :param contact_lastname: The lastname of the contact to retrieve.
#     :type contact_lastname: str
#     :param user: The user to retrieve the contacts for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: A list of contacts with the specified name.
#     :rtype: List[Contact]
#     '''
#     return db.query(Contact).filter(and_(Contact.user_id == user.id,
#                 func.lower(Contact.lastname) == func.lower(contact_lastname))).all()


# async def get_contact_email(contact_email: str, user: User, db: Session) \
#         -> Contact:
#     '''
#     Retrieves a single contact with the specified email for a specific user.

#     :param contact_email: The lastname of the contact to retrieve.
#     :type contact_email: str
#     :param user: The user to retrieve the contact for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: The contact with the specified email, or None if it does not exist.
#     :rtype: Contact
#     '''
#     return db.query(Contact).filter(and_(Contact.user_id == user.id,
#                 func.lower(Contact.email) == func.lower(contact_email))).first()


# async def get_contact_birthdays_along_week(user: User, db: Session) -> List[Contact]:
#     '''
#     Retrieves a list of contact with the birthday along week from the current date
#     for a specific user.

#     :param user: The user to retrieve the contacts for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: A list of contacts with the birthday which is matched to
#              the needed condition.
#     :rtype: List[Contact]
#     '''
#     contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
#     searched_contacts = []

#     today = date.today()
#     date_shift = timedelta(0)
#     today_over_week = today + timedelta(days=7)

#     # Period must be in the same year. Otherwise shift dates on 2 weeks
#     if today.year < today_over_week.year:
#         # The years in both dates must be the same
#         date_shift = timedelta(days=14)
#         today -= date_shift
#         today_over_week -= date_shift

#     # Searching appropriate birthdays
#     for contact in contacts:
#         bday = contact.birthday - date_shift

#         try:
#             bday = bday.replace(year=today.year)
#         except ValueError:
#             # Maybe shifted birthday on February, 29 -> March, 1
#             bday += timedelta(days=1)
#             bday = bday.replace(year=today.year)

#         if today <= bday < today_over_week:
#             searched_contacts.append(contact)
#     return searched_contacts


# async def update_contact(body: ContactModel, contact_id: int,
#                          user: User, db: Session) -> Contact | None:
#     '''
#     Updates a single contact with the specified ID for a specific user.

#     :param body: The updated data for the contact.
#     :type body: ContactModel
#     :param contact_id: The ID of the contact to update.
#     :type note_id: int
#     :param user: The user to update the contact for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: The updated contact, or None if it does not exist.
#     :rtype: Contact | None
#     '''
#     contact = db.query(Contact).filter(and_(Contact.user_id == user.id,
#                                             Contact.id == contact_id)).first()
#     if contact:
#         contact.name = body.name
#         contact.lastname = body.lastname
#         contact.email = body.email
#         contact.phone = body.phone
#         contact.birthday = body.birthday
#         contact.note = body.note
#         db.commit()
#     return contact


# async def delete_contact(contact_id: int, user: User, db: Session) -> Contact | None:
#     '''
#     Delete a single contact with the specified ID for a specific user.

#     :param note_id: The ID of the contact to delete.
#     :type note_id: int
#     :param user: The user to delete the contact for.
#     :type user: User
#     :param db: The database session.
#     :type db: Session
#     :return: The deleted contact, or None if it does not exist.
#     :rtype: Contact | None
#     '''
#     contact = db.query(Contact).filter(and_(Contact.user_id == user.id,
#                                             Contact.id == contact_id)).first()
#     if contact:
#         db.delete(contact)
#         db.commit()
#     return contact
