import unittest
import sys
sys.path.append("src/")
from unittest.mock import MagicMock, patch
from model_training import (
    extract_text,
    annotate_text
)

class TestModelTraining(unittest.TestCase):
    def test_extract_text_file_exists(self):
        # Test with a file that exists
        file_path = "tests/sample_text.txt"
        text = extract_text(file_path)
        self.assertTrue(isinstance(text, str))

    def test_extract_text_file_not_found(self):
        # Test with a file that doesn't exist
        file_path = "non_existent_file.txt"
        with self.assertRaises(FileNotFoundError):
            extract_text(file_path)

    def test_annotate_text(self):
        text = "John Doe has experience in software development and education from MIT."
        annotations = annotate_text(text)
        self.assertTrue(len(annotations) > 0)


if __name__ == "__main__":
    unittest.main()
