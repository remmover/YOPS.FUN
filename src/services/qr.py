import os
from datetime import datetime, timedelta

import cloudinary
import qrcode
from fastapi import HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.repository.images import image_exists

scheduler = AsyncIOScheduler()


async def create_qr_code_and_upload(image_id, current_user, db):
    image = await image_exists(image_id, current_user, db)
    if image:
        image = image.image

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(image)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        qr_image.save(f"{image_id, current_user.username}")

        result = cloudinary.uploader.upload(f"{image_id, current_user.username}")
        # print(result["public_id"])
        os.remove(f"{image_id, current_user.username}")

        future_time = datetime.now() + timedelta(minutes=30)
        scheduler.add_job(
            delete_temp_qr_code,
            "date",
            run_date=future_time,
            args=[result["public_id"]],
        )

        return result["secure_url"]
    raise HTTPException(status_code=400, detail="Image doesn't exist")


async def delete_temp_qr_code(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        print(f"Error while image deletion in Cloudinary: {e}")


scheduler.start()
