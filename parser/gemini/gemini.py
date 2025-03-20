"""
Advanced PDF Processing and Question-Answering System with Gemini

This script implements a sophisticated PDF processing pipeline that combines computer vision 
and natural language processing to extract and analyze PDF content. It uses Google's Gemini 
model for visual content extraction and implements a question-answering system.

Key Components:
    1. PDF Processing:
        - Converts PDFs to images
        - Uses Gemini Pro Vision for text/table extraction
        - Preserves document structure and formatting
    
    2. Question-Answering System:
        - Text chunking and embedding
        - Vector-based retrieval
        - Contextual question answering
        
Dependencies:
    - google-generativeai: For Gemini API
    - python-dotenv: Environment variable management
    - langchain & related: For LLM and embedding operations
    - FAISS: For vector similarity search
    - Custom utils: For PDF-to-image conversion

Environment Setup:
    Requires:
        - Google API key in .env file
        - Local Ollama installation
        - Access to HuggingFace models
"""
import sys
import os
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import PIL

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from utils.pdf_to_image import PDFToJPGConverter

# Initialize environment variables from .env file
load_dotenv()

# Validate and set Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables")

def get_completion_response(image_path):
    """
    Send a request to Gemini Pro Vision API to extract text and tables from an image.

    Args:
        image_path (str or Path): Path to the image file

    Returns:
        str: Extracted text content including tables

    Note:
        The function is configured to extract both plain text and tables,
        maintaining the original structure and formatting tables in Markdown.
    """
    
    # Create the prompt for text extraction
    prompt = """Extract all the text content, including both plain text and tables, from the 
               provided document or image. Maintain the original structure, including headers, 
               paragraphs, and any content preceding or following the table. Format the table in 
               Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
               including any introductory or explanatory text before or after the table."""
    
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Generate response from Gemini
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=[
                prompt,
                PIL.Image.open(image_path)
            ]
        )
    response_text = response.text
    return response_text


def main():
    """
    Main execution function implementing a complete PDF processing and Q&A pipeline.

    The pipeline consists of two major phases:
    
    Phase 1 - PDF Processing:
    1. PDF to Image Conversion
        - Converts PDF pages to JPG images
        - Handles various PDF types (simple tables, complex tables, mixed content)
    2. Text Extraction
        - Uses Gemini Pro Vision to extract text from images
        - Maintains formatting and structure of content
        

    """
    # PHASE 1: PDF PROCESSING AND TEXT EXTRACTION
    
    # Configure input PDF path
    # Different sample types available for processing:
    #file_path = project_root+"/input/sample-1.pdf"  # Simple table-based PDF
    #file_path = project_root+"/input/sample-2.pdf"  # PDF with image-based simple tables
    file_path = project_root+"/input/sample-3.pdf"   # PDF with complex image-based tables
    #file_path = project_root+"/input/sample-4.pdf"  # PDF with mixed content types
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts

    try:
        # Set up PDF to image conversion
        converter = PDFToJPGConverter()
        output_path = project_root+"/converted_images/gemini"  # Directory for converted images

        # Execute PDF to JPG conversion
        converted_files = converter.convert_pdf(file_path, output_path)

        # Display conversion results
        print("\nConversion Summary:")
        print(f"Total pages converted: {len(converted_files)}")
        print("\nConverted files:")
        for file in converted_files:
            print(f"- {file}")

        # Process and extract text from converted images
        directory = Path(output_path)
        final_response = ""

        # Iterate through converted images and extract text using Gemini
        for image_path in directory.iterdir():
            # Extract text using Gemini Pro Vision
            extracted_text = get_completion_response(image_path)
            # Accumulate extracted text
            final_response += extracted_text + "\n"

        # Display complete extracted content
        print(final_response)

    except Exception as e:
        raise e

if __name__ == "__main__":
    main()