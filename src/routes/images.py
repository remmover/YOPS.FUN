import cloudinary
import cloudinary.uploader

from datetime import date
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    status,
    UploadFile,
)
from fastapi import Path
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.conf.config import config
from src.database.connect import get_db
from src.database.models import User, Image
from src.repository import images as repository_images
from src.schemas import ImageDb

from src.schemas import (
    ImageAboutUpdateSchema,
    ImageAboutUpdateResponseSchema,
    ReturnMessageResponseSchema,
    SmallImageReadResponseSchema,
)

from src.services.auth import auth_service


router = APIRouter(prefix="/images", tags=["images"])


cloudinary.config(
    cloud_name=config.cloudinary_name,
    api_key=config.cloudinary_api_key,
    api_secret=config.cloudinary_api_secret,
    secure=True,
)


@router.post("/", response_model=ImageDb)
async def image_create(
    file: UploadFile = File(),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
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
    """
    cloud = cloudinary.uploader.upload(file.file, overwrite=True)
    # print(f"[u] version={cloud.get('version')}, public_id={cloud.get('public_id')}")
    cloud_public_id = cloud.get("public_id")
    cloud_version = cloud.get("version")
    image_url = cloudinary.CloudinaryImage(cloud_public_id).build_url(
        version=cloud_version
    )
    small_image_url = cloudinary.CloudinaryImage(cloud_public_id).build_url(
        width=config.small_image_size,
        height=config.small_image_size,
        crop="fill",
        version=cloud_version,
    )
    try:
        image = await repository_images.image_create(
            image_url, small_image_url, cloud_public_id, cloud_version, current_user, db
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Image already exists")
    return image


@router.put("/", response_model=ImageAboutUpdateResponseSchema)
async def image_about_update(
    body: ImageAboutUpdateSchema,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
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
    """
    image = await repository_images.image_about_update(body, current_user, db)
    if image:
        return {
            "image_id": image.id,
            "message": "Image description is successfully changed.",
        }
    raise HTTPException(status_code=400, detail="None suitable image is.")


@router.delete("/{image_id}", response_model=ReturnMessageResponseSchema)
async def image_delete(
    image_id: int = Path(description="The ID of image to delete", ge=1),
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
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
    """
    image: Image = await repository_images.image_delete(image_id, current_user, db)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image is absent.",
        )
    # print(f"[d] public_id={image.cloud_public_id} to delete")
    # Destroy image in cloudinary too
    cloudinary.uploader.destroy(image.cloud_public_id)
    return {"message": f"Image with ID {image_id} is successfully deleted."}


def shortent(about: str) -> str:
    if len(about) > 48:
        about = about[:48] + "…"
    return about


@router.get(
    "/{search:path}",
    response_model=List[SmallImageReadResponseSchema],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def images_read(
    search: str,
    current_user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieves a list of images which are corresponded to search filter. Call of this
    function is rate limited.

    :param current_user: Current user.
    :type current_user: User
    :param db: The database session.
    :type db: Session
    :return: List of images
    :rtype: List[SmallImageReadResponseSchema]

    Searches images into database which is identified by AsyncSession db.

    Searching can be made by the following criterias:
    |1. Username, like "Roy Bebru".
    |2. Creation period from specific date during specific days.
    |3. Tag list up to 5 items.
    |4. AND-combination of the criterias above.

    Examples:

    Get images with case insensitive username 'roy rebru' which are created
    from 2023-08-24 (-5 days) up to 2023-08-29 and each image contains tags
    'awesome', 'sun', 'world', 'ясно' simultaneously:
    |http://todo.yops.fun:8000/api/images/roy bebru/2023-08-29/-5/awesome/sun/world/ясно
    search="Roy Bebru/2023-08-29/-5/awesome/sun/world/ясно"

    Get all images:
    |http://todo.yops.fun:8000/api/images
    """
    username = None
    from_date = None
    days = None
    tags = []
    ind = 0

    search_args = search.split("/")

    if search_args[0] == "":
        ind += 1
    if len(search_args) > ind:
        if len(search_args[ind]):
            if search_args[ind].startswith("@"):
                username = search_args[ind][1:]
                ind += 1
            elif not search_args[ind][0].isdigit() and not search_args[ind][
                0
            ].startswith("-"):
                username = search_args[ind]
                ind += 1
        else:
            ind += 1  # skip empty

    if len(search_args) > ind:
        try:
            from_date = date.fromisoformat(search_args[ind])
            ind += 1
        except ValueError:
            pass

    if len(search_args) > ind:
        try:
            days = int(search_args[ind])
            ind += 1
        except ValueError:
            pass

    tags = search_args[ind:]
    if from_date is None and days is None and username:
        # search contains only tags (like "awesome/sun/world/ясно")
        tags.insert(0, username)
        username = None

    records = await repository_images.image_search(
        username, from_date, days, tags, current_user, db
    )
    return [
        {"image_id": id, "small_image_url": small_image, "short_about": shortent(about)}
        for id, small_image, about in records
    ]
