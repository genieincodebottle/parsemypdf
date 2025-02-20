<div align="center">
<h1><a href="https://www.instagram.com/genieincodebottle/"><img width="200" src="https://github.com/genieincodebottle/generative-ai/blob/main/images/logo_genie_new.png">&nbsp;</a></h1>
</div>
<div align="center">
    <a target="_blank" href="https://www.youtube.com/@genieincodebottle"><img src="https://img.shields.io/badge/YouTube-@genieincodebottle-blue"></a>&nbsp;
    <a target="_blank" href="https://www.linkedin.com/in/rajesh-srivastava"><img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social"></a>&nbsp;
    <a target="_blank" href="https://www.instagram.com/genieincodebottle/"><img src="https://img.shields.io/badge/@genieincodebottle-C13584?style=flat-square&labelColor=C13584&logo=instagram&logoColor=white&link=https://www.instagram.com/eduardopiresbr/"></a>&nbsp;
    <a target="_blank" href="https://github.com/genieincodebottle/generative-ai/blob/main/GenAI_Roadmap.md"><img src="https://img.shields.io/badge/style--5eba00.svg?label=GenAI Roadmap&logo=github&style=social"></a>
</div>

#  

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
- [Unstructured.io](parser/unstructured-io/): Advanced content partitioning and classification
- [Amazon Textract](parser/amazon-textract/): Advanced content partitioning and classification

#### 2. 🖥️ Local Methods
- [Llama 3.2 11B Vision](parser/llama-vision/): Good for Image-based PDF processing.
- [Docling](parser/docling/): Excellent  for complex PDFs with mixed content. Docling simplifies document processing, parsing diverse formats — including advanced PDF understanding, and providing seamless integrations with the gen AI ecosystem.
- [markitdown](parser/markitdown/) : Excellent  for complex PDFs with mixed content. MarkItDown is a utility for converting various files to Markdown (e.g., for indexing, text analysis, etc). It supports: PDF, PowerPoint, Word, Excel, Images (EXIF metadata and OCR), Audio (EXIF metadata and speech transcription), HTML, Text-based formats (CSV, JSON, XML), ZIP files (iterates over contents)
- [Camelot](parser/camelot/): Specialized table extraction
- [PyPdf](parser/pypdf/): pypdf is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. pypdf can retrieve text and metadata from PDFs as well.
- [PDFMiner](parser/pdfminer/): Basic text and layout extraction
- [PDFPlumber](parser/pdfplumber/): Basic text and layout extraction
- [PyMUPDF](parser/pymupdf/): PyMuPDF is a high performance Python library for data extraction, analysis, conversion & manipulation of PDF
- [pdfium](parser/pypdfmium/): High-fidelity processing using Chrome's PDF engine
- [PyPdfDirectory](parser/pypdfdirectory/): Batch PDF Content Extraction Script using PyPDF2 Directory Loader

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

### 🛠️ Setup

1. Environment Variables
```bash
ANTHROPIC_API_KEY=your_key_here    # For Claude
OPENAI_API_KEY=your_key_here       # For OpenAI
UNSTRUCTURED_API_KEY=your_key_here # For Unstructured.io
```

For **ANTHROPIC_API_KEY** follow this -> https://console.anthropic.com/settings/keys

For **OPENAI_API_KEY** follow this -> https://platform.openai.com/api-keys

For **UNSTRUCTURED_API_KEY** follow this -> https://unstructured.io/api-key-free

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

### 📈 Usage

1. Place PDF files in `input/` directory

### 📄 Example Complex Pdf placed in Input folder
- **sample-1.pdf**: Standard tables
- **sample-2.pdf**: Image-based simple tables
- **sample-3.pdf**: Image-based complex tables
- **sample-4.pdf**: Mixed content (text, tables, images)

### 📝 Notes
- System resources needed for local LLM operations
- API keys required for cloud based implementations
- Consider PDF complexity when choosing implementation
- Ghostscript required for Camelot
- Different processors suit different use cases
  - Cloud: Complex documents, mixed content
  - Local: Simple text, basic tables
  - Specialized: Specific content types (tables, forms)