"""
Upload Excel files to Claude API (Sonnet) in base64 format
"""

import base64
import os
from pathlib import Path
from typing import Optional
from anthropic import Anthropic


class ExcelToClaudeUploader:
    """
    A class to handle uploading Excel files to Claude API in base64 format
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the uploader with Claude API credentials

        Args:
            api_key: Anthropic API key. If not provided, will look for ANTHROPIC_API_KEY env variable
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not provided. Either pass it directly or set ANTHROPIC_API_KEY environment variable"
            )

        self.client = Anthropic(api_key=self.api_key)

    def encode_excel_to_base64(self, file_path: str) -> tuple[str, str]:
        """
        Read and encode an Excel file to base64

        Args:
            file_path: Path to the Excel file

        Returns:
            Tuple of (base64_encoded_data, media_type)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a supported Excel format
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine media type based on extension
        extension = file_path.suffix.lower()
        media_type_map = {
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.xlsm': 'application/vnd.ms-excel.sheet.macroEnabled.12'
        }

        if extension not in media_type_map:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: {', '.join(media_type_map.keys())}"
            )

        media_type = media_type_map[extension]

        # Read and encode the file
        with open(file_path, 'rb') as file:
            file_data = file.read()
            base64_encoded = base64.standard_b64encode(file_data).decode('utf-8')

        return base64_encoded, media_type

    def upload_excel_with_prompt(
        self,
        excel_file_path: str,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096
    ) -> dict:
        """
        Upload an Excel file to Claude API with a prompt

        Args:
            excel_file_path: Path to the Excel file
            prompt: The prompt/question to ask Claude about the Excel file
            model: Claude model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens for the response

        Returns:
            Dictionary containing the response from Claude API
        """
        # Encode the Excel file
        base64_data, media_type = self.encode_excel_to_base64(excel_file_path)

        # Create the message with document content
        message = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_data
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        return {
            "model": message.model,
            "role": message.role,
            "content": message.content,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            },
            "stop_reason": message.stop_reason
        }

    def get_response_text(self, response: dict) -> str:
        """
        Extract text content from Claude API response

        Args:
            response: Response dictionary from upload_excel_with_prompt

        Returns:
            Extracted text content
        """
        content = response.get("content", [])
        if content and len(content) > 0:
            return content[0].text
        return ""


def upload_excel_to_claude(
    file_path: str,
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-20250514"
) -> str:
    """
    Convenience function to upload Excel file and get Claude's response

    Args:
        file_path: Path to Excel file
        prompt: Question/prompt about the file
        api_key: Anthropic API key (optional, will use env variable if not provided)
        model: Claude model to use

    Returns:
        Claude's text response

    Example:
        >>> response = upload_excel_to_claude(
        ...     "data.xlsx",
        ...     "Summarize the data in this spreadsheet"
        ... )
        >>> print(response)
    """
    uploader = ExcelToClaudeUploader(api_key=api_key)
    response = uploader.upload_excel_with_prompt(file_path, prompt, model)
    return uploader.get_response_text(response)


if __name__ == "__main__":
    import sys

    # Simple CLI usage
    if len(sys.argv) < 3:
        print("Usage: python excel_to_claude.py <excel_file_path> <prompt>")
        print("\nExample:")
        print('  python excel_to_claude.py data.xlsx "Summarize this data"')
        print("\nMake sure to set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    excel_file = sys.argv[1]
    prompt = sys.argv[2]

    try:
        response = upload_excel_to_claude(excel_file, prompt)
        print("\n=== Claude's Response ===")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
