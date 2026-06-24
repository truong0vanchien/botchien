import unittest
import sys
import os

# Add root folder to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from library import handler as hdl

class TestFunc(unittest.TestCase):
    def test_get_table_name(self):
        self.assertEqual(hdl.getTableName('Cody'), 'cnxCody')
        self.assertEqual(hdl.getTableName('test'), 'cnxtest')

    def test_get_bot_role(self):
        self.assertEqual(hdl.getBotRole('Cody'), 'You are a code analyst, your name is Cody.')
        self.assertEqual(hdl.getBotRole('Chien'), 'You are a code analyst, your name is Chien.')
        self.assertEqual(hdl.getBotRole('Asky'), 'You are a code analyst, your name is Asky.')
        self.assertEqual(hdl.getBotRole('Tasky'), '')

    def test_convert_message(self):
        records = [
            {'role': 'system', 'content': 'Hello system'},
            {'role': 'user', 'content': 'Hello user'}
        ]
        expected = [
            {'role': 'system', 'content': 'Hello system'},
            {'role': 'user', 'content': 'Hello user'}
        ]
        self.assertEqual(hdl.convertMessage(records), expected)

    def test_convert_valid_json_already_valid(self):
        valid_json = '{"key": "value"}'
        self.assertEqual(hdl.convertValidJson(valid_json), valid_json)

    def test_convert_valid_json_with_markdown(self):
        md_json = "```json\n{\"key\": \"value\"}\n```"
        self.assertEqual(hdl.convertValidJson(md_json), '{"key": "value"}')

        md_raw_json = "```\n{\"key\": \"value\"}\n```"
        self.assertEqual(hdl.convertValidJson(md_raw_json), '{"key": "value"}')

if __name__ == '__main__':
    unittest.main()
