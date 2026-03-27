"""
PDF Processing using Azure AI Document Intelligence

Azure AI Document Intelligence (formerly Form Recognizer) is a cloud service
that uses machine learning to extract text, tables, key-value pairs, and
structure from documents. It supports PDFs, images, Office docs, and HTML.

Key Features:
    - Extracts text, tables, forms, and signatures
    - Preserves document structure and layout
    - Supports handwriting recognition
    - Handles scanned documents and images
    - Pre-built models for invoices, receipts, IDs, etc.
    - Custom model training for specialized documents

Dependencies:
    - azure-ai-documentintelligence: pip install azure-ai-documentintelligence

Environment Setup:
    Requires:
        - AZURE_DI_ENDPOINT: Your Azure Document Intelligence endpoint
        - AZURE_DI_KEY: Your Azure Document Intelligence API key

    Get these from Azure Portal -> Create a Document Intelligence resource
    Free tier: 500 pages/month
"""
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from dotenv import load_dotenv
load_dotenv()

AZURE_DI_ENDPOINT = os.getenv("AZURE_DI_ENDPOINT")
AZURE_DI_KEY = os.getenv("AZURE_DI_KEY")

if not AZURE_DI_ENDPOINT or not AZURE_DI_KEY:
    raise ValueError("AZURE_DI_ENDPOINT and AZURE_DI_KEY must be set in .env")


def main():
    """
    Extract text and tables from PDF using Azure Document Intelligence.
    """
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    # Configure input PDF path
    #file_path = project_root + "/input/sample-1.pdf"  # Standard tables
    #file_path = project_root + "/input/sample-2.pdf"  # Image-based simple tables
    file_path = project_root + "/input/sample-3.pdf"   # Image-based complex tables
    #file_path = project_root + "/input/sample-4.pdf"  # Mixed content
    #file_path = project_root + "/input/sample-5.pdf"  # Multi-column texts

    # Initialize the client
    client = DocumentIntelligenceClient(
        endpoint=AZURE_DI_ENDPOINT,
        credential=AzureKeyCredential(AZURE_DI_KEY)
    )

    # Read and analyze the PDF
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read",  # Use "prebuilt-layout" for tables + structure
            body=f.read(),
            content_type="application/pdf"
        )

    result = poller.result()

    # Extract text content
    full_text = ""
    for page in result.pages:
        full_text += f"\n--- Page {page.page_number} ---\n"
        for line in page.lines:
            full_text += line.content + "\n"

    # Extract tables if present (use "prebuilt-layout" model for this)
    if result.tables:
        full_text += "\n\n--- Tables ---\n"
        for i, table in enumerate(result.tables):
            full_text += f"\nTable {i+1} ({table.row_count} rows x {table.column_count} cols):\n"
            rows = {}
            for cell in table.cells:
                rows.setdefault(cell.row_index, {})[cell.column_index] = cell.content
            for row_idx in sorted(rows.keys()):
                row = rows[row_idx]
                full_text += "| " + " | ".join(
                    row.get(c, "") for c in range(table.column_count)
                ) + " |\n"

    print(full_text)

    # Save output
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print("\nOutput saved to output.txt")


if __name__ == "__main__":
    main()
