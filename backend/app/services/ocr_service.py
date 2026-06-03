import cloudinary
import cloudinary.uploader
import httpx
from app.core.config import settings

class OCRService:
    def __init__(self):
        self._reader = None  # keep placeholder for compatibility
        # No heavy OCR model loaded
        # Cloudinary config remains unchanged
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    async def _call_ocr_space(self, image_bytes: bytes) -> str:
        # OCR.Space free tier (no API key required, limited usage)
        url = "https://api.ocr.space/parse/image"
        files = {"filename": ("upload.jpg", image_bytes)}
        data = {"language": "eng", "isOverlayRequired": "false"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data, files=files, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if result.get("IsErroredOnProcessing"):
                raise RuntimeError(f"OCR error: {result.get('ErrorMessage')}")
            parsed = result.get("ParsedResults", [{}])[0]
            return parsed.get("ParsedText", "")

    async def process_image(self, image_bytes: bytes) -> str:
        # Use free OCR API; fallback to empty string on failure
        try:
            return await self._call_ocr_space(image_bytes)
        except Exception as e:
            # Log error in production; here we just return empty
            return ""

    def upload_to_cloudinary(self, image_bytes: bytes, filename: str):
        upload_result = cloudinary.uploader.upload(image_bytes, public_id=filename)
        return upload_result['secure_url']

ocr_service = OCRService()
