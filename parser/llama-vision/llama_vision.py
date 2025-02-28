"""
This module implements a PDF content extraction and Question-Answering system using LLM models.
It combines multiple AI technologies:
- PDF to Image conversion
- Vision-based text extraction using Llama 3.2
- Text embedding and vector storage
- Question answering using LangChain

The system follows these main steps:
1. Converts PDF pages to images
2. Extracts text content from images using Llama 3.2 vision model
3. Creates embeddings and vector store for efficient text search
4. Implements a QA system using the processed content

Dependencies:
- ollama: For LLM model interactions
- langchain: For creating QA chains and text processing
- FAISS: For vector storage
- PIL: For image processing
- HuggingFace: For text embeddings
"""

import sys
import os
from typing import List
import ollama
import base64
from PIL import Image
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


def encode_image_to_base64(image_path):
    """
    Convert an image file to a base64 encoded string.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def create_vector_store(texts: List[str]) -> FAISS:
    """
    Create and save vector store using FAISS.
    
    Args:
        texts (List[str]): List of text chunks to be embedded
        
    Returns:
        FAISS: Vector store object containing embedded texts
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store


def get_qa_chain(vector_store):
    """
    Create a question-answering chain using LangChain.
    
    Args:
        vector_store: FAISS vector store containing embedded documents
        
    Returns:
        RetrievalQA: QA chain object ready for question answering
    """
    # Initialize Ollama LLM
    llm = OllamaLLM(model="llama3.1")

    # Create custom prompt template with specific instructions
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

    # Create QA chain with specific configuration
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True,
    )
    return qa_chain


def extract_images_content(directory_path):
    """
    Extract text content from all images in the specified directory using Llama vision model.
    
    Args:
        directory_path (str): Path to directory containing images
        
    Returns:
        str: Concatenated text content extracted from all images
    """
    # Currently only supporting JPG files
    image_extensions = ('.jpg')
    final_response = ""

    try:
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"Directory '{directory_path}' does not exist!")
            return
            
        i = 0
        # Process each image file in the directory
        for file_path in directory.iterdir():
            if file_path.suffix.lower() in image_extensions:
                # Convert image to base64 for model input
                base64_image = encode_image_to_base64(file_path)
                
                # Use Llama vision model to extract text content
                response = ollama.chat(
                    model='x/llama3.2-vision:11b',
                    messages=[{
                        'role': 'user',
                        'content': """You are an expert at extracting and structuring content from image. 
                                            Please extract all the text content from the provided image, maintaining the 
                                            structure and formatting of each element.
                                            Format tables properly in markdown format. Preserve all numerical data and 
                                            relationships between elements as given in the images'""",
                        'images': [base64_image]
                        }]
                    )
                i += 1
                print(i)
                final_response += response.message.content + "\n" 
                
        print(final_response)                
        return final_response
    except Exception as e:
        print(f"Error accessing directory: {str(e)}")


def main():
    """
    Main function that orchestrates the PDF processing and QA pipeline:
    1. Converts PDF to images
    2. Extracts text from images using vision model
    3. Creates searchable vector store
    4. Sets up QA system for querying the content
    """
    # Sample PDF files for different use cases
    #file_path = project_root+"/input/sample-1.pdf" # Table in pdf
    #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
    file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
    #file_path = project_root+"/input/sample-4.pdf"  # Complex PDF where many text contents and tables are in image
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 

    # Initialize PDF to JPG converter
    converter = PDFToJPGConverter()
    output_path = "converted_images/llama"
    
    # Convert PDF pages to JPG images
    converted_files = converter.convert_pdf(file_path, output_path)
    
    # Print conversion summary
    print("\nConversion Summary:")
    print(f"Total pages converted: {len(converted_files)}")
    print("\nConverted files:")
    for file in converted_files:
        print(f"- {file}")
    
    # Extract text content from converted images
    response = extract_images_content(output_path)

    # Output extracted content to output.txt
    with open("output.txt", 'w') as file:
        file.write(response)

    # Split extracted text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=100, is_separator_regex=False
    )
    text_chunks = text_splitter.split_text(response)

    # Create vector store for efficient text search
    vector_store = create_vector_store(text_chunks)

    # Initialize QA chain
    qa_chain = get_qa_chain(vector_store)

    # Example questions for different PDF types
    #question = "What is maximum lot depth/width of commercial zone?" # From sample-3.pdf
    question = "Provide me details of Community Business base height?" # From sample-3.pdf
    #question = "What is Air Receiver?" # From sample-4.pdf
    #question = "What is Embodied Intelligence?" # From sample-5.pdf

    # Process question and get answer
    print(f"\nQuestion: {question}")
    response = qa_chain.invoke({"query": question})
    print(f"\nAnswer: {response['result']}")


if __name__ == "__main__":
    main()