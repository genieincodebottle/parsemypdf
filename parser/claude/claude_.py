"""
PDF Content Extraction and Question Answering Script using Claude API

This script leverages Anthropic's Claude API to process PDF documents, extract content, and answer 
specific questions about the content. It handles various PDF formats including complex layouts, 
tables, and image-based content, providing accurate question-answering capabilities.

Key Features:
    - Extracts and structures content from PDFs while preserving formatting
    - Processes both text-based and image-based content
    - Converts tables to markdown format
    - Provides focused answers to specific questions about PDF content
    - Handles multiple PDF formats (standard tables, image-based tables, complex layouts)
    - Supports base64 encoding for secure PDF transmission

Dependencies:
    - anthropic: For interacting with Claude API
    - python-dotenv: For environment variable management
    - base64 (standard library): For PDF encoding
    - os (standard library): For environment variable access

Required Environment Variables:
    - ANTHROPIC_API_KEY: API key for authenticating with Anthropic's services

Usage:
    Place PDF files in the 'input/' directory and set up environment variables.
    The script can process various types of PDFs:
    - sample-1.pdf: Contains standard tables
    - sample-2.pdf: Contains image-based simple tables
    - sample-3.pdf: Contains image-based complex tables
    - sample-4.pdf: Complex PDF with mixed content (text and tables in images)
    - sample-5.pdf: Multi-column Texts 

Note: Uses Claude 3.7 Sonnet model with PDF beta feature for optimal extraction
"""

# Standard library imports
import os
import base64

# Third-party imports
from dotenv import load_dotenv
import anthropic

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in environment variables")

def get_completion(client, messages, model_name):
    """
    Call the Claude model API to process messages and return the response
    
    Args:
        client (anthropic.Client): Initialized Anthropic API client
        messages (list): List of message objects containing role and content
        model_name (str): Name of the Claude model to use
        
    Returns:
        str: The text response from the model
    """
    return client.messages.create(
        model=model_name,
        max_tokens=8192,
        messages=messages
    ).content[0].text

def extract_pdf_content(question, pdf_base64_string) -> str:
    """
    Extract content from a PDF and answer questions about it using Claude API
    
    Args:
        question (str): Question to ask about the PDF content
        pdf_base64_string (str): Base64 encoded PDF content
        
    Returns:
        str: Claude's answer to the question based on PDF content
    """
    # Initialize Anthropic client with PDF beta feature
    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
    
    # Define system prompt for PDF content extraction and question answering
    system_prompt = f"""You are an expert at extracting and structuring content from PDFs.
    Please extract all the text content from the provided PDF, maintaining the structure and formatting.
    Format tables properly in markdown format. Preserve all numerical data and relationships between elements.
    After extracting content from the pdf as text, answer the following question: {question}
    Response must be answer to the question and not the extracted content of pdf.
    Response must be to the point."""
    
    # Specify the model version
    model_name = "claude-sonnet-4-20250514"
    #model_name = "claude-opus-4-20250514"
    #model_name = "claude-3-7-sonnet-latest"

    # Construct message payload with PDF document and prompt
    messages = [
        {
            "role": 'user',
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_base64_string}},
                {"type": "text", "text": system_prompt}
            ]
        }
    ]
    
    # Get response from Claude
    response = get_completion(client, messages, model_name)
    return response

def main():
    """
    Main function to process PDF files and extract information using Claude API
    """
    # STEP 1: Read and encode the PDF file
    # Multiple PDF files available for testing different scenarios:
    #file_path = project_root+"/input/sample-1.pdf" # Table in pdf
    #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
    file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
    #file_path = project_root+"/input/sample-4.pdf"  # Complex PDF where many text contents and tables are in image
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 
    
    # Read PDF file and convert to base64
    with open(file_path, "rb") as pdf_file:
        binary_data = pdf_file.read()
        base64_string = base64.b64encode(binary_data).decode('utf-8')
    
    # STEP 2: Process PDF and get answer to specific question
    # Sample questions for different use cases:
    #question = "What is maximum lot depth/width of commercial zone?" # From sample-3.pdf
    question = "Provide me details of Community Business base height?" # From sample-3.pdf
    #question = "What is Air Receiver?" # From sample-4.pdf
    #question = "What is Embodied Intelligence?" #From  sample-5.pdf
    
    # Get response from Claude
    response = extract_pdf_content(question, base64_string)
    
    # Print the response
    print(response)

# Execute main function if script is run directly
if __name__ == "__main__":
    main()