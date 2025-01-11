import unittest
from src.pdf_generator import generate_pdf  # Assuming this is the function to test

class TestPDFGenerator(unittest.TestCase):
    
    def test_pdf_generation(self):
        """Test if PDF is generated correctly."""
        pdf_file = generate_pdf()  # Call the function to generate PDF
        self.assertIsNotNone(pdf_file)  # Check if the PDF file is not None
        self.assertTrue(pdf_file.endswith('.pdf'))  # Check if the file has a .pdf extension

    def test_pdf_content(self):
        """Test if the generated PDF contains expected content."""
        pdf_file = generate_pdf()
        with open(pdf_file, 'rb') as file:
            content = file.read()
            self.assertIn(b'%PDF', content)  # Check if the content starts with PDF header
            # Add more assertions to check for specific game content if needed

if __name__ == '__main__':
    unittest.main()