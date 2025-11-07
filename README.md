# INCOSE-HWG-2024
Presentation from the 9th Annual Systems Engineering in Healthcare Conference

## Excel File Upload to Claude API

Python utility for uploading Excel files to Claude AI (Sonnet) via the Anthropic API in base64 format. This allows you to send Excel spreadsheets to Claude for analysis, summarization, data extraction, and other AI-powered tasks.

### Features

- Upload Excel files (.xlsx, .xls, .xlsm) to Claude API in base64 format
- Automatic base64 encoding of Excel files
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

#### Python Code - Advanced Usage

```python
from excel_to_claude import ExcelToClaudeUploader

# Initialize uploader
uploader = ExcelToClaudeUploader(api_key="your-api-key")

# Upload Excel file with custom settings
response = uploader.upload_excel_with_prompt(
    excel_file_path="data.xlsx",
    prompt="What trends do you see in this data?",
    model="claude-sonnet-4-20250514",
    max_tokens=4096
)

# Get text response
text = uploader.get_response_text(response)
print(text)

# Access token usage
print(f"Input tokens: {response['usage']['input_tokens']}")
print(f"Output tokens: {response['usage']['output_tokens']}")
```

### Usage Examples

The `example_usage.py` file contains comprehensive examples including:

1. **Simple usage** - Quick upload and response
2. **Class-based usage** - More control over the process
3. **Data analysis tasks** - Multiple prompts for analysis
4. **Multiple files** - Process several Excel files
5. **Base64 encoding only** - Get base64 without sending to API
6. **Different models** - Compare responses from different Claude models

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
- `encode_excel_to_base64(file_path)` - Encode Excel to base64
- `upload_excel_with_prompt(excel_file_path, prompt, model, max_tokens)` - Upload and get response
- `get_response_text(response)` - Extract text from response

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

- Excel files are converted to base64 before being sent to Claude
- Claude can analyze the structure and content of Excel files
- Response quality depends on the complexity of your prompt
- Token usage varies based on file size and response length

### License

This project is part of the INCOSE Healthcare Working Group 2024 conference materials.
