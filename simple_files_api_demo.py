#!/usr/bin/env python3
"""
Simple demonstration of how file_id is used in the Files API.
This shows the minimal pattern for file upload and access.
"""

import anthropic
import os


def demo_file_access():
    """
    Demonstrates how files are accessed in code execution environment.
    """

    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        default_headers={
            "anthropic-beta": "files-api-2025-04-14,code-execution-2025-08-25"
        }
    )

    # ============================================================================
    # STEP 1: Upload file and get file_id
    # ============================================================================

    file_path = "/home/user/INCOSE-HWG-2024/sample_survey.xlsx"

    print("Step 1: Uploading file...")
    with open(file_path, 'rb') as f:
        file_obj = client.files.create(file=f, purpose="user_upload")

    file_id = file_obj.id
    print(f"  ✓ File uploaded with ID: {file_id}\n")


    # ============================================================================
    # STEP 2: Send prompt with file_id embedded
    # ============================================================================

    print("Step 2: Sending request to Claude...")
    print(f"  → Prompt will reference: {file_id}\n")

    # The file_id is included in the prompt text
    prompt = f"""I've uploaded a file with file_id: {file_id}

Please write Python code to:
1. Load this Excel file using the file_id directly as the file path
2. Print the workbook sheet names
3. Show me the exact code you use to open the file

Important: Use the file_id directly - it acts as a file path in your environment."""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
    )


    # ============================================================================
    # STEP 3: Show what code Claude executed
    # ============================================================================

    print("Step 3: Claude's response:\n")
    print("=" * 70)

    for block in response.content:
        if block.type == "text":
            print(f"TEXT: {block.text}\n")

        elif block.type == "tool_use":
            print("CODE EXECUTED:")
            print("-" * 70)
            if hasattr(block, 'input') and 'code' in block.input:
                print(block.input['code'])
            print("-" * 70)
            print()

    print("=" * 70)
    print("\nKEY INSIGHT:")
    print("The file_id acts as a direct file path in the code execution environment.")
    print("Claude can use it like: openpyxl.load_workbook(file_id)")
    print("No additional API calls needed - the file is already available!")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        exit(1)

    demo_file_access()
