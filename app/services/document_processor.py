import os
from app.utils.pdf_utils import extract_text_from_pdf

def process_documents(file_paths):
    """
    Process different types of documents and extract relevant information.
    
    Args:
        file_paths: List of paths to the documents
        
    Returns:
        dict: Extracted data from documents
    """
    print(f"DEBUG: Processing {len(file_paths)} files")
    extracted_data = {}
    
    for file_path in file_paths:
        print(f"DEBUG: Processing file: {file_path}")
        print(f"DEBUG: File exists: {os.path.exists(file_path)}")
        
        if file_path.endswith(".pdf"):
            print(f"DEBUG: Processing as PDF")
            pdf_text = extract_text_from_pdf(file_path)
            print(f"DEBUG: Extracted PDF text length: {len(pdf_text)}")
            extracted_data['pdf_text'] = extracted_data.get('pdf_text', "") + "\n" + pdf_text
        elif file_path.endswith(".xlsx"):
            print(f"DEBUG: Processing as XLSX")
            import pandas as pd
            try:
                # Read all sheets
                xls = pd.ExcelFile(file_path)
                text_content = []
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    text_content.append(f"Sheet: {sheet_name}\n{df.to_string()}")
                extracted_data['xlsx_text'] = extracted_data.get('xlsx_text', "") + "\n" + "\n".join(text_content)
                print(f"DEBUG: Extracted XLSX text length: {len(extracted_data['xlsx_text'])}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                extracted_data['xlsx_text'] = extracted_data.get('xlsx_text', "") + f"\nError reading {file_path}"
    
    print(f"DEBUG: Final extracted_data keys: {extracted_data.keys()}")
    return extracted_data 