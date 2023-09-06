import cloudinary
import cloudinary.uploader
from fastapi import ( APIRouter
                    , Depends
                    , File
                    , HTTPException
                    , status
                    , UploadFile
                    ,)
from fastapi import Path
# from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List


from src.conf.config import config
from src.database.connect import get_db
from src.database.models import User, Image
from src.repository import images as repository_images
from src.schemas import ImageDb
from src.schemas import ( ImageAboutUpdateSchema, ImageAboutUpdateResponseSchema
                        , ReturnMessageResponseSchema
                        ,)
from src.services.auth import auth_service


router = APIRouter(prefix='/images')


cloudinary.config(
    cloud_name=config.cloudinary_name,
    api_key=config.cloudinary_api_key,
    api_secret=config.cloudinary_api_secret,
    secure=True,
)


@router.post('/', response_model=ImageDb)
async def image_create(file: UploadFile = File(),
                       current_user: User = Depends(auth_service.get_current_user),
                       db: AsyncSession = Depends(get_db)):
    '''
    Creates new image by current user in aim to comment it.

    :param file: An image file to upload.
    :type file: UploadFile
    :param current_user: Current user.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: New image record.
    :rtype: ImageDb
    :raises HTTPException:
            This exception is raised when such image already exists.
    '''
    cloud = cloudinary.uploader.upload(file.file,
                                       overwrite=True)
    # print(f"[u] version={cloud.get('version')}, public_id={cloud.get('public_id')}")
    cloud_public_id = cloud.get('public_id')
    cloud_version = cloud.get('version')
    image_url = cloudinary.CloudinaryImage(cloud_public_id) \
                          .build_url(version=cloud_version)
    small_image_url = cloudinary.CloudinaryImage(cloud_public_id) \
                                .build_url(width=config.small_image_size,
                                           height=config.small_image_size,
                                           crop='fill',
                                           version=cloud_version)
    try:
        image = await repository_images.image_create(image_url, small_image_url,
                                                     cloud_public_id, cloud_version,
                                                     current_user, db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Image already exists')
    return image


@router.put('/', response_model=ImageAboutUpdateResponseSchema)
async def image_about_update(
            body: ImageAboutUpdateSchema,
            current_user: User = Depends(auth_service.get_current_user),
            db: AsyncSession = Depends(get_db)):
    '''
    Updates 'about' description of image by ID for a current image owner.

    :param body: Data for updating.
    :type body: ImageAboutUpdateSchema
    :param current_user: The user to create 'about' image description for.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated image.
    :rtype: ImageDb
    :raises HTTPException:
            This exception is raised when absent image with ID or
            image owner is different from current user.
    '''
    image = await repository_images.image_about_update(body,
                                                       current_user, db)
    if image:
        return { 'image_id': image.id,
                 'message': 'Image description is successfully changed.'}
    raise HTTPException(status_code=400, detail='None suitable image is.')


@router.delete("/{image_id}", response_model=ReturnMessageResponseSchema)
async def image_delete(
            image_id: int = Path(
                description="The ID of image to delete", ge=1),
            current_user: User = Depends(auth_service.get_current_user),
            db: AsyncSession = Depends(get_db)):
    '''
    Deletes an existent image with a specific ID for the current owner.

    :param image_id: The ID of image to delete.
    :type image_id: int
    :param current_user: Current user which must be image owner.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: image
    :rtype: ReturnMessageResponseSchema
    :raises HTTPException:
            This exception is raised when image is absent.
    '''
    image: Image = await repository_images.image_delete(image_id, current_user, db)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image is absent.",
        )
    # print(f"[d] public_id={image.cloud_public_id} to delete")
    # Destroy image in cloudinary too
    cloudinary.uploader.destroy(image.cloud_public_id)
    return { "message": f"Image with ID {image_id} is successfully deleted." }
