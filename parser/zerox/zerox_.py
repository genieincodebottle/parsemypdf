"""
PDF Parsing using Zerox (Vision Model-based OCR)

Zerox converts PDFs into images and uses vision language models (GPT-4o, etc.)
to extract text with high accuracy. It supports structured data extraction using
schemas, making it ideal for pulling specific fields from documents.

Key Features:
    - Converts PDF pages to images, then uses vision LLMs for extraction
    - Supports structured data extraction via schemas
    - Works with OpenAI, Azure OpenAI, and other vision model providers
    - Handles complex layouts, tables, and mixed content
    - Returns clean markdown output

Dependencies:
    - py-zerox: pip install py-zerox
    - Requires an OpenAI API key (or other supported vision model provider)

Note: Uses the OpenAI API for processing. Each page costs ~$0.01 with gpt-4o-mini.
"""
import os
import sys
import asyncio

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)


from utils.cli import input_pdf
from dotenv import load_dotenv
load_dotenv()


def main():
    """
    Extract text from PDF using Zerox with GPT-4o-mini vision model.
    """
    from pyzerox import zerox

    # Configure input PDF path
    # Which PDF to process. Override with --file, e.g.
    #   python parser/zerox/zerox_.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")

    # Zerox routes through litellm, so any vision model litellm supports works.
    # It needs a VISION model: Groq's gpt-oss models are text-only, so there is
    # no free fallback here the way there is for the plain OpenAI parser.
    model = os.getenv("ZEROX_MODEL", "gpt-4o-mini")  # ~$0.01/page
    #model = "gpt-4o"                                # more accurate, dearer
    #model = "gemini/gemini-flash-latest"            # needs GEMINI_API_KEY

    if not (os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")):
        raise SystemExit(
            "Zerox needs a VISION model key.\n"
            "  OPENAI_API_KEY  -> keep the default gpt-4o-mini\n"
            "  GEMINI_API_KEY  -> set ZEROX_MODEL=gemini/gemini-flash-latest "
            "(free tier)"
        )

    # Run Zerox extraction
    result = asyncio.run(zerox(
        file_path=file_path,
        model=model,
        cleanup=True,
    ))

    # Extract text from result pages
    full_text = ""
    for page in result.pages:
        full_text += page.content + "\n\n"

    print(full_text)

    # Save output
    os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
    with open(os.path.join(project_root, "output", "zerox.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
