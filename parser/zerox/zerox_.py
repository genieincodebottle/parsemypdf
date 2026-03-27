"""
PDF Parsing using Zerox (Vision Model-based OCR)

Zerox converts PDFs into images and uses vision language models (GPT-4o, etc.)
to extract text with high accuracy. It supports structured data extraction using
schemas, making it ideal for pulling specific fields from documents.

Key Features:
    - Converts PDF pages to images, then uses vision LLMs for extraction
    - Supports structured data extraction via schemas
    - Works with OpenAI, Azure OpenAI, and other vision model providers
    - Handles complex layouts, tables, and mixed content
    - Returns clean markdown output

Dependencies:
    - py-zerox: pip install py-zerox
    - Requires an OpenAI API key (or other supported vision model provider)

Note: Uses the OpenAI API for processing. Each page costs ~$0.01 with gpt-4o-mini.
"""
import os
import sys
import asyncio

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from dotenv import load_dotenv
load_dotenv()


def main():
    """
    Extract text from PDF using Zerox with GPT-4o-mini vision model.
    """
    from pyzerox import zerox

    # Configure input PDF path
    #file_path = project_root + "/input/sample-1.pdf"  # Standard tables
    #file_path = project_root + "/input/sample-2.pdf"  # Image-based simple tables
    file_path = project_root + "/input/sample-3.pdf"   # Image-based complex tables
    #file_path = project_root + "/input/sample-4.pdf"  # Mixed content
    #file_path = project_root + "/input/sample-5.pdf"  # Multi-column texts

    # Select the vision model to use
    model = "gpt-4o-mini"  # Cost-effective option (~$0.01/page)
    #model = "gpt-4o"      # Higher accuracy but more expensive

    # Run Zerox extraction
    result = asyncio.run(zerox(
        file_path=file_path,
        model=model,
        cleanup=True,
    ))

    # Extract text from result pages
    full_text = ""
    for page in result.pages:
        full_text += page.content + "\n\n"

    print(full_text)

    # Save output
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
