"""
PDF OCR using GOT-OCR2 (General OCR Theory 2.0)

GOT-OCR2 is a unified end-to-end model with 580M parameters designed to handle
diverse OCR tasks including plain text, tables, charts, equations, sheet music,
and molecular formulas. It generates plain or formatted outputs (markdown, LaTeX).

Key Features:
    - Unified model for all OCR tasks (text, tables, charts, math)
    - 580M parameters - runs on consumer GPUs (8GB+ VRAM)
    - Supports formatted output (markdown, LaTeX)
    - Handles scene text and document-style images
    - Available on HuggingFace Transformers

Dependencies:
    - transformers: pip install transformers
    - torch: pip install torch
    - pymupdf: For PDF to image conversion
    - tiktoken: Required by the model

Note: First run downloads the model weights (~1.2GB). Requires GPU for inference.
"""
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)


def main():
    """
    Extract text from PDF using GOT-OCR2 model via HuggingFace Transformers.
    """
    import torch
    from transformers import AutoModel, AutoTokenizer
    import pymupdf
    from PIL import Image
    import tempfile

    # Configure input PDF path
    #file_path = project_root + "/input/sample-1.pdf"  # Standard tables
    #file_path = project_root + "/input/sample-2.pdf"  # Image-based simple tables
    file_path = project_root + "/input/sample-3.pdf"   # Image-based complex tables
    #file_path = project_root + "/input/sample-4.pdf"  # Mixed content
    #file_path = project_root + "/input/sample-5.pdf"  # Multi-column texts

    # Load GOT-OCR2 model
    model_name = "stepfun-ai/GOT-OCR-2.0-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    model.eval()

    # Convert PDF pages to images
    doc = pymupdf.open(file_path)
    full_text = ""

    for page_num, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save temp image (GOT-OCR2 expects file path)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp, format="PNG")
            tmp_path = tmp.name

        try:
            # Run OCR - use "ocr" for plain text, "format" for markdown/LaTeX
            result = model.chat(tokenizer, tmp_path, ocr_type="format")
            full_text += f"\n--- Page {page_num + 1} ---\n"
            full_text += result + "\n"
        finally:
            os.remove(tmp_path)

    doc.close()

    print(full_text)

    # Save output
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
