import unittest
import sys
import os
import re
from datetime import date

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from model.message import message as mMessage

class TestType(unittest.TestCase):
    def test_message_property_types(self):
        msg = mMessage(
            name='Chien',
            role='user',
            action='question',
            content='test content'
        )
        
        # Check instance and property types
        self.assertIsInstance(msg.id, str)
        self.assertIsInstance(msg.timestamp, int)
        self.assertIsInstance(msg.name, str)
        self.assertIsInstance(msg.role, str)
        self.assertIsInstance(msg.action, str)
        self.assertIsInstance(msg.content, str)
        
        # Check UUID format
        uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        self.assertTrue(re.match(uuid_regex, msg.id))

if __name__ == '__main__':
    unittest.main()
