# PDF Processing and Question-Answering System

A comprehensive system for extracting content from PDFs and implementing question-answering capabilities using various approaches.

## Core Features

### Content Extraction
- Multiple extraction methods:
  - Cloud-based: Claude 3.5 Sonnet, GPT-4 Vision, Unstructured.io
  - Local: Llama 3.2 Vision, Docling, PDFium
  - Specialized: Camelot (tables), PDFMiner (text), PDFPlumber (mixed)
- Maintains document structure and formatting
- Handles complex PDFs with mixed content
- Supports batch processing of multiple PDFs

### Question-Answering Pipeline
- Implements RAG (Retrieval-Augmented Generation)
- Vector storage using FAISS
- Text embeddings via HuggingFace
- Local inference using Llama 3.1 8B

## Implementation Options

### 1. Cloud-Based Solutions
- **Claude & Llama**: Best for complex PDFs with mixed content
- **GPT-4 Vision**: Excellent for visual content analysis
- **Unstructured.io**: Advanced content partitioning and classification

### 2. Local Solutions
- **Llama Vision**: Image-based PDF processing
- **Docling**: Text-heavy PDFs with formatting preservation
- **PDFium**: High-fidelity processing using Chrome's PDF engine
- **Camelot**: Specialized table extraction
- **PDFMiner/PDFPlumber**: Basic text and layout extraction

## Dependencies

### Core Libraries
```bash
langchain_ollama
langchain_huggingface
langchain_community
FAISS
python-dotenv
```

### Implementation-Specific
```bash
anthropic        # Claude
openai           # GPT-4 Vision
camelot-py      # Table extraction
docling         # Text processing
pdf2image       # PDF conversion
pypdfium2       # PDFium processing
boto3           # AWS Textract
```

## Setup

1. Environment Variables
```bash
ANTHROPIC_API_KEY=your_key_here    # For Claude
OPENAI_API_KEY=your_key_here       # For OpenAI
UNSTRUCTURED_API_KEY=your_key_here # For Unstructured.io
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Install Ollama & Models (for local processing)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.1
ollama pull x/llama3.2-vision:11b
```

## Usage

1. Place PDF files in `input/` directory
2. Choose implementation based on PDF type:
   ```python
   # Cloud-based processing
   from langchain_community.document_loaders import UnstructuredLoader
   loader = UnstructuredLoader("input/sample.pdf", partition_via_api=True)
   
   # Local processing
   from langchain_community.document_loaders import PyPDFium2Loader
   loader = PyPDFium2Loader("input/sample.pdf")
   
   # Batch processing
   from langchain_community.document_loaders import PyPDFDirectoryLoader
   loader = PyPDFDirectoryLoader("input/")
   
   # Load and process
   docs = loader.load()
   ```

## Supported PDF Types
- **sample-1.pdf**: Standard tables
- **sample-2.pdf**: Image-based simple tables
- **sample-3.pdf**: Image-based complex tables
- **sample-4.pdf**: Mixed content (text, tables, images)

## Notes
- System resources needed for local LLM operations
- API keys required for cloud-based implementations
- Consider PDF complexity when choosing implementation
- Ghostscript required for Camelot
- Different processors suit different use cases
  - Cloud: Complex documents, mixed content
  - Local: Simple text, basic tables
  - Specialized: Specific content types (tables, forms)