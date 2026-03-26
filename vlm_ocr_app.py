# Required libraries to run this app
# pip install streamlit>=1.43.2 pillow>=11.1.0 anthropic>=0.49.0 google-genai>=1.5.0 openai>=1.66.3 mistralai>=1.5.1 requests>=2.32.3 python-dotenv>=1.0.1

import streamlit as st
import base64
import io
import os
import requests
import time
from PIL import Image
from dotenv import load_dotenv

# Conditionally import provider libraries
try:
    from anthropic import Anthropic 
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from google import genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
OMNI_API_KEY = os.getenv("OMNI_API_KEY")

# Omni API constants
OMNI_API_URL = 'https://api.getomni.ai'

OMNI_HEADERS_URL = {
    'x-api-key': OMNI_API_KEY,
    'Content-Type': 'application/json'
} if OMNI_API_KEY else {}

OMNI_HEADER_UPLOAD_FILE = {
    'x-api-key': OMNI_API_KEY
} if OMNI_API_KEY else {}

# Constants
MODEL_PROVIDERS = {
    "Claude": {
        "models": ["claude-opus-4-20250514", "claude-sonnet-4-20250514", "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022"],
        "api_key": ANTHROPIC_API_KEY,
        "available": ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY is not None
    },
    "Gemini": {
        "models": ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-2.0-pro-exp-02-05"],
        "api_key": GOOGLE_API_KEY,
        "available": GOOGLE_AVAILABLE and GOOGLE_API_KEY is not None
    },
    "GPT": {
        "models": ["gpt-4.1-2025-04-14", "gpt-4.1-mini-2025-04-14", "gpt-4o", "gpt-4o-mini"],
        "api_key": OPENAI_API_KEY,
        "available": OPENAI_AVAILABLE and OPENAI_API_KEY is not None
    },
    "Mistral": {
        "models": ["mistral-ocr-latest"],
        "api_key": MISTRAL_API_KEY,
        "available": MISTRAL_AVAILABLE and MISTRAL_API_KEY is not None
    },
    "Ollama": {
        "models": ["gemma3:4b", "gemma3:12b", "gemma3:27b", "x/llama3.2-vision:11b"],
        "api_key": None,  # No API key needed for local Ollama
        "available": True  # We'll check connection during runtime
    },
    "Omni": {
        "models": ["default"],  # Omni doesn't have selectable models in the provided code
        "api_key": OMNI_API_KEY,
        "available": OMNI_API_KEY is not None
    }
}

# Get available providers
AVAILABLE_PROVIDERS = [p for p, details in MODEL_PROVIDERS.items() if details["available"]]

st.set_page_config(
    page_title="OCR with Vision Language Model",
    page_icon="📄",
    layout="wide"
)

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    # Determine the format based on the original image format or default to PNG
    if hasattr(image, 'format') and image.format:
        img_format = image.format
    else:
        img_format = "PNG"
    
    buffered = io.BytesIO()
    image.save(buffered, format=img_format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str, img_format.lower()

####### CLAUDE Models ##########
def query_claude(image, prompt, model_name, temperature=0.7, max_tokens=2048):
    """Query Claude API with the image and prompt"""
    if not ANTHROPIC_AVAILABLE or not ANTHROPIC_API_KEY:
        return "Anthropic library not installed or API key not set."
    
    # Encode image to base64
    base64_string, img_format = encode_image_to_base64(image)
    
    # Create Anthropic client
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Determine media type based on image format
    if img_format == 'jpg' or img_format == 'jpeg':
        media_type = "image/jpeg"
    elif img_format == 'png':
        media_type = "image/png"
    else:
        # Default to JPEG if format is unknown
        media_type = "image/jpeg"
    
    # Prepare the API request
    message_list = [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64_string}},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=message_list
        )
        return response.content[0].text
    except Exception as e:
        return f"Error connecting to Claude API: {str(e)}"

####### GEMINI Models ##########
def query_gemini(image, prompt, model_name, temperature=0.7, max_tokens=2048):
    """Query Gemini API with the image and prompt"""
    if not GOOGLE_AVAILABLE or not GOOGLE_API_KEY:
        return "Google GenAI library not installed or API key not set."
    
    # Create Gemini client
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[
                prompt,
                image
            ]
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini API: {str(e)}"

