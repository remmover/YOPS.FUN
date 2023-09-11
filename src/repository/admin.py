from functools import wraps
from typing import Callable
from datetime import datetime, date, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import ImageAboutUpdateSchema,CommentUpdateSchema
from src.database.models import User, Image, Role,Comment



# IMAGETS [START]
def check_permission_delete_image(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(image_id: int, user: User, db: AsyncSession) -> Image | None:
        if user.role == Role.admin:
            return await func(image_id, user, db)

        sq = select(Image).filter(
            and_(
                Image.id == image_id,
                Image.user_id == user.id,
            )
        )
        result = await db.execute(sq)
        image = result.scalar_one_or_none()

        if image:
            return await func(image_id, user, db)
        else:
            return None

    return wrapper





def check_permission_for_image_about_update(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(body: ImageAboutUpdateSchema, user: User, db: AsyncSession) -> Image:
        if user.role == Role.admin:
            return await func(body, user, db)

        sq = select(Image).filter(and_(Image.id == body.image_id, Image.user_id == user.id))
        result = await db.execute(sq)
        image = result.scalar_one_or_none()

        if image:
            image.about = body.about
            image.updated_at = datetime.now()
            await db.commit()
            return image

    return wrapper


# # IMAGES [END]


# # COMMENTS [START]

def check_permission_for_delete_comment(func):
    @wraps(func)
    async def wrapper(comment_id: int, user: User, db: AsyncSession):
        if user.role == Role.admin:
            return await func(comment_id, user, db)

        sq = select(Comment).filter(
            (Comment.id == comment_id) & (Comment.user_id == user.id)
        )
        result = await db.execute(sq)
        comment = result.scalar_one_or_none()

        if comment:
            await db.delete(comment)
            await db.commit()
        return comment

    return wrapper




def check_permission_for_update_comment(func: Callable):
    @wraps(func)
    async def wrapper(body: CommentUpdateSchema, user: User, db: AsyncSession):
        if user.role == Role.admin:
            return await func(body, user, db)

        sq = select(Comment).filter(
            (Comment.id == body.comment_id) & (Comment.user_id == user.id)
        )
        result = await db.execute(sq)
        comment = result.scalar_one_or_none()

        if comment:
            comment.comment = body.comment
            comment.updated_at = datetime.now()
            await db.commit()
        return comment

    return wrapper