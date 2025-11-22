#!/usr/bin/env python3
"""
Debug script to test combined PDF and XLSX extraction
"""
import sys
import os
import pandas as pd

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.pdf_utils import extract_text_from_pdf
from app.services.llm_service import extract_field_from_document

def main():
    pdf_path = "/Users/harout/amari-project-to-fork/testDocs/BL-COSU534343282.pdf"
    xlsx_path = "/Users/harout/amari-project-to-fork/testDocs/Demo-Invoice-PackingList_1.xlsx"
    
    print("=" * 80)
    print("STEP 1: Extracting text from PDF")
    print("=" * 80)
    
    pdf_text = extract_text_from_pdf(pdf_path)
    print(f"PDF Text Length: {len(pdf_text)}")
    print(f"PDF Preview: {pdf_text[:200] if pdf_text else 'EMPTY'}")
    
    print("\n" + "=" * 80)
    print("STEP 2: Extracting text from XLSX")
    print("=" * 80)
    
    xlsx_text = ""
    try:
        xls = pd.ExcelFile(xlsx_path)
        text_content = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            text_content.append(f"Sheet: {sheet_name}\n{df.to_string()}")
        xlsx_text = "\n".join(text_content)
        print(f"XLSX Text Length: {len(xlsx_text)}")
        print(f"XLSX Preview: {xlsx_text[:200] if xlsx_text else 'EMPTY'}")
    except Exception as e:
        print(f"Error reading XLSX: {e}")
        return

    print("\n" + "=" * 80)
    print("STEP 3: Sending COMBINED data to OpenAI")
    print("=" * 80)
    
    document_data = {
        "pdf_text": pdf_text,
        "xlsx_text": xlsx_text
    }
    
    result = extract_field_from_document(document_data)
    
    print("\n" + "=" * 80)
    print("OPENAI RESPONSE:")
    print("=" * 80)
    import json
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 80)
    print("ANALYSIS:")
    print("=" * 80)
    
    # Check if all fields are null
    null_fields = []
    non_null_fields = []
    
    for key, value in result.items():
        if key != "error":
            if value is None:
                null_fields.append(key)
            else:
                non_null_fields.append(key)
    
    if null_fields:
        print(f"\n⚠️  NULL FIELDS ({len(null_fields)}):")
        for field in null_fields:
            print(f"  - {field}")
    
    if non_null_fields:
        print(f"\n✅ NON-NULL FIELDS ({len(non_null_fields)}):")
        for field in non_null_fields:
            print(f"  - {field}: {result[field]}")

if __name__ == "__main__":
    main()
