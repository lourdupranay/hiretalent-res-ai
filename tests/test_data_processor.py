import unittest
import os
import data_processor

class TestDataProcessor(unittest.TestCase):
    def test_preprocess_text(self):
        text = "This is a sample text for testing data preprocessing."
        preprocessed_text = data_processor.preprocess_text(text)
        self.assertEqual(preprocessed_text, "sample text testing data preprocessing")

    def test_preprocess_pdf(self):
        # sample PDF file for testing
        pdf_path = "tests/resumes/3547447.pdf"
        preprocessed_text = data_processor.preprocess_pdf(pdf_path)
        self.assertIsInstance(preprocessed_text, str)

    def test_preprocess_docx(self):
        # sample DOCX file for testing
        docx_path = "tests/jobs/Infrastructure Engineer (Data Center)-R-303525.docx"
        preprocessed_text = data_processor.preprocess_docx(docx_path)
        self.assertIsInstance(preprocessed_text, str)

    def test_preprocess_file(self):
        # sample TXT file for testing
        txt_path = "tests/sample_text.txt"
        preprocessed_text = data_processor.preprocess_file(txt_path)
        with open(txt_path, 'r', encoding='utf-8') as file:
            original_text = file.read()
        self.assertEqual(preprocessed_text, data_processor.preprocess_text(original_text))

    def test_preprocess_resume_directory(self):
        input_directory = "tests/resumes"
        output_directory = "tests/preprocessed_resumes"
        # Clean the output directory before running the test
        if os.path.exists(output_directory):
            for filename in os.listdir(output_directory):
                file_path = os.path.join(output_directory, filename)
                os.remove(file_path)
        data_processor.preprocess_resume_directory(input_directory, output_directory)
        # Check if files are created in the output directory
        self.assertTrue(os.path.exists(output_directory))
        # Check if each file in the output directory has been preprocessed
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                preprocessed_text = file.read()
            self.assertEqual(preprocessed_text, data_processor.preprocess_file(os.path.join(input_directory, filename)))

if __name__ == "__main__":
    unittest.main()
