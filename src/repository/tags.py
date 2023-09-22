from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from src.database.models import Tag


async def tags_read(db: AsyncSession) -> List[Tag]:
    """
    Reads a tag list.
    """
    sq = select(Tag)
    result = await db.execute(sq)
    return result.all()


async def tag_create(tag_name: str, db: AsyncSession) -> Tag|None:
    """
    Create a new tag.
    """
    sq = select(Tag).filter(func.lower(Tag.name) == func.lower(tag_name))
    result = await db.execute(sq)
    tag = result.scalar_one_or_none()

    if tag:
        return None

    new_tag = Tag(name=tag_name)
    db.add(new_tag)

    await db.commit()
    await db.refresh(new_tag)
    return new_tag


async def tag_delete(tag_name: str, db: AsyncSession) -> Tag | None:
    """
    Delete tag with a specified name.
    """
    sq = select(Tag).filter(func.lower(Tag.name) == func.lower(tag_name))
    result = await db.execute(sq)
    tag = result.scalar_one_or_none()

    if tag:
        # Delete suitable tag
        await db.delete(tag)
        await db.commit()
    return tag
