"""
PDF Content Extraction and Question Answering System with Docling

This script implements a local document processing and question answering system using Docling 
for PDF extraction and LangChain components for text processing and retrieval. It provides a 
complete pipeline for extracting, processing, and querying PDF content without relying on 
cloud-based services.

Key Features:
    - PDF Processing:
        - Uses Docling for robust PDF content extraction
        - Maintains document structure and formatting
        - Converts content to markdown format
        - Handles various PDF types including tables and images
        
    - Text Processing:
        - Implements chunk-based text splitting for optimal processing
        - Creates embeddings using Huggingface's sentence transformers
        - Utilizes FAISS for vector storage and retrieval
        
    - Question Answering:
        - Local LLM-based question answering using llama 3.1 8B via Ollama
        - Custom prompt engineering for focused responses

Dependencies:
    - docling: For PDF content extraction
    - langchain_ollama: For local LLM integration
    - langchain_huggingface: For text embeddings
    - langchain_community: For vector store operations
    - langchain.text_splitter: For text chunking
    - langchain.chains: For QA chain implementation
    - langchain.prompts: For prompt templating

Models Used:
    - Embeddings: sentence-transformers/all-MiniLM-L12-v2
    - Question Answering: llama3.1 8B (via Ollama)

Usage:
    Place PDF files in the 'input/' directory. Supports various PDF types:
    - sample-1.pdf: Standard tables
    - sample-2.pdf: Image-based simple tables
    - sample-3.pdf: Image-based complex tables
    - sample-4.pdf: Mixed content (text, tables, images)
    - sample-5.pdf: Multi-column Texts 

Note: This implementation runs entirely locally and doesn't require API keys
or cloud services, but needs sufficient system resources for LLM operations.
"""
import os
from typing import List
from docling.document_converter import DocumentConverter  # For PDF content extraction
from langchain_ollama.llms import OllamaLLM  # Local LLM integration
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For text chunking
from langchain_huggingface import HuggingFaceEmbeddings  # For text embeddings
from langchain_community.vectorstores import FAISS  # Vector database
from langchain.chains import RetrievalQA  # For question-answering pipeline
from langchain.prompts import PromptTemplate  # For customizing LLM prompts

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def extract_pdf_content(file_path) -> str:
    """
    Extract structured content from PDF using Docling library
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted content in markdown format
    """
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return result.document.export_to_markdown()

def create_vector_store(texts: List[str]) -> FAISS:
    """
    Create and initialize FAISS vector store using text embeddings
    
    Args:
        texts (List[str]): List of text chunks to be embedded
        
    Returns:
        FAISS: Initialized FAISS vector store containing embedded texts
    """
    # Initialize sentence transformer model for text embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store

def get_qa_chain(vector_store):
    """
    Create question-answering chain using LLM and vector store
    
    Args:
        vector_store (FAISS): Vector store containing embedded documents
        
    Returns:
        RetrievalQA: Configured QA chain for answering questions
    """
    # Initialize local LLM using Ollama
    llm = OllamaLLM(model="llama3.1")
    
    # Define custom prompt template for better QA responses
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
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    # Configure QA chain with retrieval and prompt settings
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Combines all retrieved docs into single context
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),  # Retrieve top 3 relevant chunks
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,  # Include source documents in response
    )
    return qa_chain

def main():
    """
    Main function to orchestrate the PDF processing and QA pipeline
    
    Workflow:
    1. Extract content from PDF
    2. Split content into manageable chunks
    3. Create vector store with embeddings
    4. Set up QA chain and process questions
    """
    # STEP 1: Extract PDF content as text using Claude 3.5 Sonnet API
    # Different PDF types for testing
    #file_path = project_root+"/input/sample-1.pdf" # Table in pdf
    #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
    #file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
    file_path = project_root+"/input/sample-4.pdf"  # Complex PDF with text and tables in images
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 
    
    structured_content = extract_pdf_content(file_path)
    # Output extracted content to output.txt
    with open("output.txt", 'w') as file:
        file.write(structured_content)
    
    # STEP 2: Split extracted PDF text into smaller chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # Maximum chunk size in characters
        chunk_overlap=100,  # Overlap between chunks to maintain context
        is_separator_regex=False
    )
    text_chunks = text_splitter.split_text(structured_content)
    
    # STEP 3: Create vector store with embeddings for semantic search
    vector_store = create_vector_store(text_chunks)
    
    # STEP 4: Initialize QA chain for processing questions
    qa_chain = get_qa_chain(vector_store)
    
    # Sample questions for testing
    #question = "What is maximum lot depth/width of commercial zone?" # From sample-3.pdf
    #question = "Provide me details of Community Business base height?" # From sample-3.pdf
    #question = "What is Air Receiver?" # From sample-4.pdf
    question = "What is Embodied Intelligence?" # From sample-5.pdf
    
    print(f"\nQuestion: {question}")
    response = qa_chain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")

if __name__ == "__main__":
    main()