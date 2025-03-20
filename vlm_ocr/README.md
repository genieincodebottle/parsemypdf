## 🖼️ Vision Language Models Powered OCR

- [Gemini-2.0](/llm_ocr/gemini/main.py) 

- [Claude-3.7 Sonnet](/llm_ocr/claude/main.py)

- [GPT-4.0 Model](/llm_ocr/gpt4/main.py)

- [Gemma3-4b, 12b, 27b and Llama3.2-11b Vision Model](/llm_ocr/ollama_models/main.py)

- [Mistral-OCR](/llm_ocr/mistral_ocr/) : https://docs.mistral.ai/capabilities/document/

- [SmolDocling](/llm_ocr/smol_docling/main.py): https://huggingface.co/ds4sd/SmolDocling-256M-preview

- [Omni-AI](/llm_ocr/omni_ai/): https://docs.getomni.ai/docs/introduction

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