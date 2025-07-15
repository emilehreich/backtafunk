from pdf2image import convert_from_bytes
from fastapi import UploadFile
import base64
import tempfile
import os

async def pdf_to_images_base64(upload_file: UploadFile):
    """Convert PDF pages from an UploadFile to base64 encoded images"""
    # Read file content
    pdf_bytes = await upload_file.read()
    
    # Convert PDF to images from bytes
    images = convert_from_bytes(pdf_bytes)
    base64_images = []

    # Use temporary directory to store intermediate PNGs
    with tempfile.TemporaryDirectory() as tmpdirname:
        for i, image in enumerate(images):
            temp_path = os.path.join(tmpdirname, f"page_{i}.png")
            image.save(temp_path, 'PNG')
            
            with open(temp_path, "rb") as img_file:
                base64_images.append(base64.b64encode(img_file.read()).decode('utf-8'))

    return base64_images
