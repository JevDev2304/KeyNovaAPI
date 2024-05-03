from fastapi import FastAPI,File, UploadFile
from tools.uploadFiles import upload_video, upload_img
from routers.owner import ownerRouter
from routers.agent import agentRouter
from routers.tenant import tenantRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI()
IMAGEDIR= "static/images"
VIDEODIR = "static/videos"

app.include_router(ownerRouter)
app.include_router(agentRouter)
app.include_router(tenantRouter)
app.mount("/static", StaticFiles(directory="static"), name = "static")

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




