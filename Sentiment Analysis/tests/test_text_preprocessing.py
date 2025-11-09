import pytest
from app.preprocessing import TextPreprocessor


class TestTextPreprocessorCleanText:
    """Unit tests for TextPreprocessor.clean_text() method."""

    def test_clean_text_removes_punctuation(self):
        """Test that punctuation marks are removed from text."""
        text = "Hello! How are you?"
        result = TextPreprocessor.clean_text(text)
        assert result == "hello how are you"

    def test_clean_text_removes_numbers(self):
        """Test that numeric characters are removed from text."""
        text = "I have 123 apples and 456 oranges"
        result = TextPreprocessor.clean_text(text)
        assert result == "i have apples and oranges"

    def test_clean_text_removes_special_characters(self):
        """Test that special characters are removed from text."""
        text = "Hello@#$%World&*()"
        result = TextPreprocessor.clean_text(text)
        assert result == "helloworld"

    def test_clean_text_converts_to_lowercase(self):
        """Test that mixed case text is converted to lowercase."""
        text = "HeLLo WoRLd"
        result = TextPreprocessor.clean_text(text)
        assert result == "hello world"

    def test_clean_text_strips_whitespace(self):
        """Test that leading and trailing whitespace is removed."""
        text = "   hello world   "
        result = TextPreprocessor.clean_text(text)
        assert result == "hello world"

    def test_clean_text_normalizes_multiple_spaces(self):
        """Test that multiple consecutive spaces are preserved but outer spaces trimmed."""
        text = "hello     world"
        result = TextPreprocessor.clean_text(text)
        assert result == "hello     world"

    def test_clean_text_empty_string(self):
        """Test that empty string returns empty string."""
        text = ""
        result = TextPreprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_whitespace_only(self):
        """Test that whitespace-only string returns empty string."""
        text = "    "
        result = TextPreprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_special_chars_only(self):
        """Test that string with only special characters returns empty string."""
        text = "!@#$%^&*()"
        result = TextPreprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_complex_sentence(self):
        """Test cleaning a complex sentence with mixed content."""
        text = "   The product costs $99.99 and it's AMAZING!!!   "
        result = TextPreprocessor.clean_text(text)
        assert result == "the product costs and its amazing"
