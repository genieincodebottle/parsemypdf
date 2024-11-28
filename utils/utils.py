import base64
import fitz  # PyMuPDF
import math
import io

def read_pdf_in_pairs(file_name):
    """
    Read PDF two pages at a time and base64 encode them
    Returns:
        - Total number of pages
        - Dictionary containing pairs of pages encoded in base64
        - Number of pairs
    """
    result = {}
    
    # Open the PDF and get page count
    doc = fitz.open(file_name)
    total_pages = len(doc)
    number_of_pairs = math.ceil(total_pages / 2)
    
    base64_content = []
    # Read pages in pairs
    for pair_num in range(number_of_pairs):
        # Calculate page indices for current pair
        start_idx = pair_num * 2
        end_idx = min(start_idx + 2, total_pages)
        
        # Create a new PDF document for this pair
        output_doc = fitz.open()
        
        # Add pages to the new document
        for page_idx in range(start_idx, end_idx):
            page = doc[page_idx]
            output_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
        
        # Save the pair to bytes
        output_buffer = io.BytesIO()
        output_doc.save(output_buffer)
        pair_content = output_buffer.getvalue()
        
        # Convert to base64 and store in result
        base64_content.append(base64.b64encode(pair_content).decode("utf-8"))
                
        # Close the temporary document
        output_doc.close()
        output_buffer.close()
    
    doc.close()
    return base64_content

