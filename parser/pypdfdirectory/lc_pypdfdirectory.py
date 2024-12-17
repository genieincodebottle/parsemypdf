"""
Batch PDF Content Extraction Script using PyPDF2 Directory Loader

This script demonstrates the use of PyPDFDirectoryLoader from LangChain to batch process
and extract text content from multiple PDF files in a directory. It uses PyPDF2 as the
underlying PDF processor for basic text extraction.

Dependencies:
   - langchain_community.document_loaders: For directory-based PDF loading
   - PyPDF2: Pure Python library for reading and writing PDFs

Usage:
   Place PDF files in the input directory and run the script to process all PDFs.
   The script will process all PDF files in the specified directory sequentially.

Key Features:
   - Batch processing of multiple PDFs
   - Directory-based loading
   - Basic text extraction from each PDF
   - Maintains document separation in output
"""

from langchain_community.document_loaders import PyPDFDirectoryLoader

def main():
   """
   Main function to demonstrate batch PDF content extraction using PyPDFDirectoryLoader.
   
   Sample files in directory:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
   
   PyPDFDirectoryLoader characteristics:
       - Processes all PDFs in specified directory
       - Uses PyPDF2 for text extraction
       - Maintains separation between documents
       - Inherits PyPDF2 limitations:
           * Basic text extraction only
           * Limited layout preservation
           * May struggle with complex content
       
   Returns:
       None: Prints extracted content to console
   """
   
   # Initialize directory loader
   # Points to directory containing PDF files
   loader = PyPDFDirectoryLoader("input/")
   
   # Extract content from all PDFs in directory
   # Returns list of Document objects, one per page across all PDFs
   # Documents maintain source file information in metadata
   docs = loader.load()
   
   # Output options
   #print(docs)  # Uncomment to see full Document objects including metadata
   print(docs[3].page_content)  # Print content of first page from first processed PDF

if __name__ == "__main__":
   main()