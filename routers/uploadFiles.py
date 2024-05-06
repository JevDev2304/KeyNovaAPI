from fastapi import APIRouter, status, HTTPException,File, UploadFile
from tools.uploadFiles import upload_video, upload_img

filesRouter = APIRouter(prefix="/uploadFiles", tags=["uploadFiles"])
IMAGEDIR= "/home/jevdev/PycharmProjects/Project1/static/images/"
VIDEODIR = "/home/jevdev/PycharmProjects/Project1/static/videos"
@filesRouter.post("/img")
async def create_upload_img(file: UploadFile = File(...)):
    result = await upload_img(IMAGEDIR,file)
    return result


@filesRouter.post("/video")
async def create_upload_video(file: UploadFile = File(...)):
    result = await upload_video(VIDEODIR,file)
    return result

