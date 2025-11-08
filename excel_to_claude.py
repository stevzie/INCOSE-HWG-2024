"""
Upload Excel files to Claude API using the Files API
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from anthropic import Anthropic


class ExcelToClaudeUploader:
    """
    A class to handle uploading Excel files to Claude API using the Files API
    """

    # Beta header for Files API
    FILES_API_BETA_HEADER = "files-api-2025-04-14"

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
        # Store uploaded file IDs for reuse
        self._file_cache: Dict[str, str] = {}

    def validate_excel_file(self, file_path: str) -> Path:
        """
        Validate that the file exists and is a supported Excel format

        Args:
            file_path: Path to the Excel file

        Returns:
            Path object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a supported Excel format
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check file extension
        extension = file_path.suffix.lower()
        supported_formats = {'.xlsx', '.xls', '.xlsm'}

        if extension not in supported_formats:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: {', '.join(supported_formats)}"
            )

        return file_path

    def upload_file(self, file_path: str) -> str:
        """
        Upload an Excel file to Claude's Files API and get a file_id

        Args:
            file_path: Path to the Excel file

        Returns:
            file_id string that can be used to reference the file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        # Validate the file
        validated_path = self.validate_excel_file(file_path)

        # Check if already uploaded (cache check)
        cache_key = str(validated_path.absolute())
        if cache_key in self._file_cache:
            return self._file_cache[cache_key]

        # Upload the file to Files API
        with open(validated_path, 'rb') as file:
            file_response = self.client.files.create(
                file=file,
                purpose="user_upload"
            )

        file_id = file_response.id

        # Cache the file_id
        self._file_cache[cache_key] = file_id

        return file_id

    def send_message_with_file(
        self,
        file_id: str,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Send a message to Claude with a file reference

        Args:
            file_id: The file ID returned from upload_file()
            prompt: The prompt/question to ask Claude about the Excel file
            model: Claude model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens for the response

        Returns:
            Dictionary containing the response from Claude API
        """
        # Create message with file reference
        message = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            betas=[self.FILES_API_BETA_HEADER],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "file",
                                "file_id": file_id
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
            "stop_reason": message.stop_reason,
            "file_id": file_id  # Include file_id for reference
        }

    def upload_excel_with_prompt(
        self,
        excel_file_path: str,
        prompt: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
        reuse_file_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload an Excel file and send it to Claude with a prompt (all-in-one method)

        Args:
            excel_file_path: Path to the Excel file
            prompt: The prompt/question to ask Claude about the Excel file
            model: Claude model to use (default: claude-sonnet-4-20250514)
            max_tokens: Maximum tokens for the response
            reuse_file_id: Optional file_id to reuse instead of uploading again

        Returns:
            Dictionary containing the response from Claude API
        """
        # Upload file if no file_id provided
        if reuse_file_id:
            file_id = reuse_file_id
        else:
            file_id = self.upload_file(excel_file_path)

        # Send message with the file
        return self.send_message_with_file(file_id, prompt, model, max_tokens)

    def get_response_text(self, response: Dict[str, Any]) -> str:
        """
        Extract text content from Claude API response

        Args:
            response: Response dictionary from upload_excel_with_prompt or send_message_with_file

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
