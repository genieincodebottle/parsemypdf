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

from langchain_community.document_loaders import PyPDFLoader

def main():
   """
   Main function to demonstrate PDF content extraction using PyPDF2.
   
   Tests different types of PDF files:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
   
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
   #file_path = "input/sample-1.pdf" # Table in pdf
   #file_path = "input/sample-2.pdf" # Image based simple table in pdf
   #file_path = "input/sample-3.pdf" # Image based complex table in pdf
   file_path = "input/sample-4.pdf"  # Complex PDF with mixed content types
   
   # Initialize PyPDF loader
   # Uses PyPDF2 internally for basic PDF text extraction
   loader = PyPDFLoader(file_path)
   
   # Extract content from PDF
   # Returns list of Document objects with basic text content
   # Note: Layout and formatting may not be preserved
   docs = loader.load()
   
   # Output options
   #print(docs)  # Uncomment to see full Document objects including metadata
   print(docs[0].page_content)  # Print extracted text from first page

if __name__ == "__main__":
   main()