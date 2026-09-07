"""
PDF Content Extraction Script using PyPDF2

This script demonstrates the use of PyPDFLoader from LangChain to extract text content 
from PDF files. PyPDF2 is a pure-Python library for PDF processing that provides basic
text extraction capabilities.

Dependencies:
   - langchain_community.document_loaders: For PDF loading interface
   - PyPDF2: Pure Python library for reading and writing PDFs

Usage:
   Run the script directly to process a specified PDF file and print its content.
   Different sample files can be uncommented in the main function to test various PDF types.

Characteristics:
   - Pure Python implementation (no external dependencies)
   - Basic text extraction capabilities
   - Lightweight and easy to install
   - Best suited for simple PDFs with primarily text content
   - Limited support for complex layouts and tables
"""
import os
import sys
from langchain_community.document_loaders import PyPDFLoader

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
def main():
   """
   Main function to demonstrate PDF content extraction using PyPDF2.
   
   Tests different types of PDF files:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
       - sample-5.pdf: Multi-column Texts 
   
   PyPDF2 characteristics:
       - Simple text extraction without layout preservation
       - Basic PDF parsing capabilities
       - May have limitations with:
           * Complex layouts
           * Tables
           * Image-based text
           * Special characters
       
   Returns:
       None: Prints extracted content to console
   """
   # Select PDF file to process - uncomment desired sample file
   # Which PDF to process. Override with --file, e.g.
   #   python parser/pypdf/lc_pypdf.py --file input/sample-3.pdf
   # Run with --list to see every bundled sample.
   file_path = input_pdf("sample-1.pdf")
   
   # Initialize PyPDF loader
   # Uses PyPDF2 internally for basic PDF text extraction
   loader = PyPDFLoader(file_path)
   
   # Extract content from PDF
   # Returns list of Document objects with basic text content
   # Note: Layout and formatting may not be preserved
   docs = loader.load()
   
   # Output options
   print("#### Extracted Content #### \n")
   for doc in docs:
      print(doc.page_content+ "\n")

if __name__ == "__main__":
   main()