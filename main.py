from fastapi import FastAPI,File, UploadFile
from tools.uploadFiles import upload_video, upload_img
from routers.owner import ownerRouter

app = FastAPI()
IMAGEDIR= "images/"
VIDEODIR = "videos/"

app.include_router(ownerRouter)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/uploadImg/")
async def create_upload_img(file: UploadFile = File(...)):
    result = await upload_img(IMAGEDIR,file)
    return result
@app.post("/uploadVideo/")
async def create_upload_video(file: UploadFile = File(...)):
    result = await upload_video(VIDEODIR,file)
    return result




