from pdf2image import convert_from_path
import os
import base64

def pdf_to_images_base64(pdf_path):
    """Convert PDF pages to base64 encoded images"""
    images = convert_from_path(pdf_path)
    base64_images = []
    
    for i, image in enumerate(images):
        # Save as PNG temporarily
        temp_path = f"temp_page_{i}.png"
        image.save(temp_path, 'PNG')
        
        # Convert to base64
        with open(temp_path, "rb") as img_file:
            base64_images.append(base64.b64encode(img_file.read()).decode('utf-8'))
        
        # Clean up temp file
        os.remove(temp_path)
    
    return base64_images