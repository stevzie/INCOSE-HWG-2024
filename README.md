# INCOSE-HWG-2024
Presentation from the 9th Annual Systems Engineering in Healthcare Conference

## Excel File Upload API

A FastAPI-based REST API for uploading and processing Excel files (.xlsx, .xls, .xlsm).

### Features

- Upload Excel files via REST API
- Automatic validation of file format and size
- Support for multiple Excel formats (.xlsx, .xls, .xlsm)
- Extract and process data from Excel sheets
- Parse specific sheets or default to first sheet
- Get statistics and preview of uploaded data
- Built-in API documentation (Swagger UI and ReDoc)
- Comprehensive error handling and logging

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd INCOSE-HWG-2024
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the API

**Start the development server:**
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API information |
| GET | `/health` | Health check endpoint |
| GET | `/info` | Detailed API information and usage examples |
| POST | `/upload-excel/` | Upload and process Excel file |
| POST | `/upload-excel/sheets/{sheet_name}` | Upload and process specific sheet |
| GET | `/docs` | Interactive API documentation (Swagger UI) |
| GET | `/redoc` | Alternative API documentation (ReDoc) |

### Usage Examples

#### Using cURL

**Upload an Excel file:**
```bash
curl -X POST "http://localhost:8000/upload-excel/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_file.xlsx"
```

**Upload and process a specific sheet:**
```bash
curl -X POST "http://localhost:8000/upload-excel/sheets/Sheet2" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_file.xlsx"
```

#### Using Python

```python
import requests

# Upload Excel file
with open('your_file.xlsx', 'rb') as f:
    response = requests.post('http://localhost:8000/upload-excel/', files={'file': f})
    data = response.json()
    print(data)
```

#### Using JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/upload-excel/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### API Response Format

**Success Response:**
```json
{
    "success": true,
    "sheet_name": "Sheet1",
    "available_sheets": ["Sheet1", "Sheet2"],
    "statistics": {
        "total_rows": 100,
        "total_columns": 5,
        "columns": ["Column1", "Column2", "Column3", "Column4", "Column5"]
    },
    "data": [
        {"Column1": "value1", "Column2": "value2", ...},
        ...
    ],
    "preview": [
        {"Column1": "value1", "Column2": "value2", ...}
    ],
    "file_info": {
        "filename": "your_file.xlsx",
        "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "size_bytes": 12345
    }
}
```

**Error Response:**
```json
{
    "detail": "Error message describing what went wrong"
}
```

### Configuration

- **Maximum file size:** 10MB
- **Supported formats:** .xlsx, .xls, .xlsm
- **Default port:** 8000

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These provide interactive documentation where you can test the API directly from your browser.

### Error Handling

The API includes comprehensive error handling for:
- Invalid file formats
- Files exceeding size limits
- Corrupted Excel files
- Missing or invalid sheets
- Server errors

### Development

**Project Structure:**
```
INCOSE-HWG-2024/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── *.pdf                  # Conference materials
```

### License

This project is part of the INCOSE Healthcare Working Group 2024 conference materials.
