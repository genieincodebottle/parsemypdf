<div align="center">
<h1><a href="https://www.instagram.com/genieincodebottle/"><img width="200" src="https://github.com/genieincodebottle/generative-ai/blob/main/images/logo_genie.png">&nbsp;</a></h1>
</div>
<div align="center">
    <a target="_blank" href="https://www.youtube.com/@genieincodebottle"><img src="https://img.shields.io/badge/YouTube-10.6K-blue"></a>&nbsp;
    <a target="_blank" href="https://www.linkedin.com/in/rajesh-srivastava"><img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social"></a>&nbsp;
    <a target="_blank" href="https://www.instagram.com/genieincodebottle/"><img src="https://img.shields.io/badge/44.2K-C13584?style=flat-square&labelColor=C13584&logo=instagram&logoColor=white&link=https://www.instagram.com/eduardopiresbr/"></a>&nbsp;
    <a target="_blank" href="https://github.com/genieincodebottle/generative-ai/blob/main/GenAI_Roadmap.md"><img src="https://img.shields.io/badge/style--5eba00.svg?label=GenAI Roadmap&logo=github&style=social"></a>
    
#  

# 📑 Complex PDF Parsing

A comprehensive example codes for extracting content from PDFs


## 📌 Core Features

### 📤 Content Extraction
- Multiple extraction methods with different tools/libraries:
  - Cloud-based: Claude 3.5 Sonnet, GPT-4 Vision, Unstructured.io
  - Local: Llama 3.2 11B, Docling, PDFium
  - Specialized: Camelot (tables), PDFMiner (text), PDFPlumber (mixed), PyPdf etc
- Maintains document structure and formatting
- Handles complex PDFs with mixed content including extracting image data


## 📦 Implementation Options

### 1. ☁️ Cloud-Based Methods
- **Claude & Llama**: Excellent  for complex PDFs with mixed content
- **GPT-4 Vision**: Excellent for visual content analysis
- **Unstructured.io**: Advanced content partitioning and classification

### 2. 🖥️ Local Methods
- **Llama 3.2 11B Vision**: Image-based PDF processing
- **Docling**: Excellent  for complex PDFs with mixed content
- **PDFium**: High-fidelity processing using Chrome's PDF engine
- **Camelot**: Specialized table extraction
- **PDFMiner/PDFPlumber**: Basic text and layout extraction

## 🔗 Dependencies

### 📚 Core Libraries
```bash
langchain_ollama
langchain_huggingface
langchain_community
FAISS
python-dotenv
```

### ⚙️ Implementation-Specific
```bash
anthropic        # Claude
openai           # GPT-4 Vision
camelot-py      # Table extraction
docling         # Text processing
pdf2image       # PDF conversion
pypdfium2       # PDFium processing
boto3           # AWS Textract
```

## 🛠️ Setup

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

## 📈 Usage

1. Place PDF files in `input/` directory

## 📄 Example Complex Pdf placed in Input folder
- **sample-1.pdf**: Standard tables
- **sample-2.pdf**: Image-based simple tables
- **sample-3.pdf**: Image-based complex tables
- **sample-4.pdf**: Mixed content (text, tables, images)

## 📝 Notes
- System resources needed for local LLM operations
- API keys required for cloud based implementations
- Consider PDF complexity when choosing implementation
- Ghostscript required for Camelot
- Different processors suit different use cases
  - Cloud: Complex documents, mixed content
  - Local: Simple text, basic tables
  - Specialized: Specific content types (tables, forms)