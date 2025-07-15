from openai import OpenAI
from fastapi import UploadFile
from weasyprint import HTML
from utils import pdf_to_images_base64

import anthropic

client_openai = OpenAI(api_key="")

async def analyze_routes_service(trucks_file: UploadFile, invoice_file: UploadFile) -> str:
    file1 = client_openai.files.create(file=(trucks_file.filename, await trucks_file.read()), purpose="user_data")
    file2 = client_openai.files.create(file=(invoice_file.filename, await invoice_file.read()), purpose="user_data")

    response = client_openai.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "user", "content":[{"type":"input_file", "file_id":file1.id}]},
            {"role": "user", "content":[{"type":"input_file", "file_id":file2.id},
                                        {"type":"input_text", "text":"Please compare the contents and highlight key differences. Output the results in HTML format with a table showing matches and mismatches. Use ✅ for matches and ❌ for mismatches."}]}
        ]
        )
    return response.output[0].content[0].text


API_KEY = ""

async def analyze_po_mtc_service(file_1: UploadFile, file_2: UploadFile) -> str:
    client = anthropic.Anthropic(api_key=API_KEY  )

    pdf1_images = pdf_to_images_base64(file_1)
    pdf2_images = pdf_to_images_base64(file_2)

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
    return message.content[0].text

async def analyze_po_pi_service(file_1: UploadFile, file_2: UploadFile) -> str:
    client = anthropic.Anthropic(api_key=API_KEY  )

    pdf1_images = pdf_to_images_base64(file_1)
    pdf2_images = pdf_to_images_base64(file_2)

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
    return message.content[0].text  