"""
Advanced PDF Processing and Question-Answering System

This script implements a sophisticated PDF processing pipeline that combines computer vision 
and natural language processing to extract and analyze PDF content. It uses GPT-4 Vision 
for visual content extraction and implements a question-answering system.

Key Components:
    1. PDF Processing:
        - Converts PDFs to images
        - Uses GPT-4 Multimodal for text/table extraction
        - Preserves document structure and formatting
    
    2. Question-Answering System:
        - Text chunking and embedding
        - Vector-based retrieval
        - Contextual question answering
        
Dependencies:
    - openai: For GPT-4 Multimodal API
    - python-dotenv: Environment variable management
    - langchain & related: For LLM and embedding operations
    - FAISS: For vector similarity search
    - Custom utils: For PDF-to-image conversion

Environment Setup:
    Requires:
        - OpenAI API key in .env file
        - Local Ollama installation
        - Access to HuggingFace models
"""
import sys
import os
import base64
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_ollama.llms import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from utils.pdf_to_image import PDFToJPGConverter

# Initialize environment variables from .env file
load_dotenv()

# Validate and set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables")
os.environ["API_KEY"] = OPENAI_API_KEY

def encode_image_to_base64(image_path):
    """
    Convert an image file to base64 encoding.

    Args:
        image_path (str or Path): Path to the image file

    Returns:
        str: Base64 encoded string of the image

    Raises:
        FileNotFoundError: If the image file doesn't exist
        IOError: If there's an error reading the file
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_completion_response(client, base64_image):
    """
    Send a request to GPT-4 Vision API to extract text and tables from an image.

    Args:
        client (OpenAI): Initialized OpenAI client
        base64_image (str): Base64 encoded image string

    Returns:
        Response: OpenAI API response containing extracted text

    Note:
        The function is configured to extract both plain text and tables,
        maintaining the original structure and formatting tables in Markdown.
    """
    response = client.chat.completions.create(
        model="gpt-4.1-2025-04-14", #gpt-4.1-mini-2025-04-14, #gpt-4o-mini, #gpt-4o-2024-08-06, #gpt-4o-mini-2024-07-18
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Extract all the text content, including both plain text and tables, from the 
                        provided document or image. Maintain the original structure, including headers, 
                        paragraphs, and any content preceding or following the table. Format the table in 
                        Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
                        including any introductory or explanatory text before or after the table.""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )
    return response


def create_vector_store(texts: List[str]) -> FAISS:
    """
    Create and initialize a FAISS vector store using text embeddings.

    This function performs the following steps:
    1. Initializes the HuggingFace embeddings model
    2. Converts input texts into vector embeddings
    3. Creates a FAISS index for efficient similarity search

    Args:
        texts (List[str]): List of text documents to be embedded and stored

    Returns:
        FAISS: Initialized FAISS vector store containing the embedded texts

    Note:
        Uses the 'all-MiniLM-L12-v2' model which is optimized for sentence embeddings
        and provides a good balance between performance and accuracy
    """
    # Initialize the embedding model from HuggingFace
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    
    # Create FAISS vector store from texts using the embeddings
    vector_store = FAISS.from_texts(texts, embeddings)
    
    return vector_store

def get_qa_chain(vector_store):
    """
    Create a question-answering chain using the provided vector store.

    This function sets up a complete QA pipeline that:
    1. Uses Llama 3.1 as the base language model
    2. Implements a custom prompt template for controlled responses
    3. Configures a retrieval-based QA system with specific search parameters

    Args:
        vector_store (FAISS): The vector store containing embedded documents

    Returns:
        RetrievalQA: Configured QA chain ready for question answering

    Note:
        - The chain is configured to retrieve 3 most relevant documents (k=3)
        - The prompt template ensures step-by-step thinking and accurate responses
        - The chain returns source documents along with answers for transparency
    """
    # Initialize Llama 3.1 language model
    llm = OllamaLLM(model="llama3.1")

    # Define custom prompt template for controlled and accurate responses
    prompt_template = """
        Use the following pieces of context to answer the question at the end.
        
        Check context very carefully and reference and try to make sense of that before responding.
        If you don't know the answer, just say you don't know.
        Don't try to make up an answer.
        Answer must be to the point.
        Think step-by-step.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""

    # Create PromptTemplate object with defined variables
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    # Initialize and configure the QA chain with:
    # - Specified language model
    # - "stuff" chain type (loads all relevant contexts at once)
    # - Vector store retriever with top-3 document retrieval
    # - Custom prompt template
    # - Source document return enabled
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
    )

    return qa_chain


