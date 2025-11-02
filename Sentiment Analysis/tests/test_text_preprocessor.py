import pytest
from app.preprocessing import TextPreprocessor


class TestTextPreprocessor:
    """
    Comprehensive unit tests for the TextPreprocessor class.
    Tests various edge cases and scenarios for text cleaning functionality.
    """

    def test_clean_text_removes_special_characters(self):
        """Test that special characters are properly removed."""
        preprocessor = TextPreprocessor()
        text = "Hello, World! @#$%^&*()"
        result = preprocessor.clean_text(text)
        assert result == "hello world"

    def test_clean_text_removes_numbers(self):
        """Test that numbers are removed from text."""
        preprocessor = TextPreprocessor()
        text = "Product123 is 100% great"
        result = preprocessor.clean_text(text)
        assert result == "product is great"

    def test_clean_text_converts_to_lowercase(self):
        """Test that text is converted to lowercase."""
        preprocessor = TextPreprocessor()
        text = "HELLO WORLD"
        result = preprocessor.clean_text(text)
        assert result == "hello world"

    def test_clean_text_strips_whitespace(self):
        """Test that leading and trailing whitespace is stripped."""
        preprocessor = TextPreprocessor()
        text = "   hello world   "
        result = preprocessor.clean_text(text)
        assert result == "hello world"

    def test_clean_text_handles_empty_string(self):
        """Test that empty strings are handled correctly."""
        preprocessor = TextPreprocessor()
        text = ""
        result = preprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_handles_only_special_characters(self):
        """Test text with only special characters results in empty string."""
        preprocessor = TextPreprocessor()
        text = "@#$%^&*()"
        result = preprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_preserves_spaces_between_words(self):
        """Test that spaces between words are preserved."""
        preprocessor = TextPreprocessor()
        text = "this is a test"
        result = preprocessor.clean_text(text)
        assert result == "this is a test"

    def test_clean_text_handles_multiple_spaces(self):
        """Test that multiple spaces are preserved (not normalized)."""
        preprocessor = TextPreprocessor()
        text = "hello     world"
        result = preprocessor.clean_text(text)
        # Note: The implementation preserves internal spaces
        assert result == "hello     world"

    def test_clean_text_mixed_content(self):
        """Test realistic mixed content with letters, numbers, and symbols."""
        preprocessor = TextPreprocessor()
        text = "Great product! Rated 5/5 stars ⭐⭐⭐"
        result = preprocessor.clean_text(text)
        assert result == "great product rated stars"

    def test_tokenize_splits_text_correctly(self):
        """Test that tokenize method splits text into words."""
        preprocessor = TextPreprocessor()
        text = "hello world test"
        result = preprocessor.tokenize(text)
        assert result == ["hello", "world", "test"]

    def test_tokenize_empty_string(self):
        """Test tokenize with empty string."""
        preprocessor = TextPreprocessor()
        text = ""
        result = preprocessor.tokenize(text)
        assert result == [""]

    def test_clean_and_tokenize_pipeline(self):
        """Test using clean_text and tokenize together."""
        preprocessor = TextPreprocessor()
        text = "Hello, World! 123"
        cleaned = preprocessor.clean_text(text)
        tokens = preprocessor.tokenize(cleaned)
        assert tokens == ["hello", "world"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
