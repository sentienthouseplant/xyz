import re
from typing import Text

class TextPreprocessor:
    @staticmethod
    def clean_text(text: Text) -> Text:
        # Remove special characters and lowercase
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text.lower().strip()

    @staticmethod
    def tokenize(text: Text) -> list:
        return text.split()
