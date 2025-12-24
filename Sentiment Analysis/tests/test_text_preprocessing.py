import pytest
from app.preprocessing import TextPreprocessor


class TestTextPreprocessorCleanText:
    """Comprehensive unit tests for TextPreprocessor.clean_text() method."""

    def test_clean_text_with_special_characters_and_punctuation(self):
        """Test that special characters and punctuation are removed correctly."""
        text = "Hello, World!!! How are you? #amazing @user"
        expected = "hello world how are you amazing user"
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_with_numbers(self):
        """Test that numbers are removed from text."""
        text = "I have 123 apples and 456 oranges"
        expected = "i have apples and oranges"
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_with_empty_string(self):
        """Test that empty string returns empty string."""
        text = ""
        expected = ""
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_with_only_special_characters(self):
        """Test that string with only special characters returns empty string."""
        text = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        expected = ""
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_with_multiple_spaces(self):
        """Test that multiple spaces are handled correctly."""
        text = "Hello     World    with    spaces"
        expected = "hello world with spaces"
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_lowercase_conversion(self):
        """Test that uppercase letters are converted to lowercase."""
        text = "HELLO WORLD THIS IS UPPERCASE"
        expected = "hello world this is uppercase"
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_mixed_case_with_punctuation(self):
        """Test mixed case text with punctuation."""
        text = "ThIs Is MiXeD CaSe!!! With...Punctuation???"
        expected = "this is mixed case withpunctuation"
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_whitespace_stripping(self):
        """Test that leading and trailing whitespace is stripped."""
        text = "   Hello World   "
        expected = "hello world"
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_with_only_whitespace(self):
        """Test that string with only whitespace returns empty string."""
        text = "     "
        expected = ""
        result = TextPreprocessor.clean_text(text)
        assert result == expected

    def test_clean_text_with_newlines_and_tabs(self):
        """Test that newlines and tabs are handled as whitespace."""
        text = "Hello\nWorld\tPython"
        expected = "hello world python"
        result = TextPreprocessor.clean_text(text)
        assert result == expected
