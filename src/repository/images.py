from datetime import datetime, date, timedelta
from sqlalchemy import ( select
                       , text 
                       # , func
                       # , distinct
                       , and_
                       ,)
from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List


from src.database.models import ( Image
                                # , tag_m2m_image
                                # , Tag
                                , User
                                ,)
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


async def image_read(id: int, db: AsyncSession) -> Image:
    sq = select(Image).filter(Image.id == id)
    result = await db.execute(sq)
    image = result.scalar_one_or_none()
    return image


async def image_search(
        username: str, from_date: date|None, days: int|None, tags: list,
        db: AsyncSession) -> list:
    '''
    Searches images into database which is identified by AsyncSession db.

    Searching can be made by the following criterias:
    1. Username, like "Roy Bebru".
    2. Creation period from specific date during specific days.
    3. Tag list up to 5 items.
    4. AND-combination of the criterias above.     
    '''
    sq_username_join = ""
    sq_username_where = ""
    sq_between_date = ""
    if username:
        sq_username_join = "INNER JOIN users us ON us.id = im.user_id"
        sq_username_where = "us.username ILIKE :username AND "
    to_date = None
    if isinstance(days, int) and from_date is None:
        from_date = date.today()
    if from_date:
        sq_between_date = ":from_date <= im.created_at " \
                          "AND im.created_at < :to_date AND "
        if isinstance(days, int):
            if days < 0:
                to_date = date.today() + timedelta(days=days)
                if from_date > to_date:
                    from_date, to_date = to_date, from_date
            else:
                to_date = from_date + timedelta(days=days)
        else:
            to_date = from_date + timedelta(days=1)
    tags_amount = len(tags)
    ## list of searched fields ##
    only_fields = "im.id, im.small_image, im.about"
    ##
    if tags_amount:
        sq = text(f"""
            SELECT DISTINCT ON (im.id) {only_fields}
            FROM tag_m2m_image ti
            INNER JOIN images im ON im.id = ti.image_id
            {sq_username_join}
            WHERE {sq_username_where}{sq_between_date}(
                SELECT count(*)
                FROM tag_m2m_image ti2
                WHERE ti2.image_id = ti.image_id AND ti2.tag_id IN (
                    SELECT tg.id
                    FROM tags tg
                    WHERE tg.name IN (:tag1, :tag2, :tag3, :tag4, :tag5)
                )
            ) >= :tags_amount
        """)
    elif sq_username_join or sq_between_date:
        sq = text(f"""
            SELECT {only_fields}
            FROM images im
            {sq_username_join}
            WHERE {sq_username_where}{sq_between_date}True
        """)
    else:
        sq = text(f"""
            SELECT {only_fields}
            FROM images im
        """)
    # print(sq, str(from_date), str(days), str(to_date))

    for i in range(tags_amount, 5):
        tags.append('')

    # Execute the select query asynchronously and fetch the results
    result = await db.execute(sq, {
        'username': username,
        'from_date': from_date,
        'to_date': to_date,
        'tags_amount': tags_amount,
        'tag1': tags[0],
        'tag2': tags[1],
        'tag3': tags[2],
        'tag4': tags[3],
        'tag5': tags[4],
    })
    images = result.fetchall()

    # for im in images:
    #     print(im)

    return images
