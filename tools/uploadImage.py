from fastapi import File, UploadFile, status
import uuid
from fastapi import HTTPException
import os
IMAGEDIR = "../static/images/"
current_dir = os.path.dirname(os.path.realpath(__file__))
ABSOLUTE_IMG_DIR = os.path.join(current_dir, IMAGEDIR)

async def upload_img(IMGDIR, file: UploadFile = File(...), ):
    if file.filename.endswith(".jpg") or file.filename.endswith(".png") or file.filename.endswith(".jpeg"):
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
    else:
        raise HTTPException(status_code=400,
                            detail="invalid filetype . Please, upload an img filetype (.jpg, .jpeg or .png)")

    with open(f"{IMGDIR}{file.filename}", "wb") as f:
        f.write(contents)
    return file.filename
def delete_image(image_path: str):
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Image not found")