import unittest
from selenium import webdriver

class HomePageTest(unittest.TestCase):
    """Testing Home Page"""

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get('http://localhost:8000')
        # Test for default Django landing pge.
        self.assertIn('To-Do', self.browser.title)


if __name__ == '__main__':
    unittest.main()
