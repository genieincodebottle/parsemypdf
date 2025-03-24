# Required libraries to run this app
# pip install streamlit>=1.43.2 pillow>=11.1.0 anthropic>=0.49.0 python-dotenv>=1.0.1

import streamlit as st
import base64
import io
import os
from PIL import Image
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in environment variables")

st.set_page_config(
    page_title="OCR with Claude3.7 Sonnet",
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

def query_claude(image, prompt, model_name, temperature=0.7, max_tokens=2048):
    """Query Claude API with the image and prompt"""
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

# App title and description
st.header("📄 OCR with Claude 3.7 Sonnet")
st.markdown("Upload an image and ask Claude to analyze or describe it.")


# Sidebar for model selection and configuration
with st.sidebar:
    st.subheader("Model Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select Claude Model",
        options=[
            "claude-3-7-sonnet-20250219", 
            "claude-3-5-sonnet-20241022"
        ],
        index=0,
        help="Select the Claude model to use"
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
       - Add your API key as: `ANTHROPIC_API_KEY=your_key_here`
    2. Upload an image and ask Claude about it
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
        "Enter your question or prompt for Claude",
        """
        Transcribe all the text content, including both plain text and tables, from the 
        provided document or image. Maintain the original structure, including headers, 
        paragraphs, and any content preceding or following the table. Format the table in 
        Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
        including any introductory or explanatory text before or after the table.   
        """,
        help="What would you like Claude to tell you about this image?"
    )
    
    # Process image button
    if st.button("Ask Claude"):
        with st.spinner(f"Querying {model_name}..."):
            # Query Claude
            result = query_claude(
                image,
                custom_prompt,
                model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Display results
            with col2:
                st.subheader("Claude's Response")
                st.markdown(result)
                
                # Option to download results
                result_bytes = result.encode()
                st.download_button(
                    label="Download Response",
                    data=result_bytes,
                    file_name="claude_image_analysis.txt",
                    mime="text/plain"
                )

# Add footer information
st.markdown("---")
st.caption("This app uses Claude API to analyze images. API costs may apply based on your Anthropic account.")