from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect import get_db
from src.database.models import Comment, Image, User
from src.schemas import (
    CommentCreateSchema,
    ReturnMessageResponseSchema,
    CommentDb,
    CommentShowAllSchema,
    CommentUpdateSchema,
    CommentDeleteSchema,
)
from src.services.auth import auth_service
from src.repository import comment as repository_comment

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentDb)
async def create_comment_for_image(
    image_id: int,
    comment: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    image = await db.get(Image, image_id)
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Image not found or doesn't belong to the current user",
        )

    new_comment = await repository_comment.create_comment(
        comment, current_user.id, image_id, db
    )
    return new_comment


@router.get("/images/{image_id}/comments/", response_model=CommentShowAllSchema)
async def get_comments_for_image(image_id: int, db: AsyncSession = Depends(get_db)):
    comments = await repository_comment.get_comments_for_image(image_id, db)
    if comments:
        return {"comments": comments}

    raise HTTPException(
        status_code=404,
        detail="Comment not found or doesn't belong to the current user",
    )


@router.put("/", response_model=CommentUpdateSchema)
async def update_comment_for_image(
    body: CommentUpdateSchema,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_comment = await repository_comment.update_comment(body, current_user, db)

    if updated_comment:
        return {
            "comment_id": updated_comment.id,
            "image_id": updated_comment.image_id,
            "comment": updated_comment.comment,
            "message": "Comment description is successfully changed.",
        }

    raise HTTPException(
        status_code=404,
        detail="Comment not found or doesn't belong to the current user",
    )


@router.delete("/{comment_id}", response_model=ReturnMessageResponseSchema)
async def delete_comment_for_image(
    comment_id: int = Path(description="The ID of comment to delete", ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    deleted_comment = await repository_comment.delete_comment(
        comment_id, current_user, db
    )

    if deleted_comment:
        return {"message": f"Comment with ID {comment_id} is successfully deleted."}
    else:
        raise HTTPException(
            status_code=404,
            detail="Comment not found or doesn't belong to the current user",
        )
