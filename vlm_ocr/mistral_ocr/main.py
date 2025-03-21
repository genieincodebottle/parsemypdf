# Required libraries to run this app
# pip install streamlit>=1.43.2 pillow>=11.1.0 mistralai>=1.5.1 python-dotenv>=1.0.1

import streamlit as st
import base64
import io
import os
from PIL import Image
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not set in environment variables")

st.set_page_config(
    page_title="OCR with Mistral-OCR",
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

def query_mistral_ocr(image, model_name):
    """Query Mistral-OCR API with the image and prompt"""
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
        return response
    except Exception as e:
        return f"Error connecting to Mistral-OCR API: {str(e)}"

# App title and description
st.header("📄 OCR with Mistral-OCR")
st.markdown("Upload an image and ask Mistral-OCR to analyze or describe it.")


# Sidebar for model selection and configuration
with st.sidebar:
    st.subheader("Model Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select Mistral-OCR Model",
        options=[
            "mistral-ocr-latest"
        ],
        index=0,
        help="Select the Mistral-OCR model to use"
    )
    
    # Generation parameters
    st.subheader("Generation Parameters")
    
    st.markdown("---")
    st.markdown("""
    ### Setup Instructions
    1. To avoid entering your API key each time:
       - Use .env file available at root folder
       - Add your API key as: `MISTRAL_API_KEY=your_key_here`
    2. Upload an image and ask Mistral about it
    """)

# Main content area
st.subheader("Upload an Image")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.info(f"Image format: {image.format}, Size: {image.size}")
    
    # Process image button
    if st.button("Ask Mistral-OCR"):
        with st.spinner(f"Querying {model_name}..."):
            # Query Mistral-OCR
            result = query_mistral_ocr(
                image,
                model_name
            )
            # Display results
            with col2:
                st.subheader("Mistral's Response")
                st.markdown(result.pages[0].markdown)
                
                
# Add footer information
st.markdown("---")
st.caption("This app uses Mistral API to analyze images. API costs may apply based on your Mistral API account.")