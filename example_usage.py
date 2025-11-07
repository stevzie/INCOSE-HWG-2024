"""
Example usage of the Excel to Claude API uploader
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


def example_2_class_based():
    """Example 2: Using the class for more control"""
    print("\n" + "=" * 60)
    print("Example 2: Class-Based Usage")
    print("=" * 60)

    # Initialize with API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    try:
        # Create uploader instance
        uploader = ExcelToClaudeUploader(api_key=api_key)

        # Upload and get full response
        response = uploader.upload_excel_with_prompt(
            excel_file_path="your_file.xlsx",
            prompt="Analyze this spreadsheet and identify any trends or anomalies.",
            model="claude-sonnet-4-20250514",
            max_tokens=4096
        )

        # Access different parts of the response
        print(f"Model used: {response['model']}")
        print(f"Input tokens: {response['usage']['input_tokens']}")
        print(f"Output tokens: {response['usage']['output_tokens']}")
        print(f"\nResponse:\n{uploader.get_response_text(response)}")

    except Exception as e:
        print(f"Error: {e}")


def example_3_data_analysis():
    """Example 3: Specific data analysis tasks"""
    print("\n" + "=" * 60)
    print("Example 3: Data Analysis Tasks")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    analysis_prompts = [
        "What are the column names and data types in this spreadsheet?",
        "Calculate the sum, average, and standard deviation for all numeric columns.",
        "Identify any missing or null values in the data.",
        "Are there any duplicate rows in this dataset?",
        "Create a summary report of this data in markdown format."
    ]

    try:
        for i, prompt in enumerate(analysis_prompts, 1):
            print(f"\n--- Analysis Task {i} ---")
            print(f"Prompt: {prompt}")
            response = upload_excel_to_claude("your_file.xlsx", prompt)
            print(f"Response:\n{response}\n")
    except Exception as e:
        print(f"Error: {e}")


def example_4_multiple_files():
    """Example 4: Processing multiple Excel files"""
    print("\n" + "=" * 60)
    print("Example 4: Multiple Files Processing")
    print("=" * 60)

    excel_files = [
        "sales_data.xlsx",
        "inventory.xlsx",
        "customers.xlsx"
    ]

    uploader = ExcelToClaudeUploader()

    try:
        for file in excel_files:
            if os.path.exists(file):
                print(f"\n--- Processing {file} ---")
                response = uploader.upload_excel_with_prompt(
                    excel_file_path=file,
                    prompt="Provide a brief summary of this data including row count and key columns."
                )
                text_response = uploader.get_response_text(response)
                print(text_response)
            else:
                print(f"File not found: {file}")
    except Exception as e:
        print(f"Error: {e}")


def example_5_base64_encoding_only():
    """Example 5: Just encode file to base64 without sending to API"""
    print("\n" + "=" * 60)
    print("Example 5: Base64 Encoding Only")
    print("=" * 60)

    uploader = ExcelToClaudeUploader()

    try:
        base64_data, media_type = uploader.encode_excel_to_base64("your_file.xlsx")
        print(f"Media Type: {media_type}")
        print(f"Base64 Length: {len(base64_data)} characters")
        print(f"First 100 chars: {base64_data[:100]}...")

        # You can now use this base64_data in your own API calls or store it
    except Exception as e:
        print(f"Error: {e}")


def example_6_different_models():
    """Example 6: Using different Claude models"""
    print("\n" + "=" * 60)
    print("Example 6: Different Models")
    print("=" * 60)

    models = [
        "claude-sonnet-4-20250514",  # Latest Sonnet
        "claude-3-5-sonnet-20241022",  # Sonnet 3.5
        "claude-opus-4-20250514"  # Opus (most capable)
    ]

    try:
        for model in models:
            print(f"\n--- Using {model} ---")
            response = upload_excel_to_claude(
                file_path="your_file.xlsx",
                prompt="Briefly describe what you see in this Excel file.",
                model=model
            )
            print(response)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Excel to Claude API - Example Usage\n")
    print("Note: Make sure to:")
    print("1. Set ANTHROPIC_API_KEY environment variable")
    print("2. Replace 'your_file.xlsx' with actual file paths")
    print("3. Uncomment the examples you want to run\n")

    # Uncomment the examples you want to run:
    # example_1_simple_usage()
    # example_2_class_based()
    # example_3_data_analysis()
    # example_4_multiple_files()
    # example_5_base64_encoding_only()
    # example_6_different_models()

    print("\nExamples are commented out. Uncomment the ones you want to run!")
