# Required libraries to run this app
# pip install streamlit>=1.43.2 pillow>=11.1.0 openai>=1.66.3 python-dotenv>=1.0.1

import streamlit as st
import base64
import io
import os
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables")

st.set_page_config(
    page_title="OCR with GPT 4.0",
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

def query_gpt(image, prompt, model_name, temperature=0.7, max_tokens=2048):
    """Query GPT4.0 API with the image and prompt"""
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

# App title and description
st.header("📄 OCR with GPT 4.0")
st.markdown("Upload an image and ask GPT to analyze or describe it.")


# Sidebar for model selection and configuration
with st.sidebar:
    st.subheader("Model Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select GPT Model",
        options=[
            "gpt-4o", 
            "gpt-4o-mini"
        ],
        index=0,
        help="Select the GPT model to use"
    )
    
    # Generation parameters
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
    
    st.markdown("---")
    st.markdown("""
    ### Setup Instructions
    1. To avoid entering your API key each time:
       - Use .env file available at root folder
       - Add your API key as: `OPENAI_API_KEY=your_key_here`
    2. Upload an image and ask GPT about it
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
    
    # Input area for custom prompt
    custom_prompt = st.text_area(
        "Enter your question or prompt for GPT",
        """
        Transcribe all the text content, including both plain text and tables, from the 
        provided document or image. Maintain the original structure, including headers, 
        paragraphs, and any content preceding or following the table. Format the table in 
        Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
        including any introductory or explanatory text before or after the table.        
        """,
        help="What would you like GPT to tell you about this image?"
    )
    
    # Process image button
    if st.button("Ask GPT"):
        with st.spinner(f"Querying {model_name}..."):
            # Query GPT4.0
            result = query_gpt(
                image,
                custom_prompt,
                model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Display results
            with col2:
                st.subheader("GPT's Response")
                st.markdown(result)
                
                # Option to download results
                result_bytes = result.encode()
                st.download_button(
                    label="Download Response",
                    data=result_bytes,
                    file_name="gpt_image_analysis.txt",
                    mime="text/plain"
                )

# Add footer information
st.markdown("---")
st.caption("This app uses GPT4.0 API to analyze images. API costs may apply based on your OpenAI account.")