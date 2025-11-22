# Document Processing Application

A production-ready application that processes shipment documents (PDF, XLSX) and extracts structured data using AI.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- OpenAI API key (already configured)

### Installation & Running

**Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Access:** Open `http://localhost:5174` in your browser

### Testing

**Run all tests:**
```bash
source venv/bin/activate
python -m pytest tests/test_app.py -v
```

**Generate sample test documents:**
```bash
source venv/bin/activate
python create_test_docs.py
```

## 📋 Features

- ✅ Upload multiple documents (PDF, XLSX)
- ✅ AI-powered data extraction using GPT-5-mini
- ✅ Editable form with extracted data
- ✅ Side-by-side document preview
- ✅ Comprehensive test suite (8 tests passing)
- ✅ Sample test documents included

## 🧪 Test Files

Sample documents are available in `tests/`:
- `sample_bill_of_lading.pdf` - Bill of lading with shipping details
- `sample_invoice.xlsx` - Commercial invoice with line items

## 📦 Tech Stack

**Backend:**
- FastAPI
- Anthropic Claude 3 Haiku
- PyPDF2 (PDF extraction)
- Pandas (XLSX processing)

**Frontend:**
- React + Vite
- Tailwind CSS
- Axios

## 🔧 Configuration

LLM settings are in `app/services/llm_service.py`:
- Model: `claude-3-haiku-20240307`
- Provider: Anthropic

## 📝 Extracted Fields

- Bill of lading number
- Container Number
- Consignee Name
- Consignee Address
- Date of export
- Date
- Line Items Count
- Average Gross Weight
- Average Price

## 🎯 Next Steps

- [ ] Docker containerization
- [ ] Evaluation script (accuracy, precision, recall, F1)
- [ ] Additional unit tests
- [ ] OCR support for scanned documents