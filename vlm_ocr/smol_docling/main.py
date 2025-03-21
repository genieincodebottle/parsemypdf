# Required libraries to run this app
# pip install streamlit>=1.43.2 transformers>=4.49.0 torch>=2.6.0 docling_core>=2.23.1

import os
import torch
import time
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def process_document(image_path):
    timings = {}
    
    # Load image
    start_time = time.time()
    image = load_image(image_path)
    timings['image_loading'] = time.time() - start_time
    print(f"Image loading: {timings['image_loading']:.2f} seconds")
    
    # Initialize processor and model
    start_time = time.time()
    processor = AutoProcessor.from_pretrained("ds4sd/SmolDocling-256M-preview")
    timings['processor_init'] = time.time() - start_time
    print(f"Processor initialization: {timings['processor_init']:.2f} seconds")
    
    start_time = time.time()
    model = AutoModelForVision2Seq.from_pretrained(
        "ds4sd/SmolDocling-256M-preview",
        torch_dtype=torch.bfloat16,
        _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
    ).to(DEVICE)
    timings['model_init'] = time.time() - start_time
    print(f"Model initialization: {timings['model_init']:.2f} seconds")
    
    # Create input messages
    messages = [{
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Convert this page to docling."}
        ]
    }]
    
    # Process image and prepare inputs
    start_time = time.time()
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt").to(DEVICE)
    timings['input_processing'] = time.time() - start_time
    print(f"Input processing: {timings['input_processing']:.2f} seconds")
    
    # Generate outputs
    start_time = time.time()
    generated_ids = model.generate(**inputs, max_new_tokens=8192)
    timings['model_inference'] = time.time() - start_time
    print(f"Model inference: {timings['model_inference']:.2f} seconds")
    
    # Decode outputs
    start_time = time.time()
    trimmed_generated_ids = generated_ids[:, inputs.input_ids.shape[1]:]
    doctags = processor.batch_decode(
        trimmed_generated_ids,
        skip_special_tokens=False,
    )[0].lstrip()
    timings['output_decoding'] = time.time() - start_time
    print(f"Output decoding: {timings['output_decoding']:.2f} seconds")
    
    # Create document
    start_time = time.time()
    doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
    doc = DoclingDocument(name="Document")
    doc.load_from_doctags(doctags_doc)
    timings['document_creation'] = time.time() - start_time
    print(f"Document creation: {timings['document_creation']:.2f} seconds")
    
    # Calculate total time
    timings['total'] = sum(timings.values())
    print(f"Total processing time: {timings['total']:.2f} seconds")
    
    return doc, doctags

def main():
    # Use relative path from project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    image_path = os.path.join(project_root, "input", "sample_img.png")
    
    print(f"Processing document from: {image_path}")
    print(f"Using device: {DEVICE}")
    
    # Record total execution time
    total_start_time = time.time()
    
    # Process document
    doc, doctags = process_document(image_path)
    
    # Print results
    print("\nDocument Processing Completed:")
    print(f"Total script execution time: {time.time() - total_start_time:.2f} seconds")
    
    # Optionally print doctags and markdown output
    # print("\nDocTags:")
    # print(doctags)
    print("\nMarkdown Export:")
    print(doc.export_to_markdown())
    

if __name__ == "__main__":
    main()