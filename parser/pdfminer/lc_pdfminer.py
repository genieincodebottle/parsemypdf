"""
PDF Content Extraction Script using PDFMiner

This script demonstrates the use of PDFMinerLoader from LangChain to extract text content 
from PDF files. It's particularly useful for processing different types of PDFs containing 
various elements like tables, images, and text.

Dependencies:
    - langchain_community.document_loaders: For PDF processing functionality
    - pdfminer: Backend PDF processing library

Usage:
    Run the script directly to process a specified PDF file and print its content.
    Different sample files can be uncommented in the main function to test various PDF types.

Note: 
    PDFMiner is particularly good at extracting text but may have limitations with 
    complex layouts or image-based content.
"""
import os
from langchain_community.document_loaders import PDFMinerLoader

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

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
    # File path selection - uncomment desired sample file
    #file_path = project_root+"/input/sample-1.pdf" # Table in pdf
    #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
    #file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
    file_path = project_root+"/input/sample-4.pdf"  # Complex PDF where many text contents and tables are in image
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 
    
    # Initialize PDFMiner loader with specified file
    loader = PDFMinerLoader(file_path)
    
    # Extract content from PDF
    # docs will be a list of Document objects, where each Document represents a page
    docs = loader.load()
    
    # Output options
    extracted_content = ""
    for doc in docs:
        extracted_content += doc.page_content+ "\n"

    # Output extracted content to output.txt
    with open("output.txt", 'w') as file:
        file.write(extracted_content)

if __name__ == "__main__":
    main()