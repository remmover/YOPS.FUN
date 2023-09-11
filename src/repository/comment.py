from datetime import datetime

from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Comment, Image, User
from src.repository.admin import (
    check_permission,
)
from src.schemas import CommentUpdateSchema


async def create_comment(
    text: str, user_id: User, image_id: Image, db: AsyncSession
) -> Comment:
    comment = Comment(
        comment=text,
        user_id=user_id,
        image_id=image_id,
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comments_for_image(image_id: int, db: AsyncSession):
    stmt = (
        select(Comment)
        .where(Comment.image_id == image_id)
        .order_by(desc(Comment.created_at))
    )
    results = await db.execute(stmt)
    comments = results.scalars().all()
    return comments


@check_permission
async def update_comment(body: CommentUpdateSchema, user: User, db: AsyncSession):
    sq = select(Comment).filter((Comment.id == body.comment_id))

    result = await db.execute(sq)
    comment = result.scalar_one_or_none()

    if comment:
        comment.comment = body.comment
        comment.updated_at = datetime.now()
        await db.commit()
    return comment


@check_permission
async def delete_comment(comment_id: int, user: User, db: AsyncSession):
    sq = select(Comment).filter(and_(Comment.id == comment_id))
    result = await db.execute(sq)
    comment = result.scalar_one_or_none()

    if comment:
        await db.delete(comment)
        await db.commit()
    return comment
