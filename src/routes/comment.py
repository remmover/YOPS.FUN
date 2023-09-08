from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.connect import get_db
from src.database.models import Comment, Image, User
from src.schemas import CommentCreateSchema, CommentResponseSchema, ReturnMessageResponseSchema
from src.services.auth import auth_service
from src.repository.comment import create_comment, get_comments_for_image, update_comment, delete_comment

router = APIRouter(prefix='/comments', tags=["comments"])


@router.post("/images/{image_id}/", response_model=CommentResponseSchema)
async def create_comment_for_image(
        image_id: int, comment: CommentCreateSchema, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    sq = select(Image).filter(Image.id == image_id, Image.user_id == current_user.id)
    result = await db.execute(sq)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found or doesn't belong to the current user")

    new_comment = create_comment(db, comment.text, current_user.id, image_id)
    return new_comment


@router.get("/images/{image_id}/", response_model=list[CommentResponseSchema])
def get_comments_for_image(image_id: int, db: AsyncSession = Depends(get_db)):
    image = db.select(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    comments = get_comments_for_image(db, image_id)
    return comments


@router.put("/{comment_id}/", response_model=CommentResponseSchema)
def update_comment_for_user(
        comment_id: int, comment_update: CommentCreateSchema, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or doesn't belong to the current user")

    updated_comment = update_comment(db, comment_id, comment_update.text)
    return updated_comment


@router.delete("/{comment_id}/", response_model=ReturnMessageResponseSchema)
def delete_comment_for_user(
        comment_id: int, db: AsyncSession = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or doesn't belong to the current user")

    delete_comment(db, comment_id)
    return {"message": "Comment deleted"}
