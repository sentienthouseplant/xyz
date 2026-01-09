import pytest
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.preprocessing import TextPreprocessor


class TestTextPreprocessor:
    """Test suite for TextPreprocessor class."""

    def test_clean_text_removes_special_characters_and_lowercases(self):
        """Test that clean_text removes special characters and converts to lowercase."""
        # Arrange
        preprocessor = TextPreprocessor()
        input_text = "Hello, World! This is a TEST 123."
        expected_output = "hello world this is a test"

        # Act
        result = preprocessor.clean_text(input_text)

        # Assert
        assert result == expected_output
        assert result.islower()
        assert not any(char.isdigit() for char in result)
        assert not any(char in "!,." for char in result)
