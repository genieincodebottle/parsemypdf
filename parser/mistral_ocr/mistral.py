"""
Advanced PDF Processing with Mistral-OCR

Dependencies:
    - mistralai: For Mistral OCR
    - python-dotenv: Environment variable management

Environment Setup:
    Requires:
        - MISTRAL_API_KEY in .env file
"""
import os
import sys
from mistralai.client import Mistral
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
# Initialize environment variables from .env file
load_dotenv()
# Validate and set Mistral API key
# Both spellings are in circulation, so accept either rather than telling
# someone their key is missing when it is sitting in .env under another name.
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY") or os.getenv("MISTRAL_AI_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError(
        "No Mistral key found. Set MISTRAL_API_KEY (or MISTRAL_AI_API_KEY) "
        "in .env. Get one at https://console.mistral.ai/api-keys"
    )

def main():
    """
    Main execution function implementing a complete PDF processing and Q&A pipeline.
    """
    # PHASE 1: PDF PROCESSING AND TEXT EXTRACTION
    
    # Configure input PDF path
    # Different sample types available for processing:
    # Which PDF to process. Override with --file, e.g.
    #   python parser/mistral_ocr/mistral.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")

    try:
        file_name = os.path.basename(file_path)

        client = Mistral(api_key=MISTRAL_API_KEY)
        uploaded_pdf = client.files.upload(
                file={
                        "file_name": file_name,
                        "content": open(file_path, "rb"),
                    },
                    purpose="ocr"
                ) 
        signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id).url
        
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url,
            },
            include_image_base64=True,
            )
        final_response = ""
        
        for page in ocr_response.pages:
            final_response += page.markdown + "\n"
            
        print(final_response)

    except Exception as e:
        raise e

if __name__ == "__main__":
    main()