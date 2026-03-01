from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from cropper import crop_rectangle, crop_circle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.post("/crop/rectangle")
async def rectangle(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    w: int = Form(...),
    h: int = Form(...),
):
    image_bytes = await file.read()
    result = crop_rectangle(image_bytes, x, y, w, h)
    return StreamingResponse(result, media_type="image/jpeg")

@app.post("/crop/circle")
async def circle(
    file: UploadFile = File(...),
    cx: int = Form(...),
    cy: int = Form(...),
    radius: int = Form(...),
):
    image_bytes = await file.read()
    result = crop_circle(image_bytes, cx, cy, radius)
    return StreamingResponse(result, media_type="image/png")
