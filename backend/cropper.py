import cv2
import numpy as np
from PIL import Image
import io

def crop_rectangle(image_bytes, x, y, w, h):
    img = _decode(image_bytes)
    cropped = img[y:y+h, x:x+w]
    return _encode(cropped)

def crop_circle(image_bytes, cx, cy, radius):
    img = _decode(image_bytes)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (cx, cy), radius, 255, -1)

    # Apply mask
    result = cv2.bitwise_and(img, img, mask=mask)

    # Make background transparent (RGBA)
    b, g, r = cv2.split(result)
    alpha = mask
    rgba = cv2.merge([b, g, r, alpha])

    return _encode(rgba, ext=".png")  # PNG to preserve transparency

def _decode(image_bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

def _encode(img, ext=".jpg"):
    success, buffer = cv2.imencode(ext, img)
    if not success:
        raise ValueError("Failed to encode image")
    return io.BytesIO(buffer.tobytes())