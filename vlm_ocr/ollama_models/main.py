# Required libraries to run this app
# pip install streamlit>=1.43.2 pillow>=11.1.0 requests>=2.32.3

import streamlit as st
import requests
import base64
import io
from PIL import Image

st.set_page_config(
    page_title="Multimodal based OCR",
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

def query_ollama(image, model_name, prompt=None, temperature=0.7, top_p=0.9, top_k=40):
    """Query Ollama API with the image and optional prompt"""
    # Encode image to base64
    image_base64 = encode_image_to_base64(image)
    
    # Default prompt if none provided
    if not prompt:
        prompt = "Extract the content of this image. Preserve layout of tables and spatial positions of contents."
    
    # Prepare the API request
    api_url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "images": [image_base64],
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

# App title and description
st.header("📄 OCR with Gemma3 & Llama3.2 Vision Language Models")

# Sidebar for model selection and configuration
with st.sidebar:
    st.header("Model Configuration")
    model_name = st.selectbox(
        "Select Model",
        options=["gemma3:4b", "gemma3:12b", "gemma3:27b", "x/llama3.2-vision:11b"],
        index=0
    )
    
    # Add generation parameters controls
    st.header("Generation Parameters")
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.05,
        help="Controls randomness: Lower values make output more deterministic, higher values more creative."
    )
    
    top_p = st.slider(
        "Top-p (nucleus sampling)",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        step=0.05,
        help="Controls diversity by considering only top probability tokens. Lower values focus on highest probability tokens."
    )
    
    top_k = st.slider(
        "Top-k",
        min_value=1,
        max_value=100,
        value=40,
        step=1,
        help="Controls diversity by limiting to top k tokens. Lower values make output more focused."
    )
    
    st.markdown("---")
    st.markdown("""
    ### Setup Instructions
    1. Install Ollama: [https://ollama.com/](https://ollama.com/)
    2. Pull the Multimodal(as per system capacity):
    ```
    ollama pull gemma:4b
    ollama pull gemma:12b
    ollama pull gemma:27b
    ollama pull x/llama3.2-vision:11b
    ```
    3. Ensure Ollama is running in the background
    """)

# Main content area
st.subheader("Upload an Image")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Input area for custom prompt
    custom_prompt = st.text_area(
        "Custom Prompt (optional)",
        "Transcribe this image completely, preserving the exact layout of tables as markdown and spatial positioning of all text and elements.",
        help="You can customize the instruction for the model."
    )
    
    # Process image button
    if st.button("Analyze Image"):
        with st.spinner(f"Analyzing image with {model_name}..."):
            # Query the model with generation parameters
            result = query_ollama(
                image, 
                model_name, 
                custom_prompt,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k
            )
            
            # Display results
            with col2:
                st.subheader("Analysis Results")
                st.markdown(result)
                
                # Option to download results
                result_bytes = result.encode()
                st.download_button(
                    label="Download Results",
                    data=result_bytes,
                    file_name="image_analysis.txt",
                    mime="text/plain"
                )

# Add error handling and status information
st.markdown("---")
status_container = st.empty()

# Try to check if Ollama is available
try:
    health_check = requests.get("http://localhost:11434/api/tags")
    if health_check.status_code == 200:
        models = health_check.json().get("models", [])
        gemma_prefixes = ["gemma3:4b", "gemma3:12b", "gemma3:27b", "x/llama3.2-vision:11b"]
        gemma_models = [m for m in models if any(prefix in m.get("name", "").lower() for prefix in gemma_prefixes)]
        
        if gemma_models:
            status_container.success("✅ Ollama is running and models are available.")
            st.json(gemma_models)
        else:
            status_container.warning("⚠️ Ollama is running but no models found. Please pull the model first.")
    else:
        status_container.error("❌ Ollama API responded with an error.")
except:
    status_container.error("❌ Could not connect to Ollama API. Make sure Ollama is running on localhost:11434.")