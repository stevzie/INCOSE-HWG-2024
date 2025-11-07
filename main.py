from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import openpyxl
from io import BytesIO
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Excel File Upload API",
    description="API for uploading and processing Excel files",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Excel File Upload API is running",
        "status": "healthy",
        "endpoints": {
            "upload": "/upload-excel/",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


def validate_excel_file(filename: str, content: bytes) -> Dict[str, Any]:
    """
    Validate that the uploaded file is a valid Excel file

    Args:
        filename: Name of the uploaded file
        content: File content in bytes

    Returns:
        Dict with validation status and message

    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    allowed_extensions = ['.xlsx', '.xls', '.xlsm']
    file_ext = filename[filename.rfind('.'):].lower() if '.' in filename else ''

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )

    # Check file size (limit to 10MB)
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of 10MB"
        )

    # Try to open with openpyxl to verify it's a valid Excel file
    try:
        workbook = openpyxl.load_workbook(BytesIO(content), read_only=True)
        sheet_names = workbook.sheetnames
        workbook.close()
        return {
            "valid": True,
            "message": "File is a valid Excel file",
            "sheet_names": sheet_names
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Excel file format: {str(e)}"
        )


def process_excel_file(content: bytes, sheet_name: str = None) -> Dict[str, Any]:
    """
    Process Excel file and extract data

    Args:
        content: File content in bytes
        sheet_name: Optional specific sheet to read (defaults to first sheet)

    Returns:
        Dict containing processed data and metadata
    """
    try:
        # Read Excel file with pandas
        excel_file = pd.ExcelFile(BytesIO(content))

        # Get all sheet names
        sheet_names = excel_file.sheet_names

        # Determine which sheet to read
        target_sheet = sheet_name if sheet_name and sheet_name in sheet_names else sheet_names[0]

        # Read the sheet
        df = pd.read_excel(excel_file, sheet_name=target_sheet)

        # Convert DataFrame to dict with proper handling of NaN values
        data = df.fillna('').to_dict(orient='records')

        # Get column information
        columns = list(df.columns)

        # Get basic statistics
        stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": columns
        }

        return {
            "success": True,
            "sheet_name": target_sheet,
            "available_sheets": sheet_names,
            "statistics": stats,
            "data": data,
            "preview": data[:5] if len(data) > 5 else data  # First 5 rows as preview
        }

    except Exception as e:
        logger.error(f"Error processing Excel file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing Excel file: {str(e)}"
        )


@app.post("/upload-excel/")
async def upload_excel_file(
    file: UploadFile = File(...),
    sheet_name: str = None
):
    """
    Upload and process an Excel file

    Args:
        file: Excel file to upload (.xlsx, .xls, .xlsm)
        sheet_name: Optional specific sheet name to process (defaults to first sheet)

    Returns:
        JSON response with processed data and metadata

    Example:
        ```bash
        curl -X POST "http://localhost:8000/upload-excel/" \
             -H "accept: application/json" \
             -H "Content-Type: multipart/form-data" \
             -F "file=@your_file.xlsx"
        ```
    """
    logger.info(f"Received file upload: {file.filename}")

    try:
        # Read file content
        content = await file.read()

        # Validate the file
        validation_result = validate_excel_file(file.filename, content)
        logger.info(f"File validation successful: {file.filename}")

        # Process the Excel file
        result = process_excel_file(content, sheet_name)

        # Add file metadata to result
        result["file_info"] = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(content)
        }

        logger.info(f"File processed successfully: {file.filename}")
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post("/upload-excel/sheets/{sheet_name}")
async def upload_excel_file_specific_sheet(
    sheet_name: str,
    file: UploadFile = File(...)
):
    """
    Upload and process a specific sheet from an Excel file

    Args:
        sheet_name: Name of the sheet to process
        file: Excel file to upload

    Returns:
        JSON response with processed data from the specified sheet
    """
    return await upload_excel_file(file, sheet_name)


@app.get("/info")
async def api_info():
    """Get API information and usage instructions"""
    return {
        "api": "Excel File Upload API",
        "version": "1.0.0",
        "description": "Upload and process Excel files",
        "supported_formats": [".xlsx", ".xls", ".xlsm"],
        "max_file_size": "10MB",
        "endpoints": {
            "POST /upload-excel/": "Upload and process Excel file",
            "POST /upload-excel/sheets/{sheet_name}": "Upload and process specific sheet",
            "GET /": "Root endpoint",
            "GET /health": "Health check",
            "GET /info": "API information",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation (ReDoc)"
        },
        "usage_example": {
            "curl": "curl -X POST 'http://localhost:8000/upload-excel/' -F 'file=@your_file.xlsx'",
            "python": """
import requests

with open('your_file.xlsx', 'rb') as f:
    response = requests.post('http://localhost:8000/upload-excel/', files={'file': f})
    print(response.json())
"""
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
