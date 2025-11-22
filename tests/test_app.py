"""
Unit tests for the document processing application.
"""
import pytest
import os
import sys
from fastapi.testclient import TestClient

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.services.document_processor import process_documents
from app.utils.pdf_utils import extract_text_from_pdf

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_process_documents_no_files(self):
        """Test process-documents endpoint with no files"""
        response = client.post("/process-documents")
        assert response.status_code == 422  # Validation error
    
    def test_process_documents_with_files(self):
        """Test process-documents endpoint with sample files"""
        # Check if test files exist
        pdf_path = "tests/sample_bill_of_lading.pdf"
        xlsx_path = "tests/sample_invoice.xlsx"
        
        if not os.path.exists(pdf_path) or not os.path.exists(xlsx_path):
            pytest.skip("Test files not found")
        
        with open(pdf_path, "rb") as pdf_file, open(xlsx_path, "rb") as xlsx_file:
            files = [
                ("files", ("bill_of_lading.pdf", pdf_file, "application/pdf")),
                ("files", ("invoice.xlsx", xlsx_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
            ]
            response = client.post("/process-documents", files=files)
        
        assert response.status_code == 200
        assert "extracted_data" in response.json()


class TestDocumentProcessor:
    """Test document processing functions"""
    
    def test_extract_text_from_pdf(self):
        """Test PDF text extraction"""
        pdf_path = "tests/sample_bill_of_lading.pdf"
        
        if not os.path.exists(pdf_path):
            pytest.skip("Test PDF not found")
        
        text = extract_text_from_pdf(pdf_path)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "BILL OF LADING" in text or "BOL" in text
    
    def test_process_documents_pdf(self):
        """Test processing PDF documents"""
        pdf_path = "tests/sample_bill_of_lading.pdf"
        
        if not os.path.exists(pdf_path):
            pytest.skip("Test PDF not found")
        
        result = process_documents([pdf_path])
        assert isinstance(result, dict)
        assert "pdf_text" in result
        assert len(result["pdf_text"]) > 0
    
    def test_process_documents_xlsx(self):
        """Test processing XLSX documents"""
        xlsx_path = "tests/sample_invoice.xlsx"
        
        if not os.path.exists(xlsx_path):
            pytest.skip("Test XLSX not found")
        
        result = process_documents([xlsx_path])
        assert isinstance(result, dict)
        assert "xlsx_text" in result
        assert len(result["xlsx_text"]) > 0
    
    def test_process_documents_mixed(self):
        """Test processing both PDF and XLSX documents"""
        pdf_path = "tests/sample_bill_of_lading.pdf"
        xlsx_path = "tests/sample_invoice.xlsx"
        
        if not os.path.exists(pdf_path) or not os.path.exists(xlsx_path):
            pytest.skip("Test files not found")
        
        result = process_documents([pdf_path, xlsx_path])
        assert isinstance(result, dict)
        assert "pdf_text" in result
        assert "xlsx_text" in result
        assert len(result["pdf_text"]) > 0
        assert len(result["xlsx_text"]) > 0


class TestDataExtraction:
    """Test data extraction from documents"""
    
    def test_extracted_fields_structure(self):
        """Test that extracted data contains expected fields"""
        # This would require mocking the LLM response
        # For now, we'll just test the structure
        expected_fields = [
            "Bill of lading number",
            "Container Number",
            "Consignee Name",
            "Consignee Address",
            "Date of export",
            "Date",
            "Line Items Count",
            "Average Gross Weight",
            "Average Price"
        ]
        
        # This is a placeholder - in a real test, you'd mock the LLM
        assert len(expected_fields) == 9


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
