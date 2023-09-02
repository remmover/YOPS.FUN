from fastapi import APIRouter, Depends, status, UploadFile, File, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.connect import get_db
from src.services.schemas import CommentCreate, CommentCreateResponse, CommentUpdateSchema
from src.conf import messages
from src.database.connect import get_db
from src.database.models import Comment
from src.conf.config import config

router = APIRouter()


@router.post("/comments/", response_model=CommentCreateResponse)
def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    pass


@router.get("/comments/", response_model=List[CommentCreateResponse])
def get_comments(db: Session = Depends(get_db)):
    pass


@router.put("/comments/{comment_id}/", response_model=CommentCreateResponse)
def update_comment(comment_id: int, comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    pass


@router.delete("/comments/{comment_id}/", response_model=CommentCreateResponse)
def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    pass