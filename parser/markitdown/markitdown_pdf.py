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

from markitdown import MarkItDown

def main():
    """
    Main function to demonstrate PDF content extraction.
    
    Processes different types of PDF files:
        - sample-1.pdf: Contains simple tables
        - sample-2.pdf: Contains image-based simple tables
        - sample-3.pdf: Contains image-based complex tables
        - sample-4.pdf: Contains mixed content (text, images, complex tables)
        
    Returns:
        None: Prints extracted content to console
    """
    md = MarkItDown()
    # Select PDF file to process - uncomment desired sample file
    #file_path = "input/sample-1.pdf" # Table in pdf
    #file_path = "input/sample-2.pdf" # Image based simple table in pdf
    #file_path = "input/sample-3.pdf" # Image based complex table in pdf
    file_path = "input/sample-4.pdf"  # Complex PDF with mixed content types
    result = md.convert(file_path)
    print(result.text_content)

if __name__ == "__main__":
    main()