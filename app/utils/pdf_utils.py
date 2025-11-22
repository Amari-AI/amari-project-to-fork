import PyPDF2
import os
from typing import Optional, List

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file. Supports both text-based and image-based PDFs.
    For image-based PDFs, uses OCR (Optical Character Recognition).
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF file
    """
    text = ""
    
    # First, try standard text extraction with PyPDF2
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    # If no text was extracted OR very little text (likely garbage/partial), use OCR
    if len(text.strip()) < 50:
        print(f"DEBUG: extracted text is too short ({len(text.strip())} chars), attempting OCR...")
        try:
            from pdf2image import convert_from_path
            import pytesseract
            from PIL import Image
            
            # Convert PDF pages to images
            images = convert_from_path(file_path)
            
            # Perform OCR on each page
            for i, image in enumerate(images):
                print(f"DEBUG: Performing OCR on page {i+1}/{len(images)}")
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
            
            print(f"DEBUG: OCR extracted {len(text)} characters")
            
        except ImportError as e:
            print(f"ERROR: OCR libraries not installed. Install with: pip install pdf2image pytesseract Pillow")
            print(f"ERROR: {str(e)}")
            return ""
        except Exception as e:
            print(f"ERROR: OCR failed: {str(e)}")
            return ""
    
    return text
