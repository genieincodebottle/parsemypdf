

<div align="center">
    <a target="_blank" href="https://www.youtube.com/@genieincodebottle"><img src="https://img.shields.io/badge/YouTube-@genieincodebottle-blue"></a>&nbsp;
    <a target="_blank" href="https://www.linkedin.com/in/rajesh-srivastava"><img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social"></a>&nbsp;
    <a target="_blank" href="https://www.instagram.com/genieincodebottle/"><img src="https://img.shields.io/badge/@genieincodebottle-C13584?style=flat-square&labelColor=C13584&logo=instagram&logoColor=white&link=https://www.instagram.com/eduardopiresbr/"></a>&nbsp;
    <a target="_blank" href="https://github.com/genieincodebottle/generative-ai/blob/main/GenAI_Roadmap.md"><img src="https://img.shields.io/badge/style--5eba00.svg?label=GenAI Roadmap&logo=github&style=social"></a>
</div>

## 📑 Complex PDF Parsing

A comprehensive example codes for extracting content from PDFs

Also, check -> [Pdf Parsing Guide](https://github.com/genieincodebottle/parse-my-pdf/blob/main/pdf-parsing-guide.pdf)

### 📌 Core Features

#### 📤 Content Extraction
- Multiple extraction methods with different tools/libraries:
  - Cloud-based: Claude 3.5 Sonnet, GPT-4 Vision, Unstructured.io
  - Local: Llama 3.2 11B, Docling, PDFium
  - Specialized: Camelot (tables), PDFMiner (text), PDFPlumber (mixed), PyPdf etc
- Maintains document structure and formatting
- Handles complex PDFs with mixed content including extracting image data


### 📦 Implementation Options

#### 1. ☁️ Cloud-Based Methods
- [Claude 3.5 Sonnet](parser/claude/): Excellent  for complex PDFs with mixed content
- [GPT-4 Vision](parser/openai/): Excellent for visual content analysis
- [Unstructured.io](parser/unstructured-io/): Advanced content partitioning and classification. Unstructured.io specializes in converting unstructured data for LLMs and AI applications. Its open-source Unstructured library processes PDFs, HTML, Word, and images, streamlining data prep for AI. The Enterprise ETL Platform automates data ingestion and cleaning, integrating seamlessly with Generative AI stacks.
- [llama-parse](parser/llama-parse/): LlamaParse is a GenAI-native document parser for LLM applications like RAG and agents. It supports PDFs, PowerPoint, Word, Excel, and HTML, accurately extracting tables, images, and diagrams. It integrates with LlamaIndex for retrieval systems and allows custom parsing via prompts. Free users get 1,000 pages/day, with paid plans offering higher limits and extra features.
- [Amazon Textract](parser/amazon-textract/): Advanced content partitioning and classification. Amazon Textract is an AWS ML service that extracts text, forms, tables, and signatures from scanned documents. It goes beyond OCR by preserving structure for easy data integration. Supporting PNG, JPEG, TIFF, and PDF, it enables automation for data entry, search indexing, and document processing.

#### 2. 🖥️ Local Methods
- [Llama 3.2 11B Vision](parser/llama-vision/): Good for Image-based PDF processing.
- [Docling](parser/docling/): Excellent  for complex PDFs with mixed content. Docling simplifies document processing, parsing diverse formats — including advanced PDF understanding, and providing seamless integrations with the gen AI ecosystem.
- [markitdown](parser/markitdown/) : Excellent  for complex PDFs with mixed content. MarkItDown is a utility for converting various files to Markdown (e.g., for indexing, text analysis, etc). It supports: PDF, PowerPoint, Word, Excel, Images (EXIF metadata and OCR), Audio (EXIF metadata and speech transcription), HTML, Text-based formats (CSV, JSON, XML), ZIP files (iterates over contents)
- [Marker](https://github.com/VikParuchuri/marker) : Marker quickly converts PDFs and images to Markdown, JSON, and HTML with high accuracy. It supports all languages and document types while handling tables, forms, math, links, and code blocks. It extracts images, removes artifacts, and allows customization with user-defined formatting and logic. Accuracy can be enhanced with LLM integration, and it runs on GPU, CPU, or MPS. Code is not included here but can be checked on their GitHub repo.
- [Camelot](parser/camelot/): Specialized table extraction. Camelot is a Python library for extracting tables from text-based PDFs using "Lattice" (grid-based) and "Stream" (whitespace-based) methods. It outputs tables as pandas DataFrames and supports CSV, JSON, Excel, and more. A CLI is available, and Excalibur provides a web-based interface for easy table extraction.
- [PyPdf](parser/pypdf/): pypdf is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. pypdf can retrieve text and metadata from PDFs as well.
- [PDFMiner](parser/pdfminer/): Basic text and layout extraction. PDFMiner is a Python library for extracting text and layout details from PDFs, supporting various fonts and complex layouts. It enables conversion to HTML/XML and automatic layout analysis. Since version 20191010, it supports only Python 3, with pdfminer.six available for Python 2.
- [PDFPlumber](parser/pdfplumber/): Basic text and layout extraction. PDFPlumber extends pdfminer.six for PDF data extraction, handling text, tables, and shapes with visual debugging. It excels at extracting tables into pandas DataFrames while preserving layout but lacks OCR for scanned documents.
- [PyMUPDF](parser/pymupdf/): PyMuPDF is a fast Python library for extracting, analyzing, converting, and manipulating PDFs, XPS, and eBooks. It supports text/image extraction, rendering to PNG/SVG, and conversion to HTML, XML, and JSON, making it ideal for high-speed document processing.
- [pdfium](parser/pypdfmium/): PDFium is Google's open-source C++ library for viewing, parsing, and rendering PDFs. It powers Chromium, enabling text extraction, metadata access, and page rendering. Designed for performance, it's ideal for desktop and server applications.
- [PyPdfDirectory](parser/pypdfdirectory/): Batch PDF Content Extraction Script using PyPDF2 Directory Loader.


### 🔗 Dependencies

#### 📚 Python Libraries
```bash
# PDF Processing Libraries
pypdf
pymupdf
pdfplumber
PyPDF2<3.0
camelot-py[cv]
Ghostscript
docling # IBM's Opensource
markitdown # Microsoft's Opensource 

# Computer Vision
opencv-python

# LLM related Libraries
ollama
tiktoken
openai
anthropic
langchain_ollama
langchain_huggingface
langchain_community

# Vector Store and Embeddings
faiss-cpu
sentence_transformers

# AWS Libraries
boto3
amazon-textract-caller>=0.2.0

# Utilities
python-dotenv
```

### ⚙️ Setup Instructions

- #### Prerequisites
   - Python 3.9 or higher
   - pip (Python package installer)

- #### Installation
   1. Clone the repository:
      ```bash
      git clone https://github.com/genieincodebottle/genaicodelab.git
      cd parsemypdf
      ```
   2. Create a virtual environment:
      ```bash
      python -m venv venv
      venv\Scripts\activate # On Linux -> source venv/bin/activate
      ```
   3. Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```
   4. Environment Variables
      ```bash
      ANTHROPIC_API_KEY=your_key_here    # For Claude
      OPENAI_API_KEY=your_key_here       # For OpenAI
      UNSTRUCTURED_API_KEY=your_key_here # For Unstructured.io
      LLAMA_CLOUD_API_KEY=your_key_here # For llama-parse
      ```

      For **ANTHROPIC_API_KEY** follow this -> https://console.anthropic.com/settings/keys

      For **OPENAI_API_KEY** follow this -> https://platform.openai.com/api-keys

      For **UNSTRUCTURED_API_KEY** follow this -> https://unstructured.io/api-key-free

      For **LLAMA_CLOUD_API_KEY** follow this -> https://cloud.llamaindex.ai/api-key

  5. Install Ollama & Models (for local processing)
      - Install Ollama
         - For Window - Download the Ollama from following location (Requires Window 10 or later) -> https://ollama.com/download/windows
         - For Linux (command line) - curl https://ollama.ai/install.sh | sh

      - Pull required models (command line)
         - ollama pull llama3.1
         - ollama pull x/llama3.2-vision:11b

### 📈 Usage

1. Place PDF files in `input/` directory
2. You can run and test different type of parser available in "parser" folder.

### 📄 Example Complex Pdf placed in Input folder(You can use your own pdf)
- **sample-1.pdf**: Standard tables
- **sample-2.pdf**: Image-based simple tables
- **sample-3.pdf**: Image-based complex tables
- **sample-4.pdf**: Mixed content (text, tables, images)
- **sample-5.pdf**: Multi-column Texts 
   
### 📝 Important Notes
- System resources needed for local LLM operations
- API keys required for cloud based implementations
- Consider PDF complexity when choosing implementation
- Ghostscript required for Camelot
- Different processors suit different use cases
  - **Cloud**: Complex documents, mixed content
  - **Local**: Simple text, basic tables
  - **Specialized**: Specific content types (tables, forms)