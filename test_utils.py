from app.utils import extract_text_from_url, extract_text_from_file
import io
import unittest
from werkzeug.datastructures import FileStorage

class TestUtils(unittest.TestCase):
    def test_extract_text_from_file_txt(self):
        file = FileStorage(stream=io.BytesIO(b"Hello world"), filename="test.txt")
        text = extract_text_from_file(file)
        self.assertEqual(text, "Hello world")

if __name__ == '__main__':
    unittest.main()
