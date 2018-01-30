import unittest
from selenium import webdriver

class HomePageTest(unittest.TestCase):
    """Testing Home Page"""

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        # The user opens their browser to the superlists URL.
        self.browser.get('http://localhost:8000')

        # The user should see 'To-Do' in the page title and header.
        self.assertIn('To-Do', self.browser.title)

        # Intentionally failing the test.
        # self.fail('Finish writing the test!')

        # The user is invited to enter an item into the todo list.
        # TestCase

        # The user types in their todo, presses enter, and the site refreshes.
        # The user should now see their todo in the list.
        # TestCase

        # The user clicks on the 'add another' option and enters another todo.
        # The user refreshes the page and should now see their new todo in the list.
        # TestCase

        # Etc.


if __name__ == '__main__':
    # unittest.main()
    unittest.main(warnings='ignore')
