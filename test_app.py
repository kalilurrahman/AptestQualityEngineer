import unittest
from app import create_app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quality Engineering Artifact Generator', response.data)

    def test_repository_list(self):
        response = self.client.get('/repository')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Case Repository', response.data)
        # Check if one of the items is present
        self.assertIn(b'Netflix Testing', response.data)

    def test_repository_detail(self):
        # Assuming netflix is in the data
        response = self.client.get('/repository/netflix')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Netflix Test Strategy', response.data)
        # Check if markdown was converted to HTML (e.g. <table> tag)
        self.assertIn(b'<table', response.data)

    def test_generate_route(self):
        with unittest.mock.patch('app.routes.generate_artifacts') as mock_generate:
            mock_generate.return_value = "# Generated Artifacts\n\n| Case | Result |\n|---|---|\n| 1 | Pass |"

            data = {
                'api_key': 'test_key',
                'context_type': 'text',
                'context_text': 'Test context'
            }
            response = self.client.post('/generate', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Generated Artifacts', response.data)
            self.assertIn(b'<table', response.data)

if __name__ == '__main__':
    import unittest.mock
    unittest.main()
