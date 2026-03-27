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


def main():
    """
    Extract text from PDF using Surya OCR with layout analysis.
    """
    from surya.ocr import run_ocr
    from surya.recognition import RecognitionPredictor
    from surya.detection import DetectionPredictor
    import pymupdf
    from PIL import Image

    # Configure input PDF path
    #file_path = project_root + "/input/sample-1.pdf"  # Standard tables
    #file_path = project_root + "/input/sample-2.pdf"  # Image-based simple tables
    file_path = project_root + "/input/sample-3.pdf"   # Image-based complex tables
    #file_path = project_root + "/input/sample-4.pdf"  # Mixed content
    #file_path = project_root + "/input/sample-5.pdf"  # Multi-column texts

    # Initialize Surya predictors
    recognition_predictor = RecognitionPredictor()
    detection_predictor = DetectionPredictor()

    # Convert PDF pages to images
    doc = pymupdf.open(file_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()

    # Run OCR on all pages
    languages = [["en"]] * len(images)
    results = run_ocr(images, languages, detection_predictor, recognition_predictor)

    # Extract text from results
    full_text = ""
    for i, page_result in enumerate(results):
        full_text += f"\n--- Page {i+1} ---\n"
        for line in page_result.text_lines:
            full_text += line.text + "\n"

    print(full_text)

    # Save output
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
