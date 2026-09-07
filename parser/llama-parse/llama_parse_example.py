try:
    from llama_parse import LlamaParse
except ImportError:
    from llama_cloud_services import LlamaParse

import os
import sys
from dotenv import load_dotenv

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.append(project_root)

from utils.cli import input_pdf
# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables and validate its presence
# The LlamaIndex console labels this key differently from the SDK's env var,
# so accept both spellings instead of reporting a missing key that is present.
LLAMA_CLOUD_API_KEY = (os.getenv("LLAMA_CLOUD_API_KEY")
                       or os.getenv("LLAMA_PARSE_API_KEY"))
if not LLAMA_CLOUD_API_KEY:
    raise ValueError(
        "No LlamaParse key found. Set LLAMA_CLOUD_API_KEY (or "
        "LLAMA_PARSE_API_KEY) in .env. Get one at "
        "https://cloud.llamaindex.ai/api-key - 1,000 pages/day free."
    )
os.environ["LLAMA_CLOUD_API_KEY"] = LLAMA_CLOUD_API_KEY

def main():
    parser = LlamaParse(
        api_key=LLAMA_CLOUD_API_KEY,  
        result_type="markdown",  # "markdown" and "text" are available
        num_workers=4,  # if multiple files passed, split in `num_workers` API calls
        verbose=True,
        language="en",  # Optionally you can define a language, default=en
    )

    # Which PDF to process. Override with --file, e.g.
    #   python parser/llama-parse/llama_parse_example.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")

    docs = parser.load_data(file_path)

    # Batch
    #documents = parser.load_data(["./my_file1.pdf", "./my_file2.pdf"])

    # Output options
    extracted_content = ""
    for doc in docs:
        extracted_content += doc.text+ "\n"
    
    # Output extracted content to output.txt
    os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
    with open(os.path.join(project_root, "output", "llama_parse_example.txt"), "w", encoding="utf-8") as file:
        file.write(extracted_content)

if __name__ == "__main__":
   main()