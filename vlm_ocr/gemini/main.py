# Required libraries to run this app 
# pip install streamlit>=1.43.2 pillow>=11.1.0 google-genai>=1.5.0 python-dotenv>=1.0.1

import streamlit as st
import os
from PIL import Image
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Validate and set Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables")

st.set_page_config(
    page_title="OCR with gemini-2.0-flash",
    page_icon="📄",
    layout="wide"
)

def query_gemini(image, prompt, model_name, temperature=0.7, max_tokens=2048):
    """Query Gemini API with the image and prompt"""
    # Create Gemini client
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    response = client.models.generate_content(
        model=model_name,
        contents=[
                prompt,
                image
            ]
        )
    return response.text
   
# App title and description
st.header("📄 OCR with Gemini-2.0")
st.markdown("Upload an image and ask Gemini to analyze or describe it.")


# Sidebar for model selection and configuration
with st.sidebar:
    st.subheader("Model Configuration")
    
    # Model selection
    model_name = st.selectbox(
        "Select Gemini Model",
        options=[
            "gemini-2.0-flash", 
            "gemini-2.0-flash-lite",
            "gemini-2.0-pro-exp-02-05"
        ],
        index=0,
        help="Select the Gemini model to use"
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
       - Add your API key as: `GOOGLE_API_KEY=your_key_here`
    2. Upload an image and ask Gemini about it
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
        "Enter your question or prompt for Gemini",
        """
        Transcribe all the text content, including both plain text and tables, from the 
        provided document or image. Maintain the original structure, including headers, 
        paragraphs, and any content preceding or following the table. Format the table in 
        Markdown format, preserving numerical data and relationships. Ensure no text is excluded, 
        including any introductory or explanatory text before or after the table. 
        """,
        help="What would you like Gemini to tell you about this image?"
    )
    
    # Process image button
    if st.button("Ask Gemini"):
        with st.spinner(f"Querying {model_name}..."):
            # Query Gemini
            result = query_gemini(
                image,
                custom_prompt,
                model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Display results
            with col2:
                st.subheader("Gemini's Response")
                st.markdown(result)
                
                # Option to download results
                result_bytes = result.encode()
                st.download_button(
                    label="Download Response",
                    data=result_bytes,
                    file_name="gemini_image_analysis.txt",
                    mime="text/plain"
                )
