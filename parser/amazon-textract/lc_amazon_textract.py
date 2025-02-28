"""
PDF Content Extraction Script using Amazon Textract

This script demonstrates the use of AmazonTextractPDFLoader from LangChain to extract content 
from PDF files using AWS Textract service. Textract is an AWS service that automatically 
extracts text, handwriting, and data from scanned documents.

Dependencies:
   - langchain_community.document_loaders: For Textract integration
   - boto3: AWS SDK for Python
   - AWS credentials: Properly configured AWS access
   - Amazon Textract service access

Usage:
   Requires:
       - Configured AWS credentials
       - Appropriate IAM permissions for Textract
   Can process PDFs from:
       - Local files
       - S3 buckets directly
   
Advantages:
   - Advanced OCR capabilities
   - Table extraction
   - Form processing
   - Handwriting recognition
   - Integration with AWS services
"""
import os
import boto3
from langchain_community.document_loaders import AmazonTextractPDFLoader

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def main():
    """
    Main function to demonstrate PDF content extraction using Amazon Textract.

    Processes PDF files:
        - Can handle local files
        - Can process directly from S3
        - Supports complex documents with:
            * Tables
            * Forms
            * Handwritten text
            * Mixed content types

    Amazon Textract features:
        - OCR (Optical Character Recognition)
        - Table structure recognition
        - Form field detection
        - Key-value pair extraction
        - Integration with AWS ecosystem
        
    Returns:
        None: Prints extracted content to console
    """
    # Local file path for processing
    file_path = project_root+"/input/sample-1.pdf"  # Contains standard table format
    #file_path = project_root+"/input/sample-2.pdf" # Contains image-based simple table
    #file_path = project_root+"/input/sample-3.pdf" # Contains image-based complex table
    #file_path = project_root+"/input/sample-4.pdf" # Complex PDF with mixed content (text and tables in images)
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 

    # Initialize AWS Textract client
    # Requires properly configured AWS credentials
    textract_client = boto3.client(
        "textract",
        region_name="us-east-1"  # Specify your AWS region
    )

    # Alternative: Direct S3 path processing
    #file_path = "s3://amazon-textract-public-content/langchain/layout-parser-paper.pdf"

    # Initialize Textract loader with AWS client
    # Can process both local files and S3 paths
    loader = AmazonTextractPDFLoader(
        file_path,
        client=textract_client  # Use configured Textract client
    )

    # Extract content using Textract
    # Returns list of Document objects with extracted text and metadata
    documents = loader.load()

    # Second load call (Note: This appears redundant and could be removed)
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