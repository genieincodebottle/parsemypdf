"""
PDF Table Extraction Script

This script focuses on extracting tables from PDF documents using the Camelot library. 
It supports various PDF formats and can handle different types of table structures within 
PDF documents.

Key Features:
    - Extracts tables from PDF documents
    - Supports multiple PDF formats (standard tables, image-based tables)
    - Exports extracted tables to CSV format
    - Optional compression for large datasets

Dependencies:
    - camelot-py
    - ghostscript (system requirement)
    - pdf2image
    - opencv-python

Note: Requires Ghostscript to be properly configured on the system
"""
# Import camelot library for extracting tables from PDFs
import os
import camelot

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def main():
    """
    Main function to extract tables from PDF files using Camelot library.
    """
    # Define input PDF file path
    # Multiple test files available for different scenarios:
    file_path = project_root+"/input/sample-1.pdf"  # Contains standard table format
    #file_path = project_root+"/input/sample-2.pdf" # Contains image-based simple table
    #file_path = project_root+"/input/sample-3.pdf" # Contains image-based complex table
    #file_path = project_root+"/input/sample-4.pdf" # Complex PDF with mixed content (text and tables in images)
    #file_path = project_root+"/input/sample-5.pdf"  # Multi-column Texts 
    
    # Extract tables from the PDF
    # camelot.read_pdf returns a TableList object containing all detected tables
    tables = camelot.read_pdf(file_path)
    
    # Export extracted tables to CSV format
    # Parameters:
    #   - 'output/table.csv': Output file path
    #   - f='csv': Specify output format as CSV
    tables.export("/output/table.csv', f='csv')
    
    # Alternative export with compression (commented out)
    # Useful for large tables or when storage space is a concern
    #tables.export('output/table.csv', f='csv', compress=True)

# Execute main function if script is run directly
if __name__ == "__main__":
    main()