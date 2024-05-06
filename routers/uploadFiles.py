from fastapi import APIRouter, status, HTTPException,File, UploadFile
from tools.uploadFiles import upload_video, upload_img
import os

filesRouter = APIRouter(prefix="/uploadFiles", tags=["uploadFiles"])
IMAGEDIR = "../static/images/"
VIDEODIR = "../static/videos/"
current_dir = os.path.dirname(os.path.realpath(__file__))

# Combina las rutas relativas con el directorio actual para obtener las rutas absolutas
absolute_imagedir = os.path.join(current_dir, IMAGEDIR)
absolute_videodir = os.path.join(current_dir, VIDEODIR)

@filesRouter.post("/img")
async def create_upload_img(file: UploadFile = File(...)):
    result = await upload_img(absolute_imagedir,file)
    return result


@filesRouter.post("/video")
async def create_upload_video(file: UploadFile = File(...)):
    result = await upload_video(absolute_videodir,file)
    return result

