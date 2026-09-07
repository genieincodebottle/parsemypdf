"""
PDF Content Extraction Script using PDFPlumber

This script demonstrates the use of PDFPlumberLoader from LangChain to extract text and tabular 
content from PDF files. PDFPlumber excels at extracting both textual content and tables,
making it particularly useful for documents with mixed content types.

Dependencies:
   - langchain_community.document_loaders: For PDF loading functionality
   - pdfplumber: Backend PDF processing library with enhanced table extraction

Usage:
   Run the script directly to process a specified PDF file and print its content.
   Different sample files can be uncommented in the main function to test various PDF types.

Advantages:
   - Better table extraction compared to PDFMiner
   - Maintains text positioning and layout information
   - Can extract table borders and cell properties
"""
import os
import sys
from langchain_community.document_loaders import PDFPlumberLoader

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
def main():
   """
   Main function to demonstrate PDF content extraction using PDFPlumber.
   
   Tests different types of PDF files:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
       - sample-5.pdf: Multi-column Texts 
   
   The function uses PDFPlumber which is particularly good at:
       - Extracting tables while maintaining structure
       - Preserving text positioning
       - Handling complex layouts
       
   Returns:
       None: Prints extracted content to console
   """
   # Select PDF file to process - uncomment desired sample file
   # Which PDF to process. Override with --file, e.g.
   #   python parser/pdfplumber/lc_pdfplumber.py --file input/sample-3.pdf
   # Run with --list to see every bundled sample.
   file_path = input_pdf("sample-1.pdf")
   
   # Initialize PDFPlumber loader with target file
   loader = PDFPlumberLoader(file_path)
   
   # Extract content from PDF
   # Returns list of Document objects containing both text and table data
   docs = loader.load()
   
   # Output options
   extracted_content = ""
   for doc in docs:
      extracted_content += doc.page_content+ "\n"

   # Output extracted content to output.txt
   os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
   with open(os.path.join(project_root, "output", "lc_pdfplumber.txt"), "w", encoding="utf-8") as file:
      file.write(extracted_content)

if __name__ == "__main__":
   main()