from datetime import datetime, date, timedelta
from fastapi import status
from sqlalchemy import (
    select,
    delete,
    insert,
    text,
    func,
    and_,
    or_,
)

from sqlalchemy.ext.asyncio import AsyncSession


from src.database.models import Image, Comment, tag_m2m_image, Tag, User, Role
from src.schemas import ImageAboutUpdateSchema
# from src.repository.admin import (check_permission,)


async def image_create(
    image_url: str,
    small_image_url: str,
    cloud_public_id: str,
    cloud_version: str,
    user: User,
    db: AsyncSession,
) -> Image:
    """
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
    """
    image = Image(
        image=image_url,
        small_image=small_image_url,
        cloud_public_id=cloud_public_id,
        cloud_version=cloud_version,
        user_id=user.id,
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def image_about_update(
    body: ImageAboutUpdateSchema, user: User, db: AsyncSession
) -> Image:
    """
    Updates 'about' description of image by ID for a specific image owner.

    :param body: Data for updating.
    :type body: ImageAboutUpdateSchema
    :param user: The user to create 'about' image description for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated image.
    :rtype: Image
    """
    sq = select(Image).filter(and_(Image.id == body.image_id,
                                   or_(user.role == Role.admin,
                                       user.role == Role.moder,
                                       Image.user_id == user.id)))
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image:
        image.about = body.about
        image.updated_at = datetime.now()
        await db.commit()
    return image


async def image_add_tag(
    image_id: int, tag_name: str, user: User, db: AsyncSession
):
    """
    Add tag to image for a specific owner.
    """
    sq = select(Image).filter(and_(Image.id == image_id,
                                   or_(user.role == Role.admin,
                                       user.role == Role.moder,
                                       Image.user_id == user.id)))
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image is None:
        return (status.HTTP_404_NOT_FOUND, "Image is not accessible.")

    sq = select(Tag).filter(func.lower(Tag.name) == func.lower(tag_name))
    result = await db.execute(sq)
    await db.commit()
    tag = result.first()

    if tag is None:
        return (status.HTTP_404_NOT_FOUND, "Tag is not exists.")

    tag = tag[0]
    # print(f"   [D] tag: {tag.id}, {tag.name}")
    sq = select(tag_m2m_image).where(tag_m2m_image.c.image_id == image.id)
    result = await db.execute(sq)
    await db.commit()
    tags = result.all()
    # print(f"    [D] tags='{tags}'")
    # output: [(5, 9, 7), (6, 9, 3), (7, 9, 4), (8, 9, 8)]

    for tg in tags:
        if tg[2] == tag.id:
            return (status.HTTP_409_CONFLICT, "Already exists.")

    if len(tags) >= 5:
        return (status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                "More than 5 tags are not allowed.")

    sq = insert(tag_m2m_image).values(image_id=image.id, tag_id=tag.id)
    # print(f"    [D] sq='{sq}'")
    await db.execute(sq)
    await db.commit()
    tag_ids = [tg[2] for tg in tags]
    tag_ids.append(tag.id)
    sq = select(Tag).filter(Tag.id.in_(tag_ids))
    print(f"    [D2] sq='{sq}'")
    result = await db.execute(sq)
    await db.commit()
    tags = result.all()
    # print(f"    [D3] tags='{tags}'")
    return (0, [tg[0].name for tg in tags])


async def image_remove_tag(image_id: int, tag_name: str,
                           user: User, db: AsyncSession
):
    """
    Removes tag from image for a specific owner.
    """
    sq = select(Image).filter(and_(Image.id == image_id,
                                   or_(user.role == Role.admin,
                                       user.role == Role.moder,
                                       Image.user_id == user.id)))
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image is None:
        return (status.HTTP_404_NOT_FOUND, "Image is not accessible.")

    sq = select(Tag).filter(func.lower(Tag.name) == func.lower(tag_name))
    result = await db.execute(sq)
    await db.commit()
    tag = result.first()
    if tag is None:
        return (status.HTTP_404_NOT_FOUND, "Tag is not exists.")
    tag = tag[0]
    # print(f"   [D] tag='{tag}'")

    sq = delete(tag_m2m_image).where(and_(tag_m2m_image.c.image_id == image.id,
                                          tag_m2m_image.c.tag_id == tag.id)) \
                              .returning(tag_m2m_image.c.id)
    # print(f"   [D] sq='{sq}'")
    result = await db.execute(sq)
    await db.commit()

    affected_list = result.all()
    if len(affected_list) == 0: # 0 rows are deleted
        return (status.HTTP_418_IM_A_TEAPOT, "Tag is absent for this image.")

    return (0, "Tag successfully removed.")


async def image_delete(image_id: int, user: User, db: AsyncSession) -> Image | None:
    """
    Delete a single image with the specified ID for a specific user.

    :param image_id: The ID of the image to delete.
    :type image_id: int
    :param user: The user to delete the image for.
    :type user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The deleted contact, or None if it does not exist.
    :rtype: Image | None
    """
    sq = select(Image).filter(and_(Image.id == image_id,
                                   or_(user.role == Role.admin,
                                       user.role == Role.moder,
                                       Image.user_id == user.id)))
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image:
        # Delete comment for suitable image
        sq = delete(Comment).where(Comment.image_id == image.id)
        await db.execute(sq)
        # Delete suitable image
        await db.delete(image)
        await db.commit()
    return image


async def image_read(id: int, db: AsyncSession) -> Image:
    sq = select(Image).filter(Image.id == id)
    result = await db.execute(sq)
    image = result.scalar_one_or_none()
    return image


async def image_search(
    username: str,
    from_date: date | None,
    days: int | None,
    tags: list,
    db: AsyncSession,
) -> list:
    """
    Searches images into database which is identified by AsyncSession db.

    Searching can be made by the following criterias:
    1. Username, like "Roy Bebru".
    2. Creation period from specific date during specific days.
    3. Tag list up to 5 items.
    4. AND-combination of the criterias above.
    """
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
        sq_between_date = (
            ":from_date <= im.created_at " "AND im.created_at < :to_date AND "
        )
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
        sq = text(
            f"""
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
        """
        )
    elif sq_username_join or sq_between_date:
        sq = text(
            f"""
            SELECT {only_fields}
            FROM images im
            {sq_username_join}
            WHERE {sq_username_where}{sq_between_date}True
        """
        )
    else:
        sq = text(
            f"""
            SELECT {only_fields}
            FROM images im
        """
        )
    # print(sq, str(from_date), str(days), str(to_date))

    for i in range(tags_amount, 5):
        tags.append("")

    # Execute the select query asynchronously and fetch the results
    result = await db.execute(
        sq,
        {
            "username": username,
            "from_date": from_date,
            "to_date": to_date,
            "tags_amount": tags_amount,
            "tag1": tags[0],
            "tag2": tags[1],
            "tag3": tags[2],
            "tag4": tags[3],
            "tag5": tags[4],
        },
    )
    images = result.fetchall()

    # for im in images:
    #     print(im)

    return images


async def image_exists(image_id: int, user: User, db: AsyncSession) -> Image:
    sq = select(Image).filter(
        and_(
            Image.id == image_id,
            Image.user_id == user.id,
        )
    )
    result = await db.execute(sq)
    image = result.scalar_one_or_none()
    return image


async def update_image_url(
    image_id: int, crop_image_url, user: User, db: AsyncSession
) -> Image:
    sq = select(Image).filter(
        and_(
            Image.id == image_id,
            Image.user_id == user.id,
        )
    )
    result = await db.execute(sq)
    image = result.scalar_one_or_none()

    if image:
        image.image = crop_image_url
        image.updated_at = datetime.now()
        await db.commit()
    return image
