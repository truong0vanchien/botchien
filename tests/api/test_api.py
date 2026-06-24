import unittest
import sys
import os
from unittest.mock import patch

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_home_accessible(self):
        # Accessing home page should work directly
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Truong Van Chien'.encode('utf-8'), response.data)

    @patch('database.supabase_db.getSubjectData')
    def test_get_chien_data_authenticated(self, mock_get_subject_data):
        # Mock database response
        mock_get_subject_data.return_value = {
            'definition': 'Test definition content',
            'training': 'Test training content'
        }

        # Fetch data
        response = self.client.get('/api/chien/data?subject=Detect PII')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'definition': 'Test definition content',
            'training': 'Test training content'
        })

    @patch('database.supabase_db.updateRecord')
    def test_update_chien_data_authenticated(self, mock_update_record):
        # Mock update success
        mock_update_record.return_value = True

        # Update data
        response = self.client.post('/api/chien/update', json={
            'subject': 'Detect PII',
            'action': 'definition',
            'content': 'New test content'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Success'})

if __name__ == '__main__':
    unittest.main()
