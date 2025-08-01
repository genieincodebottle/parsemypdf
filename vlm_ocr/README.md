<div align="center">
<a href="https://www.instagram.com/genieincodebottle/"><img src="../images/genie_logo.png"></a>
</div>
<br>
<div align="center">
    <a target="_blank" href="https://www.youtube.com/@genieincodebottle"><img src="https://img.shields.io/badge/YouTube-11.5K-blue"></a>&nbsp;
    <a target="_blank" href="https://www.linkedin.com/in/rajesh-srivastava"><img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social"></a>&nbsp;
    <a target="_blank" href="https://www.instagram.com/genieincodebottle/"><img src="https://img.shields.io/badge/52K-C13584?style=round-square&labelColor=C13584&logo=instagram&logoColor=white&link=https://www.instagram.com/eduardopiresbr/"></a>&nbsp;
    <a target="_blank" href="https://medium.com/@raj-srivastava"><img src="https://img.shields.io/badge/Medium-12100E?style=round-square&style=for-the-badge&logo=medium"></a>&nbsp;
    <a target="_blank" href="https://x.com/zero2nn"><img src="https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=%20%40zero2nn"></a>
</div>

### <a target="_blank" href="https://github.com/genieincodebottle/generative-ai/blob/main/GenAI_Roadmap.md">👉 GenAI Roadmap - 2025</a></h3>

### 🖼️ OCR with Multimodal | Vision Language Models

| Model Provider | Models                                                       | Open / Paid | Example Code     | Doc       |
| -------------- | ------------------------------------------------------------ | ------------------ | -------- |---------- |
| Anthropic      | `claude-opus-4-20250514`, `claude-sonnet-4-20250514`, `claude-3-7-sonnet-20250219`, `claude-3-5-sonnet-20241022`   | Paid               | [Code](/vlm_ocr/anthropic/main.py)              | [Doc](https://www.anthropic.com/claude/sonnet)                                                                                |
| Gemini         | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite-preview-06-17`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-2.0-pro-exp-02-05` | Paid               | [Code](/vlm_ocr/gemini/main.py)              | [Doc](https://ai.google.dev/gemini-api/docs/models)
| OpenAI         | `gpt-4.1-2025-04-14`, `gpt-4.1-mini-2025-04-14`, `gpt-4o`, `gpt-4o-mini` | Paid               | [Code](/vlm_ocr/openai//main.py)              | [Doc](https://platform.openai.com/docs/models/gpt-4o)
| Mistral-OCR        | `mistral-ocr`                                                | Paid  | [Code](/vlm_ocr/mistral_ocr/main.py)              | [Doc](https://docs.mistral.ai/capabilities/document/)
| OmniAI         | `omniai`                                                     | Paid  | [Code](/vlm_ocr/omniai/main.py)              | [Doc](https://docs.getomni.ai/docs/introduction)
| Google & Meta         | `gemma3:4b`, `gemma3:12b`, `gemma3:27b`, `x/llama3.2-vision:11b` | Open Weight  | [Code](/vlm_ocr/ollama_models/main.py)              | [Gemma Doc](https://blog.google/technology/developers/gemma-3/), [Llama3.2 Doc](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)
| IBM         | `SmolDocling-256M-preview`                                       | Open Weight | [Code](/vlm_ocr/smol_docling//main.py)              | [Doc](https://huggingface.co/ds4sd/SmolDocling-256M-preview)

### 📊 [OCR Benchmark](https://github.com/getomni-ai/benchmark?tab=readme-ov-file#omni-ocr-benchmark) 

### 🔗 Dependencies

#### 📚 Python Libraries
```bash
# UI
streamlit>=1.43.2 

# SmolDocling related
docling_core>=2.23.1

# LLM related Libraries
ollama>=0.4.7
openai>=1.66.3
anthropic>=0.49.0
google-genai>=1.5.0

# Huggingface library
transformers>=4.49.0

# Utilities
python-dotenv>=1.0.1
pillow>=11.1.0 
requests>=2.32.3
torch>=2.6.0
```

### ⚙️ Setup Instructions

- #### Prerequisites
   - Python 3.9 or higher
   - pip (Python package installer)

- #### Installation
   1. Clone the repository:
      ```bash
      git clone https://github.com/genieincodebottle/parsemypdf.git
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
   4. Rename `.env.example` to `.env` and update required Environment Variables as per requirements
      ```bash
      ANTHROPIC_API_KEY=your_key_here    # For Claude
      OPENAI_API_KEY=your_key_here       # For OpenAI
      GOOGLE_API_KEY=your_key_here   # For Google's Gemini models api key
      MISTRAL_API_KEY=your_key_here # For Mistral API Key
      OMNI_API_KEY=your_key_here # For Omniai API Key
      ```
      For **ANTHROPIC_API_KEY** follow this -> https://console.anthropic.com/settings/keys

      For **OPENAI_API_KEY** follow this -> https://platform.openai.com/api-keys

      For **GOOGLE_API_KEY** follow this -> https://ai.google.dev/gemini-api/docs/api-key

      For **MISTRAL_API_KEY** follow this -> https://console.mistral.ai/api-keys

      For **OMNI_API_KEY** follow this -> https://app.getomni.ai/settings/account

  5. Install Ollama & Models (for local processing)
      - Install Ollama
         - For Window - Download the Ollama from following location (Requires Window 10 or later) -> https://ollama.com/download/windows
         - For Linux (command line) - curl https://ollama.ai/install.sh | sh

      - Pull required Vision Language Models as per your system capcity (command line)
         - ollama pull gemma3:4b
         - ollama pull gemma3:12b
         - ollama pull gemma3:27b
         - ollama pull x/llama3.2-vision:11b

  6. To review each Vision Language Model powered OCR in the Web UI, navigate to `parsemypdf/llm_ocr/<provider_folder>` (e.g., claude) and run:
      
      ```bash 
      streamlit run main.py 
      ```
  7.  To review all the Vision Language Models powered OCR at single Web UI, navigate to root folder -> `parsemypdf` and run:
      
      ```bash 
      streamlit run vlm_ocr_app.py 
      ```