import torch
# To override warning related torch path reload when using streamlit 
torch.classes.__path__ = []

# Standard Library Imports
import os
import json
import logging
import base64
from datetime import datetime
from typing import List
import uuid
import io

# Environment Variables
from dotenv import load_dotenv

# Streamlit
import streamlit as st

# AI/LLM Clients
import ollama
import anthropic
from openai import OpenAI
from google import genai
from google.genai import types
from mistralai import Mistral

# LangChain Core
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# LangChain Integrations
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# LangChain Chains & Vector Stores
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Document Loaders
from langchain_community.document_loaders import (
    PDFMinerLoader,
    PDFPlumberLoader,
    PyMuPDFLoader,
    PyPDFLoader,
)
import camelot
from docling.document_converter import DocumentConverter
from markitdown import MarkItDown

# AWS Services
import boto3

# Utilities
from utils.pdf_to_image import PDFToJPGConverter


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOGGING_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# LLM Provider Configurations
LLM_CONFIGS = {
    "Groq": {
        "models": [
            "llama3-8b-8192",
            "llama3-70b-8192",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ],
        "requires_key": "GROQ_API_KEY"
    },
    "OpenAI": {
        "models": [
            "gpt-4.1-2025-04-14",
            "gpt-4.1-mini-2025-04-14",
            "gpt-4o-2024-08-06",
            "gpt-4o-mini-2024-07-18"
        ],
        "requires_key": "OPENAI_API_KEY"
    },
    "Anthropic": {
        "models": [
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
            "claude-3-7-sonnet-latest",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
        ],
        "requires_key": "ANTHROPIC_API_KEY"
    },
    "Gemini": {
        "models": [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite-preview-06-17",
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite"
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro"
        ],
        "requires_key": "GOOGLE_API_KEY"
    }
}

# Parser Configurations
PARSER_CONFIGS = {
    "Docling": {
        "description": "Advanced document understanding",
        "requires_api_key": None
    },
    "MarkItDown": {
        "description": "Converts PDFs to markdown format",
        "requires_api_key": None
    },
    "Gemini 2.0": {
        "description": "Uses Gemini's native PDF processing capabilities",
        "requires_api_key": "GOOGLE_API_KEY"
    },
    "Claude": {
        "description": "Uses Claude's native PDF processing capabilities",
        "requires_api_key": "ANTHROPIC_API_KEY"
    },
    "OpenAI": {
        "description": "Uses GPT-4o for processing PDFs",
        "requires_api_key": "OPENAI_API_KEY"
    },
    "Mistral-OCR": {
        "description": "Uses Mistral-OCR for processing PDFs",
        "requires_api_key": "MISTRAL_API_KEY"
    },
    "Camelot": {
        "description": "Specialized in table extraction",
        "requires_api_key": None
    },
    "PyPDF": {
        "description": "Simple text extraction",
        "requires_api_key": None
    },
    "PDFPlumber": {
        "description": "Good for text and simple tables",
        "requires_api_key": None
    },
    "PDFMiner": {
        "description": "Basic text extraction with layout preservation",
        "requires_api_key": None
    },
    "PyMuPDF": {
        "description": "Fast processing with good layout preservation",
        "requires_api_key": None
    },
    "Amazon Textract": {
        "description": "AWS service for document processing",
        "requires_api_key": "AWS_ACCESS_KEY_ID"
    },
    "Llama Vision": {
        "description": "Uses Llama 3.2 Vision model",
        "requires_api_key": None
    }
}

