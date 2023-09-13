from fastapi import (
    APIRouter,
    Depends,
    status, 
    # Request,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# from src.conf import messages
from src.database.connect import get_db
from src.database.models import User, Role
from src.repository import tags as repository_tags
from src.services.auth import auth_service
from src.schemas import TagSchema, TagResponseSchema, ReadTagResponseSchema

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=ReadTagResponseSchema)
async def tags_read(db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a list of the all tags.
    """
    response_list = []
    tags = await repository_tags.tags_read(db)
    for tags in tags:
        response_list.append(tags[0].name)
    return { "tags": response_list }


@router.post("/", response_model=TagResponseSchema)
async def tag_create(
    body: TagSchema,
    # request: Request,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a tag.
    """
    tag = await repository_tags.tag_create(body.name, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag is already present.",
        )
    return tag


@router.delete("/{tag_name}")
async def tag_delete(
    tag_name: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    print(f"[D] current_user role: {current_user.role}")
    if current_user.role not in (Role.admin, Role.moder):
        return { 'deatil': "You have not enough permissions." }
    tag = await repository_tags.tag_delete(tag_name, db)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag is absent.",
        )
    return {"message": f"Tag '{tag_name}' is successfully deleted."}
