# import unittest
#
# from DataParser.StatementParser import BankMizrahiTefahotParser
#
#
# class TestExtractTextFromPDF(unittest.TestCase):
#         statement_parser = BankMizrahiTefahotParser(r'C:\Dev\FinView_13_01_24\FinView\Files\Input\BankMizrahiTefahot\AccountMovementsReport_17_02_2024.pdf')
#         file_path = r'C:\Dev\FinView_13_01_24\FinView\Files\Input\BankMizrahiTefahot\AccountMovementsReport_17_02_2024.pdf'
#     def test_valid_pdf(self):
#         file_path = 'valid_pdf.pdf'
#         expected_text = "Text extracted from the PDF"
#         with open(file_path, 'w') as f:
#             f.write(expected_text)
#
#         self.assertEqual(statement_parser.extract_text_from_pdf(file_path), expected_text)
#
#     def test_nonexistent_file(self):
#         file_path = 'nonexistent_file.pdf'
#         with self.assertRaises(FileNotFoundError):
#             statement_parser.extract_text_from_pdf(file_path)
#
#     def test_empty_pdf(self):
#         file_path = 'empty_pdf.pdf'
#         with open(file_path, 'w') as f:
#             f.write('')
#         self.assertEqual(statement_parser.extract_text_from_pdf(file_path), '')
#
#     def test_multiple_pages(self):
#         file_path = 'multiple_pages.pdf'
#         # Create a PDF with multiple pages
#         # You can use libraries like PyPDF2 or reportlab to create such PDFs for testing
#         # Here, for simplicity, let's assume a PDF with multiple pages is available
#         expected_text = "Text from page 1Text from page 2Text from page 3"
#         with open(file_path, 'w') as f:
#             f.write(expected_text)
#         self.assertEqual(statement_parser.extract_text_from_pdf(file_path), expected_text)
#
#
# if __name__ == '__main__':
#     unittest.main()
