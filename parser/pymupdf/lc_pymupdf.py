"""
PDF Content Extraction Script using PyMuPDF (fitz)

This script demonstrates the use of PyMuPDFLoader from LangChain to extract content 
from PDF files. PyMuPDF (also known as fitz) is a high-performance PDF processing 
library that excels at handling complex PDFs with various content types.

Dependencies:
   - langchain_community.document_loaders: For PDF loading interface
   - PyMuPDF (fitz): Backend PDF processing library with advanced features

Usage:
   Run the script directly to process a specified PDF file and print its content.
   Different sample files can be uncommented in the main function to test various PDF types.

Advantages:
   - High-performance processing
   - Better handling of complex layouts
   - Support for extracting images and annotations
   - Ability to handle encrypted PDFs
   - Memory efficient for large documents
"""
import os
import sys
from langchain_community.document_loaders import PyMuPDFLoader

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
def main():
   """
   Main function to demonstrate PDF content extraction using PyMuPDF.
   
   Tests different types of PDF files:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
       - sample-5.pdf: Multi-column Texts 
   
   PyMuPDF advantages include:
       - Fast processing speed
       - Accurate text extraction with layout preservation
       - Better handling of complex PDFs
       - Support for various PDF features (forms, annotations)
       - Lower memory footprint
       
   Returns:
       None: Prints extracted content to console
   """
   # Select PDF file to process - uncomment desired sample file
   # Which PDF to process. Override with --file, e.g.
   #   python parser/pymupdf/lc_pymupdf.py --file input/sample-3.pdf
   # Run with --list to see every bundled sample.
   file_path = input_pdf("sample-1.pdf")
   
   # Initialize PyMuPDF loader
   # PyMuPDF handles PDF parsing and content extraction
   loader = PyMuPDFLoader(file_path)
   
   # Extract content from PDF
   # Returns list of Document objects with extracted text and metadata
   # Each document represents a page with its content and properties
   docs = loader.load()
   
   # Output options
   extracted_content = ""
   for doc in docs:
      extracted_content += doc.page_content+ "\n"

   # Output extracted content to output.txt
   os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
   with open(os.path.join(project_root, "output", "lc_pymupdf.txt"), "w", encoding="utf-8") as file:
      file.write(extracted_content)

if __name__ == "__main__":
   main()