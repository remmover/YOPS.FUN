from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from src.database.models import Tag
from src.repository.admin import check_permission


async def tags_read(db: AsyncSession) -> List[Tag]:
    """
    Reads a tag list.
    """
    sq = select(Tag)
    print(f"sq: '{sq}'")
    result = await db.execute(sq)
    
    return result.fetchall()


@check_permission
async def tag_create(name: str, user, db: AsyncSession) -> Tag:
    """
    Create a new tag.
    """
    new_tag = Tag(name=name)
    db.add(new_tag)

    await db.commit()
    await db.refresh(new_tag)
    return new_tag
