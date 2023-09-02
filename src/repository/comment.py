from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Comment
from src.services.schemas import CommentCreateSchema, CommentResponseSchema, CommentUpdateSchema
from src.database.models import Comment


async def create_comment(db: AsyncSession, comment: CommentCreateSchema):
    pass


async def get_comments(db: AsyncSession, comment: CommentResponseSchema):


async def update_comment(db: AsyncSession, comment_id: int, comment: CommentUpdateSchema):
    pass


async def delete_comment(db: AsyncSession, comment_id: int):
    pass
