"""
Advanced PDF Processing with Gemini

Dependencies:
    - google-generativeai: For Gemini API
    - python-dotenv: Environment variable management

Environment Setup:
    Requires:
        - GOOGLE_API_KEY in .env file
"""
import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
# Initialize environment variables from .env file
load_dotenv()
# Validate and set Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables")

def main():
    """
    Main execution function implementing a complete PDF processing.
    """
    # PHASE 1: PDF PROCESSING AND TEXT EXTRACTION
    
    # Configure input PDF path
    # Different sample types available for processing:
    # Which PDF to process. Override with --file, e.g.
    #   python parser/gemini/gemini.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")

    try:
        with open(file_path, 'rb') as file:
            pdf_bytes = file.read()

        # Create the prompt for text extraction
        prompt = """Extract all the text content, including both plain text and tables, from the 
                provided document or image. Maintain the original structure, including headers, 
                paragraphs, and any content preceding or following the table. Format the table in 
                Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
                including any introductory or explanatory text before or after the table."""
        
        client = genai.Client(api_key=GOOGLE_API_KEY)
        # Generate response from Gemini
        response = client.models.generate_content(
            model="gemini-pro-latest", #gemini-2.5-flash, #gemini-flash-lite-latest, #gemini-flash-latest
            contents=[
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type='application/pdf',
                ),
                prompt])
        response_text = response.text
        print(response_text)

    except Exception as e:
        raise e

if __name__ == "__main__":
    main()