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


async def image_delete(image_id: int, user: User, db: AsyncSession) -> Image | None:
    '''
    Delete a single image with the specified ID for a specific user.

    :param image_id: The ID of the image to delete.
    :type image_id: int
    :param user: The user to delete the image for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The deleted contact, or None if it does not exist.
    :rtype: Image | None
    '''
    sq = select(Image).filter(and_(Image.id == image_id,
                                   Image.user_id == user.id))
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image:
        await db.delete(image)
        await db.commit()
    return image
