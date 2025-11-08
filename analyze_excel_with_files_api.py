#!/usr/bin/env python3
"""
Simplified Example: Upload and Analyze Excel File
-------------------------------------------------
A simpler pattern showing file upload and direct analysis.

This example shows the minimal code needed to:
1. Upload an Excel file
2. Ask Claude to analyze it
3. Get a response

Prerequisites:
- pip install anthropic
- Set ANTHROPIC_API_KEY environment variable
"""

import anthropic
import os


def analyze_excel_file(file_path: str, analysis_question: str):
    """
    Upload an Excel file and ask Claude to analyze it.

    Args:
        file_path: Path to the Excel file to analyze
        analysis_question: Question or task for Claude to perform

    Returns:
        String containing Claude's analysis
    """

    # ========================================================================
    # INITIALIZATION
    # ========================================================================

    # Create client with Files API enabled
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        default_headers={
            # Enable the Files API beta feature
            "anthropic-beta": "files-api-2025-04-14,code-execution-2025-08-25"
        }
    )


    # ========================================================================
    # UPLOAD FILE
    # ========================================================================

    print(f"Uploading: {file_path}")

    # Upload the Excel file to Claude's file storage
    with open(file_path, 'rb') as f:
        file_obj = client.files.create(
            file=f,
            purpose="user_upload"  # Indicates this is a user-provided file
        )

    # The file_id is the unique identifier we'll use to reference this file
    file_id = file_obj.id
    print(f"✓ Uploaded. File ID: {file_id}\n")


    # ========================================================================
    # SEND ANALYSIS REQUEST
    # ========================================================================

    # Build the prompt
    # IMPORTANT: Include the file_id in your prompt so Claude knows to access it
    prompt = f"""I've uploaded an Excel file with file_id: {file_id}

Please use code execution with openpyxl or pandas to analyze this file.

{analysis_question}"""

    print("Sending analysis request to Claude...")

    # Send the message to Claude
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        # Enable code execution so Claude can load and analyze the file
        tools=[
            {
                "type": "code_execution_20250825",
                "name": "code_execution"
            }
        ]
    )

    print("✓ Received response\n")


    # ========================================================================
    # EXTRACT TEXT RESPONSE
    # ========================================================================

    # The response.content is a list of content blocks
    # We'll extract all text blocks and concatenate them

    response_text = ""

    for block in response.content:
        if block.type == "text":
            # This is Claude's text response
            response_text += block.text + "\n"

        elif block.type == "tool_use":
            # Claude executed code - show what it did
            response_text += f"\n[Claude executed Python code]\n"
            if hasattr(block, 'input') and 'code' in block.input:
                response_text += f"Code:\n{block.input['code']}\n\n"

    return response_text


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":

    # Example 1: Basic structure analysis
    print("="*70)
    print("EXAMPLE 1: Analyze workbook structure")
    print("="*70 + "\n")

    result1 = analyze_excel_file(
        file_path="/home/user/INCOSE-HWG-2024/sample_survey.xlsx",
        analysis_question="""
Please analyze this Excel workbook and tell me:
1. How many sheets does it have?
2. What are the sheet names?
3. Which sheet appears to contain questionnaire data?
4. How many rows of data are in the first sheet?
"""
    )

    print("CLAUDE'S RESPONSE:")
    print("-" * 70)
    print(result1)
    print("\n")


    # Example 2: Find specific content
    print("="*70)
    print("EXAMPLE 2: Search for specific content")
    print("="*70 + "\n")

    result2 = analyze_excel_file(
        file_path="/home/user/INCOSE-HWG-2024/sample_survey.xlsx",
        analysis_question="""
Search through all sheets and find any cells that contain the text "Required Questions".
Tell me which sheet(s) contain this text and what row numbers.
"""
    )

    print("CLAUDE'S RESPONSE:")
    print("-" * 70)
    print(result2)
    print("\n")


# ============================================================================
# KEY POINTS TO REMEMBER
# ============================================================================

"""
KEY POINTS:

1. FILE UPLOAD:
   - Use client.files.create() to upload files
   - Set purpose="user_upload"
   - Save the file_id from the response

2. REFERENCING FILES IN PROMPTS:
   - Include the file_id in your prompt text
   - Tell Claude to use code execution to access it
   - Suggest using openpyxl or pandas for Excel files

3. CODE EXECUTION:
   - Add code_execution tool to enable Python code execution
   - Claude can then write and run code to analyze the file
   - Code runs in a sandboxed environment with the uploaded file available

4. RESPONSE HANDLING:
   - response.content is a list of blocks
   - block.type can be "text" or "tool_use"
   - Text blocks contain Claude's analysis
   - Tool_use blocks show code Claude executed

5. COMMON PATTERNS:

   Pattern A - Direct analysis (what we show here):
   → Upload file → Send prompt with file_id → Get response

   Pattern B - Multi-turn with code results:
   → Upload file → Send prompt → Claude executes code
   → Send tool results back → Get final analysis

   Pattern C - Structured output:
   → Request JSON format in prompt
   → Parse JSON from response.content[0].text
   → Use json.loads() after stripping markdown fences

6. ERROR HANDLING:
   - Always wrap in try/except blocks
   - Handle: AuthenticationError, RateLimitError, APIConnectionError
   - Check file uploads succeeded before using file_id
   - Validate JSON parsing if expecting structured output

7. BETA HEADERS:
   - files-api-2025-04-14: Required for file upload
   - code-execution-2025-08-25: Required for code execution
   - Include both in default_headers when initializing client
"""
