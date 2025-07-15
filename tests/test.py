

from openai import OpenAI
import os
from weasyprint import HTML


# client = OpenAI(api_key=os.getenv("MY_OPENAI_KEY"))
client = OpenAI(api_key="")

# Upload the PDFs
file1 = client.files.create(file=open("1.pdf","rb"), purpose="user_data")
file2 = client.files.create(file=open("2.pdf","rb"), purpose="user_data")

# Ask GPT-4.1 to compare
response = client.responses.create(
  model="gpt-4.1",
  input=[
    {"role": "user", "content":[{"type":"input_file", "file_id":file1.id}]},
    {"role": "user", "content":[{"type":"input_file", "file_id":file2.id},
                                 {"type":"input_text", "text":"Please compare the contents and highlight key differences. Output the results in HTML format with a table showing matches and mismatches. Use ✅ for matches and ❌ for mismatches."}]}
  ]
)
# print(response.output[0].content[0].text)


# Extract HTML output
html_output = response.output[0].content[0].text

# Convert directly to PDF using WeasyPrint
pdf_filename = "comparison_result.pdf"
HTML(string=html_output).write_pdf(pdf_filename)

print(f"✅ PDF saved as '{pdf_filename}'")