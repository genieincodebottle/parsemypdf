"""
PDF Content Extraction Script using Microsoft's Opensource markitdown library

Dependencies:
    - markitdown

Usage:
    Run the script directly to process a specified PDF file and print its content.
    Different sample files can be uncommented in the main function to test various PDF types.

Note: 
    MarkItDown is a utility for converting various files to Markdown (e.g., for indexing, text analysis, etc). It supports:
    PDF, PowerPoint, Word, Excel, Images (EXIF metadata and OCR), Audio (EXIF metadata and speech transcription), HTML
    Text-based formats (CSV, JSON, XML), ZIP files (iterates over contents)
"""
import os
import sys
from markitdown import MarkItDown

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
def main():
    """
    Main function to demonstrate PDF content extraction.
    
    Processes different types of PDF files:
        - sample-1.pdf: Contains simple tables
        - sample-2.pdf: Contains image-based simple tables
        - sample-3.pdf: Contains image-based complex tables
        - sample-4.pdf: Contains mixed content (text, images, complex tables)
        - sample-5.pdf: Multi-column Texts 
        
    Returns:
        None: Prints extracted content to console
    """
    md = MarkItDown()
    # Select PDF file to process - uncomment desired sample file
    # Which PDF to process. Override with --file, e.g.
    #   python parser/markitdown/markitdown_pdf.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")
    
    result = md.convert(file_path)

    # Output extracted content to output.txt
    os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
    with open(os.path.join(project_root, "output", "markitdown_pdf.txt"), "w", encoding="utf-8") as file:
        file.write(result.text_content)

if __name__ == "__main__":
    main()