####### GPT Models ##########
def query_gpt(image, prompt, model_name, temperature=0.7, max_tokens=2048):
    """Query OpenAI GPT API with the image and prompt"""
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY:
        return "OpenAI library not installed or API key not set."
    
    # Encode image to base64
    base64_string, img_format = encode_image_to_base64(image)
    
    # Create OpenAI client
    client = OpenAI()
    
    # Determine media type based on image format
    if img_format == 'jpg' or img_format == 'jpeg':
        media_type = "image/jpeg"
    elif img_format == 'png':
        media_type = "image/png"
    else:
        # Default to JPEG if format is unknown
        media_type = "image/jpeg"
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{base64_string}"
                            },
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to GPT API: {str(e)}"

####### MISTRAL-OCR Model ##########
def query_mistral_ocr(image, model_name):
    """Query Mistral-OCR API with the image and prompt"""
    if not MISTRAL_AVAILABLE or not MISTRAL_API_KEY:
        return "Mistral library not installed or API key not set."
    
    # Encode image to base64
    base64_string, img_format = encode_image_to_base64(image)
    
    # Create Mistral client
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    # Determine media type based on image format
    if img_format == 'jpg' or img_format == 'jpeg':
        media_type = "image/jpeg"
    elif img_format == 'png':
        media_type = "image/png"
    else:
        # Default to JPEG if format is unknown
        media_type = "image/jpeg"
    
    try:
        response = client.ocr.process(
            model=model_name,
            document={
                "type": "image_url",
                "image_url": f"data:{media_type};base64,{base64_string}" 
            }
        )
        return response.pages[0].markdown
    except Exception as e:
        return f"Error connecting to Mistral-OCR API: {str(e)}"

####### OLLAMA Based Vision Models ##########
def query_ollama(image, model_name, prompt=None, temperature=0.7, top_p=0.9, top_k=40):
    """Query Ollama API with the image and optional prompt"""
    # Encode image to base64
    base64_string, img_format = encode_image_to_base64(image)   
    
    # Default prompt if none provided
    if not prompt:  
        prompt = "Extract the content of this image. Preserve layout of tables and spatial positions of contents."
    
    # Prepare the API request
    api_url = "http://localhost:11434/api/generate" 
    payload = {
        "model": model_name,
        "prompt": prompt,
        "images": [base64_string],
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }
    }
    
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

####### OMNIAI Model ##########
def create_omni_extraction(url, template_id):
    """Initiate an extraction job with Omni AI API"""
    if not OMNI_API_KEY:
        return {"error": "OMNI_API_KEY not set in environment variables"}
    
    data = {"url": url, "templateId": template_id}
    response = requests.post(f"{OMNI_API_URL}/extract", json=data, headers=OMNI_HEADERS_URL)
    return response.json()

def create_omni_extraction_from_file(uploaded_file):
    """Upload an image file and initiate an extraction job with Omni AI"""
    if not OMNI_API_KEY:
        return {"error": "OMNI_API_KEY not set in environment variables"}
    
    files = {
        'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/octet-stream')
    }
    
    response = requests.post(f"{OMNI_API_URL}/extract", files=files, headers=OMNI_HEADER_UPLOAD_FILE)
    return response.json()

def get_omni_extraction_result(extraction_id):
    """Get the results of an extraction job from Omni AI"""
    if not OMNI_API_KEY:
        return {"error": "OMNI_API_KEY not set in environment variables"}
    
    response = requests.get(f"{OMNI_API_URL}/extract?jobId={extraction_id}", headers=OMNI_HEADERS_URL)
    return response.json()

def run_omni_extraction_with_progress(url=None, uploaded_file=None, template_id=""):
    """Run extraction with progress bar for Omni AI"""
    try:
        # Step 1: Initiate the extraction
        with st.spinner("Initiating extraction..."):
            if url:
                extraction_data = create_omni_extraction(url, template_id)
            else:
                extraction_data = create_omni_extraction_from_file(uploaded_file)
            
            if 'error' in extraction_data:
                st.error(f"Error initiating extraction: {extraction_data['error']}")
                return None
            
            if 'jobId' not in extraction_data:
                st.error(f"Error initiating extraction: {extraction_data}")
                return None
                
            extraction_id = extraction_data.get('jobId')
            st.success(f"Extraction initiated with job ID: {extraction_id}")

        # Step 2: Poll for results with a progress bar
        polling_interval = 2  # 2 seconds between attempts
        max_duration = 180  # 3 minutes maximum polling duration
        start_time = time.time()
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        while time.time() - start_time < max_duration:
            # Calculate progress percentage (time-based)
            elapsed = time.time() - start_time
            progress = min(elapsed / max_duration, 0.99)
            progress_bar.progress(progress)
            
            status_text.text(f"Extracting data... ({int(elapsed)}s elapsed)")
            
            # Wait for the specified polling interval
            time.sleep(polling_interval)
            
            # Check extraction status
            result = get_omni_extraction_result(extraction_id)
            if result.get('status') in ['COMPLETE', 'ERROR']:
                progress_bar.progress(1.0)
                if result.get('status') == 'COMPLETE':
                    status_text.text("Extraction completed successfully!")
                else:
                    status_text.text(f"Extraction error: {result.get('error', 'Unknown error')}")
                break
        
        return result
    except Exception as e:
        st.error(f"Error during extraction: {str(e)}")
        return None

