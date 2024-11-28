"""
PDF to JPG Converter using PyMuPDF (no Poppler required)
Install required package: pip install PyMuPDF
"""

import os
import fitz  # PyMuPDF
import logging

class PDFToJPGConverter:
    def __init__(self):
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.logger = logging.getLogger(__name__)
        
        # Image quality settings
        self.zoom_x = 2.0  # horizontal zoom
        self.zoom_y = 2.0  # vertical zoom
        self.mat = fitz.Matrix(self.zoom_x, self.zoom_y)  # zoom matrix
        
    
    def convert_pdf(self, pdf_path, output_dir):
        """Convert PDF to JPG images"""
        
        try:
            # Check if PDF exists
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            self.logger.info(f"Output directory ready: {output_dir}")

            # Get PDF filename without extension
            pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
            
            # Open PDF file
            self.logger.info(f"Opening PDF: {pdf_path}")
            pdf_document = fitz.open(pdf_path)
            
            converted_files = []
            
            # Convert each page
            for page_number in range(pdf_document.page_count):
                # Get page
                page = pdf_document[page_number]
                
                # Convert page to image
                pix = page.get_pixmap(matrix=self.mat)
                
                # Generate output path
                output_file = os.path.join(
                    output_dir,
                    f"{pdf_filename}_page_{page_number + 1}.jpg"
                )
                
                # Save image
                pix.save(output_file)
                converted_files.append(output_file)
                
                self.logger.info(f"Saved page {page_number + 1} to: {output_file}")
            
            # Close PDF
            pdf_document.close()
            
            self.logger.info(f"Successfully converted {len(converted_files)} pages")
            return converted_files
            
        except Exception as e:
            self.logger.error(f"Error during conversion: {str(e)}")
            raise
