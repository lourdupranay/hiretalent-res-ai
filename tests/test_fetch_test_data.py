import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from fetch_test_data import (
    extract_bucketname_from_path
)

class TestExtractBucketnameFromPath(unittest.TestCase):
    def test_extract_bucketname_from_path_valid(self):
        # Test with a valid path
        path = "https://console.cloud.google.com/storage/browser/hackathon1415"
        bucket_name = extract_bucketname_from_path(path)
        self.assertEqual(bucket_name, "hackathon1415")

    def test_extract_bucketname_from_path_invalid(self):
        # Test with an invalid path
        path = "https://invalid-path"
        bucket_name = extract_bucketname_from_path(path)
        self.assertIsNone(bucket_name)

if __name__ == "__main__":
    unittest.main()
