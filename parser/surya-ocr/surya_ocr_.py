"""
PDF OCR and Layout Analysis using Surya OCR

Surya is a lightweight document OCR toolkit supporting 90+ languages with line-level
detection, layout analysis, and table recognition. It outperforms Tesseract on most
benchmarks and is created by the same author as the Marker PDF tool.

Key Features:
    - 90+ language OCR support
    - Layout analysis and reading order detection
    - Table recognition and extraction
    - Runs locally without any API key
    - High accuracy on complex documents

Dependencies:
    - surya-ocr: pip install surya-ocr
    - pymupdf: For PDF to image conversion

Note: Requires a GPU for best performance, but works on CPU too (slower).
      First run will download the model weights (~1.5GB).
"""
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)



from utils.cli import input_pdf
def main():
    """
    Extract text from PDF using Surya OCR with layout analysis.
    """
    from surya.recognition import RecognitionPredictor
    import pymupdf
    from PIL import Image

    # Configure input PDF path
    # Which PDF to process. Override with --file, e.g.
    #   python parser/surya-ocr/surya_ocr_.py --file input/sample-3.pdf
    # Run with --list to see every bundled sample.
    file_path = input_pdf("sample-1.pdf")

    # Initialize the Surya predictor. Detection is run internally from 0.18
    # onward, so there is no detection predictor to pass in any more.
    recognition_predictor = RecognitionPredictor()

    # Convert PDF pages to images
    doc = pymupdf.open(file_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()

    # Run OCR on all pages. Surya 0.18 removed the `det_predictor` keyword -
    # passing it raises TypeError on any current install.
    results = recognition_predictor(images)

    # Extract text from results
    full_text = ""
    for i, page_result in enumerate(results):
        full_text += f"\n--- Page {i+1} ---\n"
        for line in page_result.text_lines:
            full_text += line.text + "\n"

    print(full_text)

    # Save output
    os.makedirs(os.path.join(project_root, "output"), exist_ok=True)
    with open(os.path.join(project_root, "output", "surya_ocr.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
