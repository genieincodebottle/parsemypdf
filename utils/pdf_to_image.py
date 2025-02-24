"""
PDF to JPG Converter using PyMuPDF (no Poppler required)
Install required package: pip install PyMuPDF
"""

import os
import fitz  # PyMuPDF
import logging
from typing import Union, List, Optional
from PIL import Image
import io

class PDFToJPGConverter:
    def __init__(self):
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.logger = logging.getLogger(__name__)
        
        # Image quality settings
        self.zoom_x = 2.0  # horizontal zoom
        self.zoom_y = 2.0  # vertical zoom
        self.mat = fitz.Matrix(self.zoom_x, self.zoom_y)  # zoom matrix
        
    
    def convert_pdf(self, 
                   pdf_input: Union[str, bytes], 
                   output_dir: Optional[str] = None,
                   save_to_disk: bool = False) -> Union[List[Image.Image], List[str]]:
        """
        Convert PDF to images. Can handle both file paths and byte content.
        
        Args:
            pdf_input (Union[str, bytes]): Either a file path or PDF content as bytes
            output_dir (Optional[str]): Directory to save images if save_to_disk is True
            save_to_disk (bool): Whether to save images to disk
            
        Returns:
            Union[List[Image.Image], List[str]]: List of PIL Images or file paths depending on save_to_disk
            
        Raises:
            FileNotFoundError: If pdf_input is a file path that doesn't exist
            ValueError: If input type is not recognized
        """
        try:
            # Determine input type and open PDF accordingly
            if isinstance(pdf_input, str):
                # Input is a file path
                if not os.path.exists(pdf_input):
                    raise FileNotFoundError(f"PDF file not found: {pdf_input}")
                self.logger.info(f"Opening PDF from file: {pdf_input}")
                pdf_document = fitz.open(pdf_input)
                pdf_filename = os.path.splitext(os.path.basename(pdf_input))[0]
            elif isinstance(pdf_input, bytes):
                # Input is bytes
                self.logger.info("Opening PDF from bytes")
                pdf_document = fitz.open(stream=pdf_input, filetype="pdf")
                pdf_filename = "pdf_converted"
            else:
                raise ValueError("pdf_input must be either a file path (str) or bytes")

            # Create output directory if saving to disk
            if save_to_disk:
                if output_dir is None:
                    raise ValueError("output_dir must be specified when save_to_disk is True")
                os.makedirs(output_dir, exist_ok=True)
                self.logger.info(f"Output directory ready: {output_dir}")

            converted_items = []

            # Convert each page
            for page_number in range(pdf_document.page_count):
                # Get page and convert to pixmap
                page = pdf_document[page_number]
                pix = page.get_pixmap(matrix=self.mat)

                if save_to_disk:
                    # Save to file and store path
                    output_file = os.path.join(
                        output_dir,
                        f"{pdf_filename}_page_{page_number + 1}.jpg"
                    )
                    pix.save(output_file)
                    converted_items.append(output_file)
                    self.logger.info(f"Saved page {page_number + 1} to: {output_file}")
                else:
                    # Convert to PIL Image and store image
                    img_data = pix.tobytes("jpeg")
                    img = Image.open(io.BytesIO(img_data))
                    converted_items.append(img)
                    self.logger.info(f"Converted page {page_number + 1} to PIL Image")

            # Close PDF
            pdf_document.close()

            self.logger.info(f"Successfully converted {len(converted_items)} pages")
            return converted_items

        except Exception as e:
            self.logger.error(f"Error during conversion: {str(e)}")
            raise
