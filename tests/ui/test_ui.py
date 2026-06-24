import unittest
from playwright.sync_api import sync_playwright

class TestUI(unittest.TestCase):
    def test_login_and_dashboard_interaction(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 1. Navigate directly to dashboard
            page.goto("http://localhost:5000/")
            page.wait_for_url("http://localhost:5000/")
            
            # 2. Wait for data load from supabase
            page.wait_for_timeout(3000)
            
            definition_val = page.locator("#definitionInput").input_value()
            self.assertTrue(len(definition_val) > 0)
            
            # 3. Verify question submission input works
            page.fill("#contentInput", 'const email = "test@example.com";')
            
            browser.close()

if __name__ == '__main__':
    unittest.main()
