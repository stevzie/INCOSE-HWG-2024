# INCOSE-HWG-2024
Presentation from the 9th Annual Systems Engineering in Healthcare Conference

## Excel File Upload to Claude API

Python utility for uploading Excel files to Claude AI (Sonnet) via the Anthropic **Files API**. This allows you to send Excel spreadsheets to Claude for analysis, summarization, data extraction, and other AI-powered tasks.

### Features

- Upload Excel files (.xlsx, .xls, .xlsm) to Claude API using the Files API
- Get reusable file IDs for efficient multiple queries on the same file
- Automatic file caching to avoid re-uploading
- Support for multiple Claude models (Sonnet 4, Opus, etc.)
- Simple function-based and class-based interfaces
- Comprehensive error handling
- Extract responses from Claude about your Excel data

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

4. **Set up your Anthropic API key**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or on Windows:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

Get your API key from: https://console.anthropic.com/

### Quick Start

#### Command Line Usage

```bash
python excel_to_claude.py your_file.xlsx "Summarize this data"
```

#### Python Code - Simple Usage

```python
from excel_to_claude import upload_excel_to_claude

response = upload_excel_to_claude(
    file_path="sales_data.xlsx",
    prompt="Analyze this sales data and provide key insights."
)
print(response)
```

#### Python Code - Advanced Usage (Upload Once, Query Multiple Times)

```python
from excel_to_claude import ExcelToClaudeUploader

# Initialize uploader
uploader = ExcelToClaudeUploader(api_key="your-api-key")

# Step 1: Upload file and get file_id
file_id = uploader.upload_file("data.xlsx")
print(f"File ID: {file_id}")

# Step 2: Query the file multiple times using the file_id
questions = [
    "What trends do you see in this data?",
    "What are the column names?",
    "How many rows are there?"
]

for question in questions:
    response = uploader.send_message_with_file(
        file_id=file_id,
        prompt=question,
        model="claude-sonnet-4-20250514",
        max_tokens=1024
    )

    # Get text response
    text = uploader.get_response_text(response)
    print(f"Q: {question}")
    print(f"A: {text}\n")

    # Access token usage
    print(f"Tokens: {response['usage']['input_tokens']} in, "
          f"{response['usage']['output_tokens']} out\n")
```

### Usage Examples

The `example_usage.py` file contains comprehensive examples including:

1. **Simple usage** - Quick upload and response
2. **Upload once, query multiple times** - Efficient file ID reuse
3. **Full response details** - Access metadata and token usage
4. **Automatic file caching** - Avoid re-uploading same files
5. **Manual file ID reuse** - Explicitly pass file IDs
6. **Multiple files** - Process several Excel files
7. **Different models** - Compare responses from different Claude models
8. **Error handling** - Proper exception handling

Run examples:
```bash
python example_usage.py
```

### API Reference

#### `upload_excel_to_claude(file_path, prompt, api_key=None, model="claude-sonnet-4-20250514")`

Convenience function to upload Excel and get Claude's response.

**Parameters:**
- `file_path` (str): Path to Excel file
- `prompt` (str): Question/prompt about the file
- `api_key` (str, optional): Anthropic API key
- `model` (str): Claude model to use

**Returns:** Text response from Claude

#### `ExcelToClaudeUploader` Class

**Methods:**

- `__init__(api_key=None)` - Initialize with API key
- `upload_file(file_path)` - Upload Excel file to Files API, returns `file_id`
- `send_message_with_file(file_id, prompt, model, max_tokens)` - Send message using existing file_id
- `upload_excel_with_prompt(excel_file_path, prompt, model, max_tokens, reuse_file_id=None)` - All-in-one: upload and query
- `get_response_text(response)` - Extract text from response

**Key Features:**
- Automatic file caching prevents re-uploading the same file
- File IDs can be reused across multiple queries
- Returns file_id in response for manual reuse

### Supported Excel Formats

- `.xlsx` - Excel 2007+ (OpenXML)
- `.xls` - Excel 97-2003
- `.xlsm` - Excel with macros

### Supported Claude Models

- `claude-sonnet-4-20250514` - Latest Sonnet (recommended)
- `claude-3-5-sonnet-20241022` - Sonnet 3.5
- `claude-opus-4-20250514` - Most capable (higher cost)

### Example Use Cases

**Data Analysis:**
```python
response = upload_excel_to_claude(
    "sales.xlsx",
    "Calculate total revenue by region and identify top 5 products."
)
```

**Data Validation:**
```python
response = upload_excel_to_claude(
    "customer_data.xlsx",
    "Check for missing values, duplicates, and data quality issues."
)
```

**Data Summarization:**
```python
response = upload_excel_to_claude(
    "survey_results.xlsx",
    "Provide a summary of survey responses with key findings."
)
```

**Format Conversion:**
```python
response = upload_excel_to_claude(
    "data.xlsx",
    "Convert this data to JSON format."
)
```

### Project Structure

```
INCOSE-HWG-2024/
├── excel_to_claude.py      # Main library module
├── example_usage.py        # Comprehensive usage examples
├── requirements.txt        # Python dependencies (anthropic)
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── *.pdf                  # Conference materials
```

### Error Handling

The library handles common errors:
- Missing or invalid API key
- File not found
- Unsupported file format
- API request errors
- Invalid responses

### Notes

- **Files API**: Excel files are uploaded to Claude's Files API and referenced by file_id
- **File Reuse**: Upload once, query multiple times with the same file_id for efficiency
- **Automatic Caching**: The same file won't be re-uploaded within a session
- **Beta Feature**: Uses the Files API beta header `files-api-2025-04-14`
- Claude can analyze the structure and content of Excel files
- Response quality depends on the complexity of your prompt
- Token usage varies based on file size and response length

### How It Works

1. **Upload**: File is uploaded to `/v1/files` endpoint → returns `file_id`
2. **Query**: Messages reference the `file_id` instead of sending file data
3. **Efficiency**: Reuse the same `file_id` for multiple questions about the same file

### License

This project is part of the INCOSE Healthcare Working Group 2024 conference materials.
