from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import tempfile

from app.services.document_processor import process_documents
from app.services.llm_service import extract_field_from_document

router = APIRouter()

@router.post("/process-documents", response_model=dict)
async def process_documents_endpoint(
    files: List[UploadFile] = File(...)
):
    print(f"DEBUG: Received {len(files)} files")
    temp_file_paths = []
    for file in files:
        print(f"DEBUG: Processing uploaded file: {file.filename}, content_type: {file.content_type}")
        
        # Extract file extension
        file_ext = os.path.splitext(file.filename)[1]  # e.g., ".pdf" or ".xlsx"
        print(f"DEBUG: File extension: {file_ext}")
        
        # Save uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(suffix=file_ext, delete=False)
        temp_file_paths.append(temp_file.name)
        print(f"DEBUG: Created temp file: {temp_file.name}")

        # Write content to temp file
        content = await file.read()
        print(f"DEBUG: Read {len(content)} bytes from uploaded file")
        temp_file.write(content)
        temp_file.close()

    # Process documents
    document_data = process_documents(temp_file_paths)

    # Extract data from document
    extracted_data = extract_field_from_document(document_data)

    # Clean up temp files
    for path in temp_file_paths:
        os.unlink(path)

    return {"extracted_data": extracted_data} 

@router.get("/health-check/openai")
async def health_check_openai():
    """
    Health check endpoint to verify OpenAI API connectivity using responses.parse()
    """
    from openai import OpenAI
    from pydantic import BaseModel
    import os
    
    class HealthCheckResponse(BaseModel):
        status: str
        message: str
    
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Make a simple test request using the new responses.parse() format
        response = client.responses.parse(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": "You are a health check assistant. Respond with a status and message."},
                {"role": "user", "content": "Perform a health check. Return status as 'OK' and a brief message confirming the API is working."}
            ],
            text_format=HealthCheckResponse,
        )
        
        parsed_response = response.output_parsed
        
        return {
            "status": "success",
            "message": "OpenAI API is accessible",
            "model": "gpt-5-mini",
            "response": {
                "status": parsed_response.status,
                "message": parsed_response.message
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to connect to OpenAI API",
                "error": str(e)
            }
        )
