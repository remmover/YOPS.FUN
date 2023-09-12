from fastapi import (
    APIRouter,
    Depends,
    # status, 
    # Request,
    # HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# from src.conf import messages
from src.database.connect import get_db
from src.database.models import User
from src.repository import tags as repository_tags
from src.services.auth import auth_service
from src.schemas import TagSchema, TagResponseSchema

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagResponseSchema])
async def tags_read(db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a list of the all tags.
    """
    response_list = []
    tags = await repository_tags.tags_read(db)
    for _, name in tags:
        print(f"[T] name='{name}'")
        response_list.append({'name': name})
    return response_list


@router.post("/", response_model=TagResponseSchema)
async def create_tag(
    body: TagSchema,
    # request: Request,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a tag.
    """
    tag = await repository_tags.create_tag(body, current_user, db)
    return tag
