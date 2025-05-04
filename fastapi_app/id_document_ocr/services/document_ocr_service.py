import cv2
import easyocr
import numpy as np
from PIL import Image
from io import BytesIO


async def best_rotation(img: np.ndarray, reader: easyocr.Reader) -> np.ndarray:
    candidates = {
        0:   img,
        90:  cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
        180: cv2.rotate(img, cv2.ROTATE_180),
        270: cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE),
    }
    best_img, best_score = img, -1
    
    for _, candidate in candidates.items():
        h, w = candidate.shape[:2]
        scale = 800 / max(h, w)                # OCR rápido num thumb
        thumb = cv2.resize(candidate, (int(w*scale), int(h*scale)),
                            interpolation=cv2.INTER_AREA) if scale < 1 else candidate
        score = sum(conf for *_, conf in reader.readtext(thumb, detail=1)) # type: ignore
        
        if score > best_score:
            best_img, best_score = candidate, score
            
    return best_img


async def enhance(img: np.ndarray, upscale: float = 1.5) -> np.ndarray:
    h, w = img.shape[:2]
    img  = cv2.resize(img, (int(w*upscale), int(h*upscale)),
                      interpolation=cv2.INTER_CUBIC)
    ycrcb      = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb  = cv2.split(ycrcb)
    clahe      = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    y_eq       = clahe.apply(y)
    img_eq     = cv2.merge((y_eq, cr, cb))
    
    return cv2.cvtColor(img_eq, cv2.COLOR_YCrCb2BGR)


async def easyocr_fulltext(img: np.ndarray, reader: easyocr.Reader) -> str:
    blocks = reader.readtext(img, detail=0, paragraph=True,
                             text_threshold=0.25, link_threshold=0.25,
                             low_text=0.25)
    
    if blocks and isinstance(blocks[0], list):
        blocks = [" ".join(b) for b in blocks]
        
    return "\n".join(blocks).strip() # type: ignore


async def read_image_bytes(file_bytes: bytes) -> np.ndarray:
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)