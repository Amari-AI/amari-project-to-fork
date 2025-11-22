#!/usr/bin/env python3
"""
Debug script to test PDF extraction and OpenAI response
"""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.pdf_utils import extract_text_from_pdf
from app.services.llm_service import extract_field_from_document

def main():
    pdf_path = "/Users/harout/amari-project-to-fork/testDocs/BL-COSU534343282.pdf"
    
    print("=" * 80)
    print("STEP 1: Extracting text from PDF")
    print("=" * 80)
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF file not found at {pdf_path}")
        return
    
    pdf_text = extract_text_from_pdf(pdf_path)
    
    print(f"\nExtracted text length: {len(pdf_text)} characters")
    print("\n" + "=" * 80)
    print("EXTRACTED TEXT (first 1000 characters):")
    print("=" * 80)
    print(pdf_text[:1000])
    print("\n" + "=" * 80)
    print("EXTRACTED TEXT (last 500 characters):")
    print("=" * 80)
    print(pdf_text[-500:])
    
    print("\n" + "=" * 80)
    print("STEP 2: Sending to OpenAI for extraction")
    print("=" * 80)
    
    document_data = {"pdf_text": pdf_text}
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
    
    if "error" in result:
        print(f"\n❌ ERROR: {result['error']}")

if __name__ == "__main__":
    main()
