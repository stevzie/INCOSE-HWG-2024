"""
Example usage of the Excel to Claude API uploader using Files API
"""

import os
from excel_to_claude import ExcelToClaudeUploader, upload_excel_to_claude


def example_1_simple_usage():
    """Example 1: Simple usage with convenience function"""
    print("=" * 60)
    print("Example 1: Simple Usage")
    print("=" * 60)

    # Make sure to set your API key
    # os.environ["ANTHROPIC_API_KEY"] = "your-api-key-here"

    try:
        response = upload_excel_to_claude(
            file_path="your_file.xlsx",
            prompt="Please summarize the data in this Excel file and provide key insights."
        )
        print(response)
    except Exception as e:
        print(f"Error: {e}")


def example_2_class_based_with_file_id():
    """Example 2: Upload file once, reuse file_id for multiple queries"""
    print("\n" + "=" * 60)
    print("Example 2: Upload Once, Query Multiple Times")
    print("=" * 60)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    try:
        uploader = ExcelToClaudeUploader(api_key=api_key)

        # Step 1: Upload file and get file_id
        print("Uploading Excel file...")
        file_id = uploader.upload_file("your_file.xlsx")
        print(f"File uploaded successfully! File ID: {file_id}")

        # Step 2: Ask multiple questions using the same file_id
        questions = [
            "What are the column names in this spreadsheet?",
            "How many rows of data are there?",
            "What is the date range covered by this data?"
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n--- Question {i}: {question} ---")
            response = uploader.send_message_with_file(
                file_id=file_id,
                prompt=question,
                model="claude-sonnet-4-20250514",
                max_tokens=1024
            )
            print(f"Answer: {uploader.get_response_text(response)}")
            print(f"Tokens used: {response['usage']['input_tokens']} in, "
                  f"{response['usage']['output_tokens']} out")

    except Exception as e:
        print(f"Error: {e}")


def example_3_full_response_details():
    """Example 3: Get full response with all metadata"""
    print("\n" + "=" * 60)
    print("Example 3: Full Response Details")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    try:
        response = uploader.upload_excel_with_prompt(
            excel_file_path="your_file.xlsx",
            prompt="Analyze this spreadsheet and identify any trends or anomalies.",
            model="claude-sonnet-4-20250514",
            max_tokens=4096
        )

        # Access different parts of the response
        print(f"Model used: {response['model']}")
        print(f"File ID: {response['file_id']}")
        print(f"Input tokens: {response['usage']['input_tokens']}")
        print(f"Output tokens: {response['usage']['output_tokens']}")
        print(f"Stop reason: {response['stop_reason']}")
        print(f"\nResponse:\n{uploader.get_response_text(response)}")

    except Exception as e:
        print(f"Error: {e}")


def example_4_reuse_cached_file():
    """Example 4: Automatic file caching within same uploader instance"""
    print("\n" + "=" * 60)
    print("Example 4: Automatic File Caching")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    try:
        # First call: uploads the file
        print("First query (uploads file)...")
        response1 = uploader.upload_excel_with_prompt(
            excel_file_path="your_file.xlsx",
            prompt="What is the total number of records?"
        )
        file_id_1 = response1['file_id']
        print(f"File ID from first upload: {file_id_1}")
        print(f"Response: {uploader.get_response_text(response1)}")

        # Second call: reuses cached file_id
        print("\nSecond query (reuses cached file_id)...")
        response2 = uploader.upload_excel_with_prompt(
            excel_file_path="your_file.xlsx",  # Same file path
            prompt="What are the main categories in the data?"
        )
        file_id_2 = response2['file_id']
        print(f"File ID from second call: {file_id_2}")
        print(f"Same file ID? {file_id_1 == file_id_2}")  # Should be True
        print(f"Response: {uploader.get_response_text(response2)}")

    except Exception as e:
        print(f"Error: {e}")


def example_5_manual_file_id_reuse():
    """Example 5: Manually reuse a file_id"""
    print("\n" + "=" * 60)
    print("Example 5: Manual File ID Reuse")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    try:
        # Upload file and save the file_id
        file_id = uploader.upload_file("your_file.xlsx")
        print(f"Uploaded file. File ID: {file_id}")

        # Later, reuse the same file_id without re-uploading
        response = uploader.upload_excel_with_prompt(
            excel_file_path="your_file.xlsx",
            prompt="Summarize the key metrics in this data.",
            reuse_file_id=file_id  # Explicitly pass the file_id
        )

        print(f"Response: {uploader.get_response_text(response)}")

    except Exception as e:
        print(f"Error: {e}")


def example_6_multiple_files():
    """Example 6: Processing multiple different Excel files"""
    print("\n" + "=" * 60)
    print("Example 6: Multiple Files Processing")
    print("=" * 60)

    excel_files = [
        "sales_data.xlsx",
        "inventory.xlsx",
        "customers.xlsx"
    ]

    uploader = ExcelToClaudeUploader()

    try:
        # Upload all files first and collect file_ids
        file_ids = {}
        for file in excel_files:
            if os.path.exists(file):
                print(f"Uploading {file}...")
                file_id = uploader.upload_file(file)
                file_ids[file] = file_id
                print(f"  → File ID: {file_id}")
            else:
                print(f"File not found: {file}")

        # Now query each file
        for file, file_id in file_ids.items():
            print(f"\n--- Processing {file} ---")
            response = uploader.send_message_with_file(
                file_id=file_id,
                prompt="Provide a brief summary of this data including row count and key columns."
            )
            text_response = uploader.get_response_text(response)
            print(text_response)

    except Exception as e:
        print(f"Error: {e}")


def example_7_different_models():
    """Example 7: Using different Claude models with the same file"""
    print("\n" + "=" * 60)
    print("Example 7: Different Models Comparison")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    models = [
        "claude-sonnet-4-20250514",     # Latest Sonnet
        "claude-3-5-sonnet-20241022",   # Sonnet 3.5
    ]

    try:
        # Upload file once
        file_id = uploader.upload_file("your_file.xlsx")
        print(f"File uploaded: {file_id}\n")

        prompt = "Briefly describe what you see in this Excel file."

        # Try the same prompt with different models
        for model in models:
            print(f"--- Using {model} ---")
            response = uploader.send_message_with_file(
                file_id=file_id,
                prompt=prompt,
                model=model
            )
            print(f"Response: {uploader.get_response_text(response)}")
            print(f"Tokens: {response['usage']['input_tokens']} in, "
                  f"{response['usage']['output_tokens']} out\n")

    except Exception as e:
        print(f"Error: {e}")


def example_8_error_handling():
    """Example 8: Proper error handling"""
    print("\n" + "=" * 60)
    print("Example 8: Error Handling")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    # Test 1: Non-existent file
    try:
        uploader.upload_file("nonexistent.xlsx")
    except FileNotFoundError as e:
        print(f"✓ Caught expected error: {e}")

    # Test 2: Invalid file format
    try:
        uploader.upload_file("document.pdf")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")

    # Test 3: Missing API key
    try:
        bad_uploader = ExcelToClaudeUploader(api_key=None)
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")


if __name__ == "__main__":
    print("Excel to Claude API - Example Usage (Files API)\n")
    print("Note: Make sure to:")
    print("1. Set ANTHROPIC_API_KEY environment variable")
    print("2. Replace 'your_file.xlsx' with actual file paths")
    print("3. Uncomment the examples you want to run\n")

    # Uncomment the examples you want to run:
    # example_1_simple_usage()
    # example_2_class_based_with_file_id()
    # example_3_full_response_details()
    # example_4_reuse_cached_file()
    # example_5_manual_file_id_reuse()
    # example_6_multiple_files()
    # example_7_different_models()
    # example_8_error_handling()

    print("\nExamples are commented out. Uncomment the ones you want to run!")
