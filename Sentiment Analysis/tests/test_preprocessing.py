import pytest
from app.preprocessing import TextPreprocessor


class TestTextPreprocessor:
    """Comprehensive unit tests for TextPreprocessor class."""

    @pytest.fixture
    def preprocessor(self):
        """Fixture to provide a TextPreprocessor instance for each test."""
        return TextPreprocessor()

    def test_clean_text_removes_special_characters(self, preprocessor):
        """Test that special characters are removed from text."""
        text = "Hello, World! This is @amazing #test."
        result = preprocessor.clean_text(text)
        assert result == "hello world this is amazing test"

    def test_clean_text_converts_to_lowercase(self, preprocessor):
        """Test that text is converted to lowercase."""
        text = "UPPERCASE MixedCase lowercase"
        result = preprocessor.clean_text(text)
        assert result == "uppercase mixedcase lowercase"

    def test_clean_text_removes_numbers(self, preprocessor):
        """Test that numbers are removed from text."""
        text = "Test123 with 456 numbers"
        result = preprocessor.clean_text(text)
        assert result == "test with numbers"

    def test_clean_text_handles_multiple_spaces(self, preprocessor):
        """Test that multiple spaces are preserved internally but trimmed at edges."""
        text = "  multiple    spaces   here  "
        result = preprocessor.clean_text(text)
        assert result == "multiple    spaces   here"

    def test_clean_text_handles_empty_string(self, preprocessor):
        """Test that empty strings are handled correctly."""
        text = ""
        result = preprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_handles_only_special_characters(self, preprocessor):
        """Test that text with only special characters returns empty string."""
        text = "!@#$%^&*()123"
        result = preprocessor.clean_text(text)
        assert result == ""

    def test_tokenize_splits_on_whitespace(self, preprocessor):
        """Test that tokenize correctly splits text on whitespace."""
        text = "hello world test"
        result = preprocessor.tokenize(text)
        assert result == ["hello", "world", "test"]
        assert len(result) == 3

    def test_tokenize_handles_multiple_spaces(self, preprocessor):
        """Test tokenize behavior with multiple spaces."""
        text = "hello    world"
        result = preprocessor.tokenize(text)
        # split() removes empty strings from multiple spaces
        assert result == ["hello", "world"]

    def test_tokenize_handles_empty_string(self, preprocessor):
        """Test that tokenize returns empty list for empty string."""
        text = ""
        result = preprocessor.tokenize(text)
        assert result == []

    def test_tokenize_single_word(self, preprocessor):
        """Test that tokenize handles single word correctly."""
        text = "hello"
        result = preprocessor.tokenize(text)
        assert result == ["hello"]
        assert len(result) == 1

    @pytest.mark.parametrize("input_text,expected", [
        ("Hello, World!", "hello world"),
        ("123test456", "test"),
        ("  spaces  ", "spaces"),
        ("CAPS", "caps"),
        ("mix123ed!@#", "mixed"),
    ])
    def test_clean_text_parametrized(self, preprocessor, input_text, expected):
        """Parametrized test for various clean_text scenarios."""
        result = preprocessor.clean_text(input_text)
        assert result == expected

    def test_preprocessing_pipeline(self, preprocessor):
        """Test the full preprocessing pipeline: clean then tokenize."""
        raw_text = "Hello, World! This is a TEST with numbers123 and symbols@#$"
        cleaned = preprocessor.clean_text(raw_text)
        tokens = preprocessor.tokenize(cleaned)

        assert cleaned == "hello world this is a test with numbers and symbols"
        assert tokens == ["hello", "world", "this", "is", "a", "test", "with", "numbers", "and", "symbols"]
        assert len(tokens) == 10