def process_with_provider(provider, model, image, prompt, temp, max_tokens):
    """Process the image with the selected provider and model"""
    if provider == "Claude":
        return query_claude(image, prompt, model, temperature=temp, max_tokens=max_tokens)
    elif provider == "Gemini":
        return query_gemini(image, prompt, model, temperature=temp, max_tokens=max_tokens)
    elif provider == "GPT":
        return query_gpt(image, prompt, model, temperature=temp, max_tokens=max_tokens)
    elif provider == "Mistral":
        return query_mistral_ocr(image, model)
    elif provider == "Ollama":
        return query_ollama(image, model, prompt, temperature=temp)
    elif provider == "Omni":
        # For Omni, we handle differently since it uses a job-based approach
        return "Omni processing will be handled separately."
    else:
        return f"Unknown provider: {provider}"

# App title and description
st.header("📄 OCR with Vision Language Model")
st.markdown("Upload an image and extract text using various AI models")

# Sidebar for model selection and configuration
with st.sidebar:
    st.subheader("Model Provider")
    
    if not AVAILABLE_PROVIDERS:
        st.error("No model providers are available. Please check your API keys and installed libraries.")
        provider = None
    else:
        provider = st.selectbox(
            "Select Provider",
            options=AVAILABLE_PROVIDERS,
            index=0,
            help="Select the AI provider to use"
        )
    
    if provider:
        st.subheader("Model Configuration")
        
        # Model selection
        available_models = MODEL_PROVIDERS[provider]["models"]
        model = st.selectbox(
            f"Select {provider} Model",
            options=available_models,
            index=0,
            help=f"Select the {provider} model to use"
        )
        
        # Generation parameters (except for Omni which has a different workflow)
        if provider != "Omni" and provider != "Mistral":
            st.subheader("Generation Parameters")
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Controls randomness: Lower values make output more deterministic, higher values more creative."
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=100,
                max_value=4096,
                value=2048,
                step=50,
                help="Maximum number of tokens to generate in the response."
            )
            
            if provider == "Ollama":
                top_p = st.slider(
                    "Top-p (nucleus sampling)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.9,
                    step=0.05,
                    help="Controls diversity by considering only top probability tokens."
                )
                
                top_k = st.slider(
                    "Top-k",
                    min_value=1,
                    max_value=100,
                    value=40,
                    step=1,
                    help="Controls diversity by limiting to top k tokens."
                )
        
    # API Key Information
    st.markdown("---")
    st.markdown("""
    ### Setup Instructions
    1. To avoid entering API keys each time:
       - Use .env file available at root folder
       - Add your API keys as follows:
       ```
       ANTHROPIC_API_KEY=your_key_here
       GOOGLE_API_KEY=your_key_here
       OPENAI_API_KEY=your_key_here
       MISTRAL_API_KEY=your_key_here
       OMNI_API_KEY=your_key_here
       ```
    2. For Ollama:
       - Install Ollama: [https://ollama.com/](https://ollama.com/)
       - Pull the required model:
       ```
       ollama pull gemma3:4b
       ollama pull gemma3:12b
       ollama pull gemma3:27b
       ollama pull x/llama3.2-vision:11b
       ```
       - Ensure Ollama is running in the background
    """)

