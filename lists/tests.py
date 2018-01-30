from django.test import TestCase
from django.http import HttpRequest

# Import a reference to the views.
from lists.views import home_page

# Create your tests here.

class HomePageViewTest(TestCase):
    """Testing HomePageView"""

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # Decode the byte data as utf-8.
        html = response.content.decode('utf8')

        # Verify content starts with proper html tag.
        self.assertTrue(html.startswith('<html>'))

        # Verify content title contains `To-Do Lists`.
        self.assertIn('<title>To-Do Lists</title>', html)

        # Verify content ends with proper html tag.
        self.assertTrue(html.endswith('</html>'))
