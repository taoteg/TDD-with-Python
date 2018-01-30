from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# Import a reference to the views.
from lists.views import home_page

# Create your tests here.

class HomePageViewTest(TestCase):
    """Testing HomePageView"""

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # Read in the template file.
        expected_content = render_to_string('home.html')

        # Compare the template content with the response content.
        self.assertEqual(response.content.decode('utf8'), expected_content)