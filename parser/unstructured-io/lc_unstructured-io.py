"""
PDF Content Extraction Script using Unstructured.io API

This script demonstrates the use of UnstructuredLoader from LangChain to extract and 
structure content from PDF files using the Unstructured.io cloud API. This service 
excels at handling complex documents with mixed content types.

Dependencies:
   - langchain_unstructured: For Unstructured.io API integration
   - unstructured: Backend library for document processing
   - Unstructured.io API key: Required for cloud-based processing

Usage:
   Requires a valid Unstructured.io API key
   Run the script directly to process a specified PDF file and print its content.
   Different sample files can be uncommented in the main function to test various PDF types.

Advantages:
   - Advanced content partitioning
   - Better handling of tables and layouts
   - Cloud-based processing power
   - Sophisticated document structure analysis
   - Support for multiple document formats
"""
import os
from langchain_unstructured import UnstructuredLoader

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Get API key from environment variables and validate its presence
UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
if not UNSTRUCTURED_API_KEY:
    raise ValueError("UNSTRUCTURED_API_KEY not set in environment variables")

def main():
   """
   Main function to demonstrate PDF content extraction using Unstructured.io API.
   
   Tests different types of PDF files:
       - sample-1.pdf: Contains standard tables
       - sample-2.pdf: Contains image-based simple tables
       - sample-3.pdf: Contains image-based complex tables
       - sample-4.pdf: Contains mixed content (text, images, complex tables)
       - sample-5.pdf: Multi-column Texts 
   
   Unstructured.io advantages:
       - API-based processing for better results
       - Sophisticated content partitioning
       - Handles complex document layouts
       - Features:
           * Table extraction
           * Layout analysis
           * Content classification
           * Metadata extraction
       
   Returns:
       None: Prints extracted content to console
   """
   # Select PDF file to process - uncomment desired sample file
   file_path = project_root+"/input/sample-1.pdf" # Table in pdf
   #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
   #file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
   #file_path = project_root+"/input/sample-4.pdf"  # Complex PDF with mixed content types
   #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 
   
   # Initialize Unstructured loader with API configuration
   # Note: API key should be stored securely in environment variables
   loader = UnstructuredLoader(
       file_path=file_path,
       api_key=UNSTRUCTURED_API_KEY,  # Replace with your API key
       partition_via_api=True,  # Enable cloud-based processing
   )
   
   # Extract and structure content from PDF
   # Returns list of Document objects with structured content
   # Content is partitioned into meaningful segments
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