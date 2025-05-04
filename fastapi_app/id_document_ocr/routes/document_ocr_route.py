import os
import uuid
import httpx
import asyncio
import easyocr
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from services.document_ocr_service import easyocr_fulltext, best_rotation, enhance, read_image_bytes

router = APIRouter()
reader = easyocr.Reader(['en'], gpu=False)

X_WEBHOOK_TOKEN = os.environ.get("X_WEBHOOK_TOKEN", "")
DJANGO_WEBHOOK_URL = "http://django_app:8000/accounts/webhook/"

if not X_WEBHOOK_TOKEN:
    raise ValueError("X_WEBHOOK_TOKEN environment variable is not set.")

@router.post("/upload-rg/")
async def upload_rg(
    rg_front: UploadFile = File(...),
    rg_back: UploadFile = File(...)
):
    task_id = str(uuid.uuid4())

    # Lê os arquivos ANTES de iniciar a task
    front_bytes = await rg_front.read()
    back_bytes = await rg_back.read()

    async def process_and_callback():
        try:
            from services.document_ocr_service import read_image_bytes

            img_front, img_back = await asyncio.gather(
                read_image_bytes(front_bytes),
                read_image_bytes(back_bytes)
            )

            async def process(img):
                rotated = await best_rotation(img, reader)
                enhanced = await enhance(rotated)
                return await easyocr_fulltext(enhanced, reader)

            text_front, text_back = await asyncio.gather(
                process(img_front),
                process(img_back)
            )

            result = {
                "task_id": task_id,
                "rg_front": text_front,
                "rg_back": text_back,
            }

            print(f"Task {task_id} completed successfully.")
            
            async with httpx.AsyncClient() as client:
                await client.post(
                    DJANGO_WEBHOOK_URL,
                    headers={"Host": "localhost", "X-WEBHOOK-TOKEN": X_WEBHOOK_TOKEN},
                    json=result,
                    timeout=60
                )

        except Exception as e:
            async with httpx.AsyncClient() as client:
                await client.post(
                    DJANGO_WEBHOOK_URL,
                    headers={"Host": "localhost", "X-WEBHOOK-TOKEN": X_WEBHOOK_TOKEN},
                    json={"task_id": task_id, "error": str(e)},
                    timeout=60
                )

    asyncio.create_task(process_and_callback())
    return JSONResponse({"task_id": task_id})

