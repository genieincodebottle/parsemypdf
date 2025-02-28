from llama_cloud_services import LlamaParse

import os
from dotenv import load_dotenv

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
if not LLAMA_CLOUD_API_KEY:
    raise ValueError("LLAMA_CLOUD_API_KEY not set in environment variables")

def main():
    parser = LlamaParse(
        api_key=LLAMA_CLOUD_API_KEY,  
        result_type="markdown",  # "markdown" and "text" are available
        num_workers=4,  # if multiple files passed, split in `num_workers` API calls
        verbose=True,
        language="en",  # Optionally you can define a language, default=en
    )

    #file_path = project_root+"/input/sample-1.pdf" # Table in pdf
    #file_path = project_root+"/input/sample-2.pdf" # Image based simple table in pdf
    #file_path = project_root+"/input/sample-3.pdf" # Image based complex table in pdf
    file_path = project_root+"/input/sample-4.pdf"  # Complex PDF with text and tables in images
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 

    docs = parser.load_data(file_path)

    # Batch
    #documents = parser.load_data(["./my_file1.pdf", "./my_file2.pdf"])

    # Output options
    extracted_content = ""
    for doc in docs:
        extracted_content += doc.text+ "\n"
    
    # Output extracted content to output.txt
    with open("output.txt", 'w') as file:
        file.write(extracted_content)

if __name__ == "__main__":
   main()