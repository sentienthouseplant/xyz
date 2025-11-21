import pytest
from hypothesis import given, strategies as st
from app.preprocessing import TextPreprocessor
import time


class TestTextPreprocessor:
    """Comprehensive unit tests for TextPreprocessor class."""

    @pytest.fixture
    def preprocessor(self):
        """Fixture to provide a TextPreprocessor instance for each test."""
        return TextPreprocessor()

    # ==================== BASIC FUNCTIONALITY TESTS ====================

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

    # ==================== UNICODE AND INTERNATIONALIZATION ====================

    def test_clean_text_removes_emojis(self, preprocessor):
        """Test that emojis are removed from text."""
        text = "Hello 👋 World 🌍 Amazing 🎉"
        result = preprocessor.clean_text(text)
        assert result == "hello world amazing"

    def test_clean_text_handles_accented_characters(self, preprocessor):
        """Test that accented characters are removed (as they're not a-zA-Z)."""
        text = "café résumé naïve"
        result = preprocessor.clean_text(text)
        # The regex [^a-zA-Z\s] removes accented characters
        assert result == "caf rsum nave"

    def test_clean_text_handles_mixed_unicode(self, preprocessor):
        """Test text with mixed unicode characters."""
        text = "Hello™ World® Test© Symbol±"
        result = preprocessor.clean_text(text)
        assert result == "hello world test symbol"

    def test_clean_text_handles_chinese_characters(self, preprocessor):
        """Test that non-Latin scripts are removed."""
        text = "Hello 你好 World 世界"
        result = preprocessor.clean_text(text)
        assert result == "hello world"

    def test_tokenize_with_unicode_whitespace(self, preprocessor):
        """Test tokenization with various unicode whitespace."""
        text = "hello\u00A0world\u2009test"  # Non-breaking space and thin space
        result = preprocessor.tokenize(text)
        # Python's split() handles unicode whitespace
        assert len(result) >= 1

    # ==================== EDGE CASES AND BOUNDARIES ====================

    def test_clean_text_single_character(self, preprocessor):
        """Test with single character input."""
        assert preprocessor.clean_text("a") == "a"
        assert preprocessor.clean_text("A") == "a"
        assert preprocessor.clean_text("1") == ""
        assert preprocessor.clean_text("!") == ""

    def test_clean_text_only_whitespace(self, preprocessor):
        """Test with only whitespace characters."""
        text = "     \t\n   "
        result = preprocessor.clean_text(text)
        assert result == ""

    def test_clean_text_newlines_and_tabs(self, preprocessor):
        """Test handling of newlines and tabs."""
        text = "Hello\nWorld\tTest"
        result = preprocessor.clean_text(text)
        # Newlines and tabs are not removed by regex, but will be in output
        assert "hello" in result
        assert "world" in result

    def test_clean_text_mixed_whitespace_types(self, preprocessor):
        """Test with mixed whitespace types."""
        text = "word1\tword2\nword3 word4"
        result = preprocessor.clean_text(text)
        tokens = result.split()
        assert len(tokens) == 4

    def test_tokenize_with_tabs(self, preprocessor):
        """Test tokenization with tab characters."""
        text = "hello\tworld\ttest"
        result = preprocessor.tokenize(text)
        assert result == ["hello", "world", "test"]

    def test_tokenize_with_newlines(self, preprocessor):
        """Test tokenization with newline characters."""
        text = "hello\nworld\ntest"
        result = preprocessor.tokenize(text)
        assert result == ["hello", "world", "test"]

    def test_tokenize_mixed_whitespace(self, preprocessor):
        """Test tokenization with mixed whitespace types."""
        text = "hello \t\n world  \n\t  test"
        result = preprocessor.tokenize(text)
        assert result == ["hello", "world", "test"]

    # ==================== PARAMETRIZED TESTS ====================

    @pytest.mark.parametrize("input_text,expected", [
        ("Hello, World!", "hello world"),
        ("123test456", "test"),
        ("  spaces  ", "spaces"),
        ("CAPS", "caps"),
        ("mix123ed!@#", "mixed"),
        ("email@example.com", "emailexamplecom"),
        ("price: $19.99", "price"),
        ("50% off!", "off"),
        ("one-two-three", "onetwothree"),
        ("under_score", "underscore"),
    ])
    def test_clean_text_parametrized(self, preprocessor, input_text, expected):
        """Parametrized test for various clean_text scenarios."""
        result = preprocessor.clean_text(input_text)
        assert result == expected

    @pytest.mark.parametrize("input_text,expected_tokens", [
        ("hello world", ["hello", "world"]),
        ("  hello  world  ", ["hello", "world"]),
        ("a b c", ["a", "b", "c"]),
        ("single", ["single"]),
        ("", []),
        ("  ", []),
        ("one\ttwo\nthree", ["one", "two", "three"]),
    ])
    def test_tokenize_parametrized(self, preprocessor, input_text, expected_tokens):
        """Parametrized test for various tokenization scenarios."""
        result = preprocessor.tokenize(input_text)
        assert result == expected_tokens

    @pytest.mark.parametrize("special_chars", [
        "!@#$%^&*()",
        "<>?/\\|[]{}",
        "~`+=_-",
        "©®™",
        "€£¥",
    ])
    def test_clean_text_removes_various_special_chars(self, preprocessor, special_chars):
        """Test removal of various categories of special characters."""
        text = f"test{special_chars}text"
        result = preprocessor.clean_text(text)
        assert result == "testtext"

    # ==================== REAL-WORLD SCENARIOS ====================

    def test_preprocessing_pipeline(self, preprocessor):
        """Test the full preprocessing pipeline: clean then tokenize."""
        raw_text = "Hello, World! This is a TEST with numbers123 and symbols@#$"
        cleaned = preprocessor.clean_text(raw_text)
        tokens = preprocessor.tokenize(cleaned)

        assert cleaned == "hello world this is a test with numbers and symbols"
        assert tokens == ["hello", "world", "this", "is", "a", "test", "with", "numbers", "and", "symbols"]
        assert len(tokens) == 10

    def test_yelp_review_style_text(self, preprocessor):
        """Test with Yelp review-style text (real-world use case)."""
        review = "This place is AMAZING!!! Best food I've had in years. 5/5 stars! ⭐⭐⭐⭐⭐"
        cleaned = preprocessor.clean_text(review)
        tokens = preprocessor.tokenize(cleaned)

        assert "amazing" in tokens
        assert "best" in tokens
        assert "food" in tokens
        # Numbers and special characters should be removed
        assert "5" not in cleaned
        assert "!!!" not in cleaned

    def test_social_media_style_text(self, preprocessor):
        """Test with social media style text with hashtags and mentions."""
        tweet = "Check out this #amazing product! @company makes the best stuff 😊"
        cleaned = preprocessor.clean_text(tweet)
        tokens = preprocessor.tokenize(cleaned)

        assert "amazing" in tokens
        assert "company" in tokens
        assert "#" not in cleaned
        assert "@" not in cleaned

    def test_product_review_with_prices(self, preprocessor):
        """Test with product review containing prices and measurements."""
        review = "Great value at $49.99! Weight: 2.5kg, Size: 10x15cm. Highly recommend!!!"
        cleaned = preprocessor.clean_text(review)
        tokens = preprocessor.tokenize(cleaned)

        assert "great" in tokens
        assert "value" in tokens
        # Numbers and currency should be removed
        assert "$" not in cleaned
        assert "49" not in cleaned

    # ==================== IMMUTABILITY TESTS ====================

    def test_clean_text_does_not_modify_original(self, preprocessor):
        """Test that clean_text doesn't modify the original string."""
        original = "Hello, World! 123"
        original_copy = original
        result = preprocessor.clean_text(original)

        # Python strings are immutable, so this should always pass
        # but it's good to verify the function doesn't attempt mutation
        assert original == original_copy
        assert original == "Hello, World! 123"

    def test_tokenize_does_not_modify_original(self, preprocessor):
        """Test that tokenize doesn't modify the original string."""
        original = "hello world test"
        original_copy = original
        result = preprocessor.tokenize(original)

        assert original == original_copy
        assert original == "hello world test"

    # ==================== PERFORMANCE AND STRESS TESTS ====================

    def test_clean_text_with_long_string(self, preprocessor):
        """Test performance with a long string."""
        # Create a 10KB string
        text = "Hello World! 123 " * 1000
        result = preprocessor.clean_text(text)

        # Should complete without error
        assert isinstance(result, str)
        assert len(result) > 0
        assert "hello world" in result

    def test_tokenize_with_many_tokens(self, preprocessor):
        """Test tokenization with many tokens."""
        # Create text with 10,000 words
        text = " ".join([f"word{i}" for i in range(10000)])
        result = preprocessor.tokenize(text)

        assert len(result) == 10000
        assert result[0] == "word0"
        assert result[-1] == "word9999"

    def test_repeated_cleaning_operations(self, preprocessor):
        """Test that repeated cleaning produces consistent results."""
        text = "Hello, World! 123"
        result1 = preprocessor.clean_text(text)
        result2 = preprocessor.clean_text(result1)
        result3 = preprocessor.clean_text(result2)

        # Cleaning cleaned text should produce the same result (idempotent)
        assert result1 == result2 == result3

    # ==================== PROPERTY-BASED TESTS (Hypothesis) ====================

    @given(st.text())
    def test_clean_text_always_returns_string(self, preprocessor, text):
        """Property: clean_text should always return a string."""
        result = preprocessor.clean_text(text)
        assert isinstance(result, str)

    @given(st.text())
    def test_clean_text_output_is_lowercase(self, preprocessor, text):
        """Property: clean_text output should always be lowercase."""
        result = preprocessor.clean_text(text)
        # Only check if result is not empty
        if result:
            assert result == result.lower()

    @given(st.text())
    def test_clean_text_no_special_characters_in_output(self, preprocessor, text):
        """Property: clean_text output should contain only letters and spaces."""
        result = preprocessor.clean_text(text)
        # Check that result only contains letters and spaces
        for char in result:
            assert char.isalpha() or char.isspace()

    @given(st.text())
    def test_tokenize_returns_list(self, preprocessor, text):
        """Property: tokenize should always return a list."""
        result = preprocessor.tokenize(text)
        assert isinstance(result, list)

    @given(st.text())
    def test_tokenize_no_empty_strings(self, preprocessor, text):
        """Property: tokenize should not produce empty strings in output."""
        result = preprocessor.tokenize(text)
        assert "" not in result

    @given(st.text(min_size=1))
    def test_preprocessing_pipeline_consistency(self, preprocessor, text):
        """Property: The preprocessing pipeline should be consistent."""
        cleaned = preprocessor.clean_text(text)
        tokens = preprocessor.tokenize(cleaned)

        # If cleaned text is not empty, tokens should not be empty
        if cleaned.strip():
            assert len(tokens) > 0

        # All tokens should be lowercase
        for token in tokens:
            assert token == token.lower()

    # ==================== TYPE AND ERROR HANDLING ====================

    def test_clean_text_with_none_raises_error(self, preprocessor):
        """Test that None input raises appropriate error."""
        with pytest.raises((TypeError, AttributeError)):
            preprocessor.clean_text(None)

    def test_tokenize_with_none_raises_error(self, preprocessor):
        """Test that None input raises appropriate error."""
        with pytest.raises((TypeError, AttributeError)):
            preprocessor.tokenize(None)

    def test_clean_text_with_numeric_type(self, preprocessor):
        """Test behavior with numeric input."""
        with pytest.raises((TypeError, AttributeError)):
            preprocessor.clean_text(12345)

    def test_tokenize_with_numeric_type(self, preprocessor):
        """Test behavior with numeric input."""
        with pytest.raises((TypeError, AttributeError)):
            preprocessor.tokenize(12345)

    # ==================== ADDITIONAL EDGE CASES ====================

    def test_clean_text_with_leading_trailing_punctuation(self, preprocessor):
        """Test text with leading and trailing punctuation marks."""
        text = "...Hello World!!!"
        result = preprocessor.clean_text(text)
        assert result == "hello world"

    def test_clean_text_with_consecutive_punctuation(self, preprocessor):
        """Test handling of consecutive punctuation marks."""
        text = "Wait!!!??? Really!?!?!"
        result = preprocessor.clean_text(text)
        assert result == "wait really"

    def test_clean_text_removes_html_tags(self, preprocessor):
        """Test that HTML/XML-like tags are removed."""
        text = "<div>Hello</div> <span>World</span>"
        result = preprocessor.clean_text(text)
        assert result == "divhellodiv spanworldspan"

    def test_clean_text_with_urls(self, preprocessor):
        """Test handling of URL-like strings."""
        text = "Check out https://example.com for more info"
        result = preprocessor.clean_text(text)
        assert "https" not in result
        assert "://" not in result
        assert "check" in result
        assert "out" in result

    def test_clean_text_with_contractions(self, preprocessor):
        """Test handling of contractions with apostrophes."""
        text = "don't can't won't I'm you're"
        result = preprocessor.clean_text(text)
        # Apostrophes are removed as special characters
        assert result == "dont cant wont im youre"

    def test_tokenize_with_leading_trailing_spaces(self, preprocessor):
        """Test tokenization with extensive leading and trailing spaces."""
        text = "     hello world     "
        result = preprocessor.tokenize(text)
        assert result == ["hello", "world"]
        assert len(result) == 2
