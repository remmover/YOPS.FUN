from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Comment


def create_comment(db: AsyncSession, text: str, user_id: int, image_id: int):
    new_comment = Comment(text=text, user_id=user_id, image_id=image_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comments_for_image(db: AsyncSession, image_id: int):
    comments = db.query(Comment).filter(Comment.image_id == image_id).all()


def update_comment(db: AsyncSession, comment_id: int, text: str):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None

    comment.text = text
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: AsyncSession, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None

    db.delete(comment)
    db.commit()
    return True