def main():
    """
    Main execution function implementing a complete PDF processing and Q&A pipeline.

    The pipeline consists of two major phases:
    
    Phase 1 - PDF Processing:
    1. PDF to Image Conversion
        - Converts PDF pages to JPG images
        - Handles various PDF types (simple tables, complex tables, mixed content)
    2. Text Extraction
        - Uses GPT-4 Vision to extract text from images
        - Maintains formatting and structure of content
        
    Phase 2 - Question Answering:
    1. Text Processing
        - Splits extracted text into manageable chunks
        - Maintains context with chunk overlap
    2. Vector Database Creation
        - Creates embeddings for text chunks
        - Builds searchable vector store
    3. Q&A Implementation
        - Sets up retrieval-based QA system
        - Processes queries and returns relevant answers

    """
    # PHASE 1: PDF PROCESSING AND TEXT EXTRACTION
    
    # Initialize OpenAI client for GPT-4 Vision API
    client = OpenAI()

    # Configure input PDF path
    # Different sample types available for processing:
    #file_path = project_root+"/input/sample-1.pdf"  # Simple table-based PDF
    #file_path = project_root+"/input/sample-2.pdf"  # PDF with image-based simple tables
    file_path = project_root+"/input/sample-3.pdf"   # PDF with complex image-based tables
    #file_path = project_root+"/input/sample-4.pdf"  # PDF with mixed content types
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts

    # Set up PDF to image conversion
    converter = PDFToJPGConverter()
    output_path = project_root+"/converted_images/llama"  # Directory for converted images

    # Execute PDF to JPG conversion
    converted_files = converter.convert_pdf(file_path, output_path)

    # Display conversion results
    print("\nConversion Summary:")
    print(f"Total pages converted: {len(converted_files)}")
    print("\nConverted files:")
    for file in converted_files:
        print(f"- {file}")

    # Process and extract text from converted images
    directory = Path(output_path)
    final_response = ""

    # Iterate through converted images
    for image_path in directory.iterdir():
        # Convert image to base64 for API compatibility
        base64_image = encode_image_to_base64(image_path)
        # Extract text using GPT-4 Vision
        response = get_completion_response(client, base64_image)
        # Accumulate extracted text
        final_response += response.choices[0].message.content + "\n"

    # Display complete extracted content
    print("#### Extracted Response ####")
    print(final_response)

    # PHASE 2: QUESTION ANSWERING SETUP

    # Initialize text splitting with specific parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,      # Size of each text chunk
        chunk_overlap=100,    # Overlap between chunks to maintain context
        is_separator_regex=False
    )
    # Split extracted text into manageable chunks
    text_chunks = text_splitter.split_text(response)

    # Create vector store for semantic search
    vector_store = create_vector_store(text_chunks)

    # Initialize question-answering chain
    qa_chain = get_qa_chain(vector_store)

    # Example questions for different document types
    #question = "What is maximum lot depth/width of commercial zone?" # From sample-3.pdf
    question = "Provide me details of Community Business base height?" # From sample-3.pdf
    #question = "What is Air Receiver?" # From sample-4.pdf
    #question = "What is Embodied Intelligence?" # From sample-5.pdf
    
    # Process question and generate answer
    print(f"\nQuestion: {question}")
    response = qa_chain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")


if __name__ == "__main__":
    main()
