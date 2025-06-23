"""
PDF Content Extraction and Question Answering System with RAG Architecture

This script implements a Retrieval-Augmented Generation (RAG) system for processing PDFs and answering
questions about their content. It combines Claude's PDF extraction capabilities with local LLM inference
using Ollama, vector storage, and efficient text retrieval.

Key Features:
    - PDF Processing: 
        - Extracts content from complex PDFs including tables, images, and text
        - Handles PDFs in chunks for efficient processing
        - Maintains document structure and formatting
        
    - Text Processing:
        - Implements recursive text splitting for optimal chunk sizes
        - Creates embeddings using Hugging Face's sentence transformers
        - Stores vectorized text chunks in FAISS for efficient retrieval
        
    - Question Answering:
        - Uses RAG architecture for accurate responses
        - Combines local LLM (llama3.1) with vector retrieval
        - Custom prompt templates for focused answers
        - Returns source context for answer verification

Dependencies:
    - anthropic: For Claude API integration
    - langchain_ollama: For local LLM integration
    - langchain_huggingface: For text embeddings
    - langchain_community: For vector store (FAISS)
    - python-dotenv: For environment variable management
    - typing: For type hints
    
Required Environment Variables:
    - ANTHROPIC_API_KEY: API key for Claude services

Models Used:
    - Text Extraction: claude-3-7-sonnet-20250219
    - Embeddings: sentence-transformers/all-MiniLM-L12-v2
    - Question Answering: llama3.1 8B(via Ollama)

Usage:
    Place PDF files in the 'input/' directory. Supports various PDF types:
    - sample-1.pdf: Standard tables
    - sample-2.pdf: Image-based simple tables
    - sample-3.pdf: Image-based complex tables
    - sample-4.pdf: Mixed content (text, tables, images)
    - sample-5.pdf: Multi-column Texts 

Note: Requires sufficient system resources for running local LLM and vector operations
"""

import sys
import os
from typing import List
from dotenv import load_dotenv

import anthropic

from langchain_ollama.llms import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

import utils.utils as utils

# Load environment variables
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in environment variables")


def get_completion(client, messages, model_name):
    """Call the claude model to extract text from the Complex PDF"""
    return (
        client.messages.create(model=model_name, max_tokens=8096, messages=messages)
        .content[0]
        .text
    )


def extract_pdf_content(pdf_base64_string) -> str:
    """Extract structured content from PDF using Claude API"""

    client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

    system_prompt = """You are an expert at extracting and structuring content from complex PDFs, which contain tables, images and text. 
    Please scan the pdf deeply and extract every text content from the provided PDF, maintaining the structure and formatting.
    Format tables properly in markdown format. In case of tables, preserve all numerical data and relationships between elements.
    Do not exclude any content from the pdf"""

    model_name = "claude-sonnet-4-20250514"
    #model_name = "claude-opus-4-20250514"
    #model_name = "claude-3-7-sonnet-latest"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64_string,
                    },
                },
                {"type": "text", "text": system_prompt},
            ],
        }
    ]
    response = get_completion(client, messages, model_name)
    print(f"Response: {response}")
    return response


def create_vector_store(texts: List[str]) -> FAISS:
    """Create and save vector store"""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


def get_qa_chain(vector_store):

    llm = OllamaLLM(model="llama3.1")

    # Create custom prompt template
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

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
    )
    return qa_chain


def main():

    # STEP 1: Read the PDF and base64 encoding

    #file_path = project_root+"/input/sample-1.pdf" # Table in pdf
    #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
    #file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
    file_path = project_root+"/input/sample-4.pdf"  # Complex PDF where many text contents and tables are in image 
    base64_encoded_list = utils.read_pdf_in_pairs(file_path)
    
    # STEP 2: Extract PDF content as text using Claude 3.7 Sonnet API
    structured_content = ""
    for content in base64_encoded_list:
        structured_content += "\n" + extract_pdf_content(content)
    
    # Output extracted content to output.txt
    with open("output.txt", 'w') as file:
        file.write(structured_content)

    # STEP 3: Split & chunk extracted PDF text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=100, is_separator_regex=False
    )
    text_chunks = text_splitter.split_text(structured_content)

    # STEP 4: Create vector store with embeddings
    vector_store = create_vector_store(text_chunks)

    # STEP 5: Create QA chain & get response of question
    qa_chain = get_qa_chain(vector_store)

    #question = "What is maximum lot depth/width of commercial zone?" # From sample-3.pdf
    #question = "Provide me details of Community Business base height?" # From sample-3.pdf
    question = "What is Air Receiver?" # From sample-4.pdf
    print(f"\nQuestion: {question}")
    response = qa_chain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")

    # print("\nSource Documents:")
    # for doc in response["source_documents"]:
    #    print(f"- {doc.page_content[:200]}...")

if __name__ == "__main__":
    main()
