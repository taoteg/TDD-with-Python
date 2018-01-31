from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# Import a reference to the views.
from lists.views import home_page

# Create your tests here.

class HomePageViewTest(TestCase):
    """Testing HomePageView"""

    def test_home_page_uses_home_template(self):
        request = HttpRequest()
        response = home_page(request)

        # Read in the template file.
        expected_content = render_to_string('home.html')

        # Compare the template content with the response content.
        self.assertEqual(
            response.content.decode('utf8'),
            expected_content
        )

    def test_home_page_can_store_post_requests(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'new item'
        response = home_page(request)

        expected_content = render_to_string(
            'home.html',
            {'new_item_text': 'new item'}
        )

        # self.assertIn(
        #     '<td>new item</td>',
        #     response.content.decode('utf8')
        # )

        self.assertEqual(
            response.content.decode('utf8'),
            expected_content
        )
