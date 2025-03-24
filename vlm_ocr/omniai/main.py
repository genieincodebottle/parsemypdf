# Required libraries to run this app
# pip install streamlit>=1.43.2 pillow>=11.1.0 requests>=2.32.3 python-dotenv>=1.0.1

import streamlit as st
import requests
import time
import os
import io
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
OMNI_API_KEY = os.getenv("OMNI_API_KEY")
if not OMNI_API_KEY:
    raise ValueError("OMNI_API_KEY not set in environment variables")

# Constants
OMNI_API_URL = 'https://api.getomni.ai'
HEADERS_URL = {
    'x-api-key': OMNI_API_KEY,
    'Content-Type': 'application/json'
}
HEADER_UPLOAD_FILE = {
    'x-api-key': OMNI_API_KEY
}

# Set up Streamlit page configuration
st.set_page_config(
    page_title="OCR with Omni AI",
    page_icon="📄",
    layout="wide"
)

def create_extraction(url, template_id):
    """Initiate an extraction job with Omni AI API"""
    data = {"url": url, "templateId": template_id}
    response = requests.post(f"{OMNI_API_URL}/extract", json=data, headers=HEADERS_URL)
    return response.json()

def create_extraction_from_file(uploaded_file):
    """Upload an image file and initiate an extraction job"""
    files = {
        'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/octet-stream')
    }
    
    response = requests.post(f"{OMNI_API_URL}/extract", files=files, headers=HEADER_UPLOAD_FILE)
    return response.json()

def get_extraction_result(extraction_id):
    """Get the results of an extraction job"""
    response = requests.get(f"{OMNI_API_URL}/extract?jobId={extraction_id}", headers=HEADERS_URL)
    return response.json()

def run_extraction_with_progress(url=None, uploaded_file=None, template_id=""):
    """Run extraction with progress bar"""
    try:
        # Step 1: Initiate the extraction
        with st.spinner("Initiating extraction..."):
            if url:
                extraction_data = create_extraction(url, template_id)
            else:
                extraction_data = create_extraction_from_file(uploaded_file)
            
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
            result = get_extraction_result(extraction_id)
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

st.header("📄 OCR with Omni AI")
with st.sidebar:
    st.markdown("""
    ### Setup Instructions
    1. To avoid entering your API key each time:
       - Use .env file available at root folder
       - Add your API key as: `OMNI_API_KEY=your_key_here`
    3. Upload file or provide a URL
    """)

# Main content area
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
                result = run_extraction_with_progress(uploaded_file=uploaded_file, template_id="")
                
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
                result = run_extraction_with_progress(url=url, template_id="")
                
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

# Add footer information
st.markdown("---")
st.caption("This app uses Omni AI API to extract data from documents. API costs may apply based on your Omni AI account.")