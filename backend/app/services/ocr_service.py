import easyocr
import cloudinary
import cloudinary.uploader
from app.core.config import settings
from PIL import Image
import io

class OCRService:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    def process_image(self, image_bytes: bytes):
        # 1. OCR Extraction
        results = self.reader.readtext(image_bytes)
        text = " ".join([res[1] for res in results])
        return text

    def upload_to_cloudinary(self, image_bytes: bytes, filename: str):
        # 2. Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(image_bytes, public_id=filename)
        return upload_result['secure_url']

ocr_service = OCRService()
