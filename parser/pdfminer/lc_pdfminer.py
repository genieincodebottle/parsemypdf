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

from langchain_community.document_loaders import PDFMinerLoader

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
    # File path selection - uncomment desired sample file
    #file_path = "input/sample-1.pdf" # Table in pdf
    #file_path = "input/sample-2.pdf" # Image based simple table in pdf
    #file_path = "input/sample-3.pdf" # Image based complex table in pdf
    file_path = "input/sample-4.pdf"  # Complex PDF where many text contents and tables are in image
    
    # Initialize PDFMiner loader with specified file
    loader = PDFMinerLoader(file_path)
    
    # Extract content from PDF
    # docs will be a list of Document objects, where each Document represents a page
    docs = loader.load()
    
    # Print extracted content
    #print(docs)  # Uncomment to see full Document objects including metadata
    print(docs[0].page_content)  # Print only the text content of the first page

if __name__ == "__main__":
    main()