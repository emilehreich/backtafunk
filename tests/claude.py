


API_KEY = ""


import anthropic
import os
from weasyprint import HTML
import base64
from pdf2image import convert_from_path

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=API_KEY  # Replace with your actual API key
)

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

# Convert PDFs to images
pdf1_images = pdf_to_images_base64("1.pdf")
pdf2_images = pdf_to_images_base64("2.pdf")

# Create content with all images
content = [
    {
        "type": "text",
        "text": "I'm providing you with images from two PDF files. Please compare their contents and highlight key differences. Output the results in HTML format with a table showing matches and mismatches. Use ✅ for matches and ❌ for mismatches."
    }
]

# Add images from PDF 1
for i, img_base64 in enumerate(pdf1_images):
    content.append({
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": img_base64
        }
    })

# Add images from PDF 2
for i, img_base64 in enumerate(pdf2_images):
    content.append({
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": img_base64
        }
    })

# Create the message
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    messages=[
        {
            "role": "user",
            "content": content
        }
    ]
)

# Extract HTML output
html_output = message.content[0].text

# Convert directly to PDF using WeasyPrint
pdf_filename = "comparison_result.pdf"
HTML(string=html_output).write_pdf(pdf_filename)

print(f"✅ PDF saved as '{pdf_filename}'")