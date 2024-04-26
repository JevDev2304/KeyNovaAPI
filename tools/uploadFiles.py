from fastapi import File, UploadFile
import uuid
from fastapi import HTTPException

async def upload_video(VIDEODIR , file :UploadFile = File(...), ):
    if file.filename.endswith(".mp4"):
        file.filename = f"{uuid.uuid4()}.mp4"
        contents = await file.read()

    # save the file
        with open(f"{VIDEODIR}{file.filename}", "wb") as f:
            f.write(contents)
        return {"filename": file.filename}
    else:
        raise HTTPException(status_code=400,
                            detail="invalid filetype . Please, upload an video filetype (.mp4).")

async def upload_img(IMGDIR , file :UploadFile = File(...), ):
    if file.filename.endswith(".jpg") or file.filename.endswith(".png") or file.filename.endswith(".jpeg"):
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
    else:
        raise HTTPException(status_code=400,
                            detail="invalid filetype . Please, upload an img filetype (.jpg, .jpeg or .png)")



    # save the file
    with open(f"{IMGDIR}{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}