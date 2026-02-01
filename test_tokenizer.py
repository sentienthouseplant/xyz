import pytest
from Sentiment Analysis.app.preprocessing import TextPreprocessor


def test_tokenize():
    """Test the tokenize method of TextPreprocessor"""
    preprocessor = TextPreprocessor()

    # Test basic tokenization
    text = "hello world python"
    tokens = preprocessor.tokenize(text)
    assert tokens == ["hello", "world", "python"]

    # Test with extra whitespace
    text_with_spaces = "  hello   world  python  "
    tokens_spaces = preprocessor.tokenize(text_with_spaces)
    assert tokens_spaces == ["hello", "world", "python"]

    # Test empty string
    empty_tokens = preprocessor.tokenize("")
    assert empty_tokens == [""]

    # Test single word
    single_word = preprocessor.tokenize("python")
    assert single_word == ["python"]