# Main content area based on provider
if provider != "Omni":
    # Standard OCR workflow for most providers
    st.subheader("Upload an Image")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.info(f"Image format: {image.format}, Size: {image.size}")
        
        # Custom prompt input (except for Mistral which has a fixed workflow)
        if provider != "Mistral":
            custom_prompt = st.text_area(
                f"Enter your question or prompt for {provider}",
                """Transcribe all the text content, including both plain text and tables, from the provided document or image. 
                Maintain the original structure, including headers, paragraphs, and any content preceding or following the 
                table. Format the table in Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
                including any introductory or explanatory text before or after the table.""",
                help=f"What would you like {provider} to tell you about this image?"
            )
        
        # Process image button
        button_label = f"Ask {provider}" if provider != "Mistral" else f"Use {provider}-OCR"
        if st.button(button_label):
            with st.spinner(f"Querying {model}..."):
                # Query the selected provider
                if provider == "Mistral":
                    result = query_mistral_ocr(image, model)
                elif provider == "Ollama":
                    result = query_ollama(
                        image, 
                        model, 
                        custom_prompt,
                        temperature=temperature,
                        top_p=top_p,
                        top_k=top_k
                    )
                else:
                    result = process_with_provider(
                        provider, 
                        model, 
                        image, 
                        custom_prompt, 
                        temperature, 
                        max_tokens
                    )
                
                # Display results
                with col2:
                    st.subheader(f"{provider}'s Response")
                    st.markdown(result)
                    
                    # Option to download results
                    result_bytes = result.encode()
                    st.download_button(
                        label="Download Response",
                        data=result_bytes,
                        file_name=f"{provider.lower()}_image_analysis.txt",
                        mime="text/plain"
                    )

else:
    # Omni-specific workflow
    st.subheader("Document Input")
    
    # Tabs for different input methods
    tab1, tab2 = st.tabs(["Upload Image", "Provide URL"])
    
    with tab1:
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Display the uploaded image
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Document", width=400)
                st.info(f"File format: {uploaded_file.type}, Size: {uploaded_file.size} bytes")
            except Exception as e:
                st.warning(f"Unable to preview this file type: {str(e)}")
    
            # Process document button
            if st.button("Extract Data (Upload)"):
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                
                # Run extraction
                with st.expander("Extraction Process", expanded=True):
                    result = run_omni_extraction_with_progress(uploaded_file=uploaded_file, template_id="")
                    
                    if result:
                        # Display results
                        st.subheader("Extraction Results")
                        st.json(result)
                        
                        # Option to download results
                        result_json = str(result)
                        st.download_button(
                            label="Download Results (JSON)",
                            data=result_json,
                            file_name="omni_extraction_results.json",
                            mime="application/json"
                        )
    
    with tab2:
        url = st.text_input("Enter document URL", help="URL of the document to extract data from")
        
        if url:
            st.markdown(f"**Document URL**: {url}")
            
            # Try to display the image from URL
            try:
                response = requests.get(url)
                image = Image.open(io.BytesIO(response.content))
                st.image(image, caption="Document from URL", width=400)
            except:
                st.info("Unable to preview this URL. It might not be an image or might be inaccessible.")
            
            # Process URL button
            if st.button("Extract Data (URL)"):
                # Run extraction
                with st.expander("Extraction Process", expanded=True):
                    result = run_omni_extraction_with_progress(url=url, template_id="")
                    
                    if result:
                        # Display results
                        st.subheader("Extraction Results")
                        st.json(result)
                        
                        # Option to download results
                        result_json = str(result)
                        st.download_button(
                            label="Download Results (JSON)",
                            data=result_json,
                            file_name="omni_extraction_results.json",
                            mime="application/json"
                        )

# Check Ollama connection if it's an available provider
if "Ollama" in AVAILABLE_PROVIDERS:
    st.markdown("---")
    ollama_status = st.empty()
    
    # Try to check if Ollama is available
    try:
        health_check = requests.get("http://localhost:11434/api/tags")
        if health_check.status_code == 200:
            models = health_check.json().get("models", [])
            ollama_models = [m for m in models if any(model in m.get("name", "").lower() for model in ["gemma3", "llama3.2-vision"])]
            
            if ollama_models:
                ollama_status.success("✅ Ollama is running and models are available.")
            else:
                ollama_status.warning("⚠️ Ollama is running but required models not found. Please pull the models first.")
        else:
            ollama_status.error("❌ Ollama API responded with an error.")
    except:
        ollama_status.error("❌ Could not connect to Ollama API. Make sure Ollama is running on localhost:11434.")

# Add footer information
st.markdown("---")
st.caption("This app uses various AI APIs to analyze images. API costs may apply based on your provider accounts.")