import pytest
from Sentiment_Analysis.app.preprocessing import TextPreprocessor


def test_tokenize():
    """Test that tokenize method properly splits text into words."""
    preprocessor = TextPreprocessor()

    # Test basic tokenization
    text = "hello world python"
    tokens = preprocessor.tokenize(text)
    assert tokens == ["hello", "world", "python"]

    # Test with extra spaces
    text_with_spaces = "  hello   world  python  "
    tokens_spaces = preprocessor.tokenize(text_with_spaces)
    expected = ["hello", "world", "python"]
    assert tokens_spaces == expected

    # Test empty string
    empty_text = ""
    empty_tokens = preprocessor.tokenize(empty_text)
    assert empty_tokens == []

    # Test single word
    single_word = "python"
    single_tokens = preprocessor.tokenize(single_word)
    assert single_tokens == ["python"]