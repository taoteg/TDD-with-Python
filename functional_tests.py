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

        # Find elements by tag name.
        # Selenium has a find_element AND a find_elements.
        # The former will fail if no match, the latter willl return an empty list.
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header.text)

        # Find and interact with an element by ID.
        inputbox = self.browser.find_element_by_id('id_new_item')
        # The user should see placeholder text in the input field.
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Test using the input field.
        # Note: this simulates a user typing into the field, so client-soide JS will react as it would in production.
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys('\n')

        # The user is invited to enter an item into the todo list.
        # TestCase

        # The user types in their todo, presses enter, and the site refreshes.
        # The user should now see their todo in the list.
        # TestCase

        # The user clicks on the 'add another' option and enters another todo.
        # The user refreshes the page and should now see their new todo in the list.
        # TestCase

        # Etc.

        # Intentionally failing the test.
        self.fail('Finish writing the test! Resume video at 1:55:00')

if __name__ == '__main__':
    # unittest.main()
    unittest.main(warnings='ignore')
