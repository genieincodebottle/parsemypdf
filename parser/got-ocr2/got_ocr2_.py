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



from utils.cli import input_pdf
def main():
    """
    Extract text from PDF using GOT-OCR2 model via HuggingFace Transformers.
    """
    import torch
    # The "-hf" repo is the transformers-native port of GOT-OCR2 and uses the
    # standard processor + generate() API. The `.chat()` method belongs to the
    # ORIGINAL trust_remote_code repo (stepfun-ai/GOT-OCR2_0); mixing the two
    # raises AttributeError: 'GotOcr2Model' object has no attribute 'chat'.
    from transformers import AutoProcessor, AutoModelForImageTextToText
    import pymupdf
    from PIL import Image

    # Configure input PDF path
    # Which PDF to process. Override with --file, e.g.
    #   python parser/got-ocr2/got_ocr2_.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")

    # Load GOT-OCR2. About 1.5 GB on the first run, cached afterwards.
    model_name = "stepfun-ai/GOT-OCR-2.0-hf"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForImageTextToText.from_pretrained(
        model_name,
        dtype=torch.float16 if device == "cuda" else torch.float32,
    ).to(device)
    model.eval()

    # Convert PDF pages to images
    doc = pymupdf.open(file_path)
    full_text = ""

    for page_num, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # The processor takes a PIL image directly - no temp file needed.
        inputs = processor(img, return_tensors="pt").to(device)
        with torch.no_grad():
            generated = model.generate(
                **inputs,
                do_sample=False,
                tokenizer=processor.tokenizer,
                stop_strings="<|im_end|>",
                max_new_tokens=2048,
            )
        result = processor.decode(
            generated[0, inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        )
        full_text += f"\n--- Page {page_num + 1} ---\n"
        full_text += result + "\n"

    doc.close()

    print(full_text)

    # Save output
    os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
    with open(os.path.join(project_root, "output", "got_ocr2.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