class RAGSystem:
    """Handles RAG functionality with different LLM providers"""
    def __init__(self, provider: str, model: str, temperature: float = 0.7):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L12-v2"
        )
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the appropriate LLM based on provider"""
        try:
            if self.provider == "Groq":
                os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
                return ChatGroq(temperature=self.temperature, model_name=self.model)
            elif self.provider == "OpenAI":
                os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
                return ChatOpenAI(model_name=self.model, temperature=self.temperature)
            elif self.provider == "Anthropic":
                os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
                return ChatAnthropic(model_name=self.model, temperature=self.temperature)
            elif self.provider == "Gemini":
                os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
                return ChatGoogleGenerativeAI(model=self.model, temperature=self.temperature)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.error(f"Error initializing LLM for {self.provider}: {str(e)}", exc_info=True)
            raise
    
    def create_vector_store(self, texts: List[str]) -> FAISS:
        return FAISS.from_texts(texts, self.embeddings)
    
    def setup_qa_chain(self, vector_store):
        
        system_prompt = (
            """Use the following pieces of context to answer the question at the end. 
            Check context very carefully and reference and try to make sense of that before responding.
            If you don't know the answer, just say you don't know. 
            Don't try to make up an answer.
            Answer must be to the point.
            Think step-by-step.
            Context: {context}"""
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # Create retriever
        retriever = vector_store.as_retriever()

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        qa_chain = create_retrieval_chain(retriever, question_answer_chain)

        return qa_chain

class MultiParser:
    """Handles multiple PDF parsing methods"""
    def __init__(self, parser_name: str):
        self.parser_name = parser_name
        self.image_converter = PDFToJPGConverter()

    def parse_pdf(self, uploaded_file) -> str:
        pdf_content = uploaded_file.read()
        logger.debug(f"Parsing PDF with {self.parser_name}")
        try:
            if self.parser_name == "Docling":
                return self._parse_with_docling(pdf_content)
            elif self.parser_name == "MarkItDown":
                return self._parse_with_markitdown(pdf_content)
            elif self.parser_name == "Gemini 2.0":
                return self._parse_with_gemini(pdf_content)
            elif self.parser_name == "Claude":
                return self._parse_with_claude(pdf_content)
            elif self.parser_name == "OpenAI":
                return self._parse_with_openai_vision(pdf_content)
            elif self.parser_name == "Mistral-OCR":
                return self._parse_with_mistral_ocr(uploaded_file)
            elif self.parser_name == "Camelot":
                return self._parse_with_camelot(pdf_content)
            elif self.parser_name == "PyPDF":
                return self._parse_with_pypdf(pdf_content)
            elif self.parser_name == "PDFPlumber":
                return self._parse_with_pdfplumber(pdf_content)
            elif self.parser_name == "PDFMiner":
                return self._parse_with_pdfminer(pdf_content)
            elif self.parser_name == "PyMuPDF":
                return self._parse_with_pymupdf(pdf_content)
            elif self.parser_name == "Amazon Textract":
                return self._parse_with_textract(pdf_content)
            elif self.parser_name == "Llama Vision":
                return self._parse_with_llama_vision(pdf_content)
            else:
                raise ValueError(f"Unsupported parser: {self.parser_name}")
        except Exception as e:
            logger.error(f"Error parsing PDF with {self.parser_name}: {str(e)}", exc_info=True)
            raise
    
    def _parse_with_gemini(self, pdf_content: bytes) -> str:
        api_key=os.getenv("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key)
    
        prompt = """Extract all the text content, including both plain text and tables, from the 
                provided document or image. Maintain the original structure, including headers, 
                paragraphs, and any content preceding or following the table. Format the table in 
                Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
                including any introductory or explanatory text before or after the table."""
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=pdf_content,
                    mime_type='application/pdf',
                ),
                prompt])
        return response.text
    
    def _parse_with_claude(self, pdf_content: bytes) -> str:
        api_key=os.getenv("ANTHROPIC_API_KEY")
        client = anthropic.Client(api_key=api_key, default_headers={"anthropic-beta": "pdfs-2024-09-25"})
    
        base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
        
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": base64_pdf
                    }
                },
                {
                    "type": "text",
                    "text": """Extract all the text content, including both plain text and tables, from the 
                            provided document or image. Maintain the original structure, including headers, 
                            paragraphs, and any content preceding or following the table. Format the table in 
                            Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
                            including any introductory or explanatory text before or after the table."""
                }
            ]
        }]
        
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1500,
            messages=messages
        )
        return response.content[0].text

    def _parse_with_openai_vision(self, pdf_content: bytes) -> str:
        """
        Parse PDF using OpenAI's Vision model, handling the content as bytes.
        
        Args:
            pdf_content (bytes): The PDF content as bytes
            
        Returns:
            str: Extracted text from the PDF
        """
        client = OpenAI()
        output_path = f"converted_images/ui/{str(uuid.uuid4())}"
        
        # Convert PDF pages to images (keeping in memory)
        images = self.image_converter.convert_pdf(
            pdf_input=pdf_content,
            output_dir=output_path,
            save_to_disk=False
        )
        
        full_text = ""
        
        for img in images:
            # Convert PIL Image to base64
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            base64_img = base64.b64encode(img_byte_arr).decode('utf-8')
            
            # Process with OpenAI Vision
            response = client.chat.completions.create(
                model="gpt-4o",
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
                                        including any introductory or explanatory text before or after the table."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_img}"
                                }
                            }
                        ]
                    }
                ]
            )
            full_text += response.choices[0].message.content + "\n\n"
        
        return full_text

    def _parse_with_mistral_ocr(self, uploaded_file) -> str:
        api_key=os.getenv("MISTRAL_API_KEY")
        client = Mistral(api_key=api_key)
        uploaded_pdf = client.files.upload(
                file={
                        "file_name": uploaded_file.name,
                        "content": uploaded_file.getvalue(),
                    },
                    purpose="ocr"
                ) 
        signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id).url
        
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": signed_url,
            },
            include_image_base64=True,
            )
        final_response = ""
        
        for page in ocr_response.pages:
            final_response += page.markdown + "\n"
        
        return final_response
    
    def _parse_with_camelot(self, pdf_content: bytes) -> str:
        # Save PDF content temporarily
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        # Extract tables
        tables = camelot.read_pdf("temp.pdf")
        
        # Convert tables to markdown format
        text = ""
        for i, table in enumerate(tables):
            text += f"\nTable {i+1}:\n"
            text += table.df.to_markdown()
            text += "\n"
        
        # Cleanup
        os.remove("temp.pdf")
        return text

    def _parse_with_pdfminer(self, pdf_content: bytes) -> str:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        loader = PDFMinerLoader("temp.pdf")
        documents = loader.load()
        
        os.remove("temp.pdf")
        return "\n\n".join(doc.page_content for doc in documents)

    def _parse_with_pdfplumber(self, pdf_content: bytes) -> str:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        loader = PDFPlumberLoader("temp.pdf")
        documents = loader.load()
        
        os.remove("temp.pdf")
        return "\n\n".join(doc.page_content for doc in documents)

    def _parse_with_pymupdf(self, pdf_content: bytes) -> str:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        loader = PyMuPDFLoader("temp.pdf")
        documents = loader.load()
        
        os.remove("temp.pdf")
        return "\n\n".join(doc.page_content for doc in documents)

    def _parse_with_pypdf(self, pdf_content: bytes) -> str:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        loader = PyPDFLoader("temp.pdf")
        documents = loader.load()
        
        os.remove("temp.pdf")
        return "\n\n".join(doc.page_content for doc in documents)

    def _parse_with_docling(self, pdf_content: bytes) -> str:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        converter = DocumentConverter()
        result = converter.convert("temp.pdf")
        
        os.remove("temp.pdf")
        return result.document.export_to_markdown()

    def _parse_with_markitdown(self, pdf_content: bytes) -> str:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_content)
        
        md = MarkItDown()
        result = md.convert("temp.pdf")
        
        os.remove("temp.pdf")
        return result.text_content

    def _parse_with_textract(self, pdf_content: bytes) -> str:
        textract = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="us-east-1"
        )
        
        response = textract.detect_document_text(
            Document={'Bytes': pdf_content}
        )
        
        return "\n".join(item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE')

    def _parse_with_llama_vision(self, pdf_content: bytes) -> str:
        output_path = f"converted_images/ui/{str(uuid.uuid4())}"
        images = self.image_converter.convert_pdf(pdf_content, output_path)
        full_text = ""
        
        for img in images:
            # Convert PIL Image to base64
            import io
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            base64_img = base64.b64encode(img_byte_arr).decode('utf-8')
            
            response = ollama.chat(
                model='x/llama3.2-vision:11b',
                messages=[{
                    'role': 'user',
                    'content': 'Extract all text content from this image.',
                    'images': [base64_img]
                }]
            )
            full_text += response.message.content + "\n\n"
        
        return full_text

def main():
    st.set_page_config(page_title="Pdf Parsing & RAG Evaluator", page_icon="📚", layout="wide")
    st.subheader("📚 Pdf Parsing & RAG Evaluator")
    
    # Initialize session state
    if 'processed_chunks' not in st.session_state:
        st.session_state.processed_chunks = None
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.7

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        llm_provider = st.selectbox(
            "LLM Provider",
            options=list(LLM_CONFIGS.keys())
        )

        # Check if API key is set for selected provider
        if LLM_CONFIGS[llm_provider].get("requires_key"):
            key_name = LLM_CONFIGS[llm_provider]["requires_key"]
            if not os.getenv(key_name):
                st.warning(f"⚠️ {key_name} not set")

        model_name = st.selectbox(
            "Model",
            options=LLM_CONFIGS[llm_provider]["models"]
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1
        )
        st.session_state.temperature = temperature
        st.markdown("---")
        # Parser Configuration
        st.subheader("📄 Parser Settings")
        parser_name = st.selectbox(
            "Select Parser",
            options=list(PARSER_CONFIGS.keys()),
            help="Choose the method to extract text from your PDF"
        )

        # Show parser description
        st.info(PARSER_CONFIGS[parser_name]["description"])

        # Check if required API key is set
        required_key = PARSER_CONFIGS[parser_name]["requires_api_key"]
        if required_key and not os.getenv(required_key):
            st.warning(f"⚠️ {required_key} not set. This parser may not work.")

        st.markdown("---")

        # Text Chunking Configuration
        st.subheader("📝 Chunking Settings")
        chunk_size = st.slider(
            "Chunk Size",
            min_value=500,
            max_value=4000,
            value=2000,
            step=100
        )

        chunk_overlap = st.slider(
            "Chunk Overlap",
            min_value=0,
            max_value=500,
            value=100,
            step=50
        )

        st.markdown("---")
        
        # Debug Options
        st.subheader("🔧 Debug Options")
        show_debug = st.checkbox(
            "Show Debug Info",
            value=False,
            help="Display detailed processing information"
        )

    # Main content area
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        if st.button("Process PDF"):
            try:
                with st.spinner(f"Processing PDF using {parser_name}..."):
                    # Create progress tracking
                    progress_text = st.empty()
                    progress_bar = st.progress(0)

                    # Initialize parser and RAG system
                    progress_text.text("Initializing systems...")
                    progress_bar.progress(0.1)

                    parser = MultiParser(parser_name)
                    rag_system = RAGSystem(llm_provider, model_name, temperature)
                    # Parse PDF
                    progress_text.text("Extracting text from PDF...")
                    progress_bar.progress(0.3)
                    extracted_text = parser.parse_pdf(uploaded_file)

                    if show_debug:
                        st.text("Extracted text sample:")
                        st.text(extracted_text[:500] + "...")

                    # Split into chunks
                    progress_text.text("Splitting text into chunks...")
                    progress_bar.progress(0.5)
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )
                    chunks = text_splitter.split_text(extracted_text)
                    st.session_state.processed_chunks = chunks

                    # Create vector store
                    progress_text.text("Creating vector store...")
                    progress_bar.progress(0.7)
                    st.session_state.vector_store = rag_system.create_vector_store(chunks)

                    # Setup QA chain
                    progress_text.text("Setting up question-answering system...")
                    progress_bar.progress(0.9)
                    st.session_state.qa_chain = rag_system.setup_qa_chain(st.session_state.vector_store)

                    progress_text.text("Processing complete!")
                    progress_bar.progress(1.0)

                    st.success(f"✅ PDF processed successfully into {len(chunks)} chunks")

                    # Display chunks preview
                    with st.expander("📄 View Processed Chunks"):
                        num_preview = min(3, len(chunks))
                        for i in range(num_preview):
                            st.text_area(
                                f"Chunk {i+1}/{len(chunks)}", 
                                chunks[i],
                                height=150
                            )
                        if len(chunks) > num_preview:
                            st.info(f"... and {len(chunks) - num_preview} more chunks")

            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
                if show_debug:
                    st.exception(e)
                return

        # Question answering interface
        if st.session_state.qa_chain:
            st.subheader("Ask Questions")
            question = st.text_input("Enter your question about the document")

            if st.button("Send") and question:
                try:
                    with st.spinner("Finding answer..."):
                        response = st.session_state.qa_chain.invoke({"input": question})

                        # Display answer
                        st.markdown("### 💡 Answer")
                        st.write(response["answer"])

                        # Show sources
                        with st.expander("🔍 View Source Chunks"):
                            for i, doc in enumerate(response["context"]):
                                st.markdown(f"**Source {i+1}:**")
                                st.text(doc.page_content)
                                st.markdown("---")

                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    if show_debug:
                        st.exception(e)

            # Download processed text
            if st.button("📥 Download Processed Text"):
                try:
                    combined_text = "\n\n".join(st.session_state.processed_chunks)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Create a JSON with metadata
                    download_data = {
                        "metadata": {
                            "timestamp": timestamp,
                            "parser": parser_name,
                            "llm_provider": llm_provider,
                            "model": model_name,
                            "chunk_size": chunk_size,
                            "chunk_overlap": chunk_overlap
                        },
                        "processed_text": combined_text
                    }
                    
                    download_json = json.dumps(download_data, indent=2)
                    
                    st.download_button(
                        "Click to Download",
                        download_json,
                        file_name=f"processed_text_{timestamp}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Error preparing download: {str(e)}")
                    if show_debug:
                        st.exception(e)

if __name__ == "__main__":
    main()