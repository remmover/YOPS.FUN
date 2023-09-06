import cloudinary
import cloudinary.uploader
from fastapi import ( APIRouter
                    , Depends
                    , File
                    , HTTPException
                    # , status
                    , UploadFile
                    ,)
# from fastapi import Path
# from fastapi_limiter.depends import RateLimiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List


from src.conf.config import config
from src.database.connect import get_db
from src.database.models import User
from src.repository import images as repository_images
from src.schemas import ImageDb, ImageAboutUpdateSchema
from src.services.auth import auth_service


router = APIRouter(prefix='/images')


cloudinary.config(
    cloud_name=config.cloudinary_name,
    api_key=config.cloudinary_api_key,
    api_secret=config.cloudinary_api_secret,
    secure=True,
)


@router.post('/create', response_model=ImageDb)
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
    ufile = cloudinary.uploader.upload(file.file,
                                       public_id=f'ImageApp/{current_user.username}',
                                       overwrite=True)
    image_url = cloudinary.CloudinaryImage(f'ImageApp/{current_user.username}') \
                          .build_url(version=ufile.get('version'))
    small_image_url = cloudinary.CloudinaryImage(f'ImageApp/{current_user.username}') \
                                .build_url(width=config.small_image_size,
                                           height=config.small_image_size,
                                           crop='fill',
                                           version=ufile.get('version'))
    try:
        image = await repository_images.image_create(image_url, small_image_url,
                                                     current_user, db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Image already exists")
    return image


@router.post('/update', response_model=ImageDb)
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
        return image
    raise HTTPException(status_code=400, detail="None suitable image is.")


# @router.get("/", response_model=List[ResponseContactModel],
#             description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
# async def read_images(
#                 current_user: User = Depends(auth_service.get_current_user),
#                 db: Session = Depends(get_db)):
#     '''
#     Retrieves a list of images for the current user. Call of this
#     function is rate limited.

#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: List of images
#     :rtype: List[ResponseImageModel]
#     '''
#     images = await repository_images.get_images(current_user, db)
#     return images


# @router.get("/by_id/{image_id}", response_model=ResponseImageModel)
# async def read_image_id(image_id: int = Path(
#                     description="The ID of the image to get", ge=1),
#                 current_user: User = Depends(auth_service.get_current_user),
#                 db: Session = Depends(get_db)):
#     '''
#     Retrieves an image with specific ID for the current user.

#     :param image_id: ID of the image.
#     :type image_id: int
#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: Suitable image
#     :rtype: ResponseImageModel
#     :raises HTTPException: If aa image is absent for the current user, then
#                 exception with HTTP_404_NOT_FOUND status is raised.
#     '''
#     image = await repository_images.get_image_id(image_id, current_user, db)
#     if image is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='NOT FOUND')
#     return image


# @router.get("/by_name/{image_name}", response_model=List[ResponseImageModel])
# async def read_image_name(image_name: str = Path(
#                     description="The case insensitive name of the image to get"),
#                 current_user: User = Depends(auth_service.get_current_user),
#                 db: Session = Depends(get_db)):
#     '''
#     Retrieves a list of images for the current user with a specific image name.

#     :param image_name: Case insensitive image name.
#     :type image_name: str
#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: List of images
#     :rtype: List[ResponseImageModel]
#     '''
#     images = await repository_images.get_image_name(image_name,
#                                                     current_user, db)
#     return images


# @router.get("/by_period/{from_date}/{to_date}",
#             response_model=List[ResponseImageModel])
# async def read_image_period(
#                 from_date,
#                 to_date,
#                 current_user: User = Depends(auth_service.get_current_user),
#                 db: Session = Depends(get_db)):
#     '''
#     Retrieves a list of images for the current user with birtdays which
#     are happened during near 7 days.

#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: List of images
#     :rtype: List[ResponseImageModel]
#     '''
#     images = await repository_images.get_image_period(from_date, to_date,
#                 current_user, db)
#     return contacts


# @router.post("/", response_model=ResponseImageModel,
#              status_code=status.HTTP_201_CREATED)
# async def create_image(
#                 body: ImageModel,
#                 current_user: User = Depends(auth_service.get_current_user),
#                 db: Session = Depends(get_db)):
#     '''
#     Creates new image for the current user.

#     :param body: Image data.
#     :type body: ImageModel
#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: image
#     :rtype: ResponseImageModel

#     :raises HTTPException:
#             This exception is raised when such image already exists.

#     | For example, use Postman POST request to
#       URL=.../images/ with the following JSON raw body to create
#       new image:
#     | {
#     |   "name": "Lara",
#     |   "lastname": "Craft",
#     |   "email": "LaraCraft@gmail.com",
#     |   "phone": "(304) 625-2000",
#     |   "birthday": "2001-11-27",
#     |   "note": "The game must be continued."
#     | }
#     '''
#     try:
#         image = await repository_images.create_image(body, current_user, db)
#     except IntegrityError:
#         raise HTTPException(status_code=400, detail="ALREADY EXISTS")
#     return image


# @router.put("/{image_id}", response_model=ResponseImageModel)
# async def update_image(body: ImageModel, image_id: int = Path(ge=1),
#                          current_user: User = Depends(auth_service.get_current_user),
#                          db: Session = Depends(get_db)):
#     '''
#     Updates an existent image for the current user.

#     :param body: New image data.
#     :type body: ImageModel
#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: image
#     :rtype: ResponseImageModel

#     :raises HTTPException:
#             This exception is raised when image data already exists
#             for the other image or image is absent.
#     '''
#     try:
#         image = await repository_images.update_image(body,
#                                                      image_id, current_user, db)
#     except IntegrityError:
#         raise HTTPException(status_code=400, detail="ALREADY EXISTS")
#     if image is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="NOT FOUND",
#         )
#     return image


# @router.delete("/{image_id}", response_model=ResponseImageModel)
# async def delete_image(image_id: int = Path(
#                 description="The ID of image to delete", ge=1),
#             current_user: User = Depends(auth_service.get_current_user),
#             db: Session = Depends(get_db)):
#     '''
#     Deletes an existent image with a specific ID for the current user.

#     :param image_id: The ID of image to delete.
#     :type image_id: int
#     :param current_user: Current user.
#     :type current_user: User
#     :param db: The database session.
#     :type db: Session
#     :return: image
#     :rtype: ResponseImageModel

#     :raises HTTPException:
#             This exception is raised when image is absent.
#     '''
#     image = await repository_images.delete_image(image_id, current_user, db)
#     if image is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="NOT FOUND",
#         )
#     return image
