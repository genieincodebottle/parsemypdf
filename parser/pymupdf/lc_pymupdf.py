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

from langchain_community.document_loaders import PyMuPDFLoader

def main():
   """
   Main function to demonstrate PDF content extraction using PyMuPDF.
   
   Tests different types of PDF files:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
   
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
   #file_path = "input/sample-1.pdf" # Table in pdf
   #file_path = "input/sample-2.pdf" # Image based simple table in pdf
   #file_path = "input/sample-3.pdf" # Image based complex table in pdf
   file_path = "input/sample-4.pdf"  # Complex PDF with mixed content types
   
   # Initialize PyMuPDF loader
   # PyMuPDF handles PDF parsing and content extraction
   loader = PyMuPDFLoader(file_path)
   
   # Extract content from PDF
   # Returns list of Document objects with extracted text and metadata
   # Each document represents a page with its content and properties
   docs = loader.load()
   
   # Output options
   #print(docs)  # Uncomment to see full Document objects including metadata
   print(docs[0].page_content)  # Print text content of first page only

if __name__ == "__main__":
   main()