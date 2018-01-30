# TDD with Django


Based on these works by Harry Percival:
- [video](https://www.youtube.com/watch?v=vQjmz9wCjLA)
- [docs](https://www.obeythetestinggoat.com/pages/book.html#toc)

This covers Part 1: The Basics of TDD and Django


#### Requirements:

- Python v3.6.4rc1
- Git
- FireFox (64 bit) (Firefox is a FAIL, using Chrome)
- Google Chrome v64.0.3282.119 (64 bit)
- Django v1.8 (pip install django==1.8)
- Selenium v3.8.1 (pip install selenium)
- GeckoDriver (brew install geckodriver) (For FF - FAIL)
- ChromeDriver (brew install chromedriver) (For Chrome - PASS)

_NOTE: Use of a Venv is up to you. I recommend it._


## Test Development Environment Setup

```
> python3
Python 3.6.4 (default, Jan  6 2018, 11:51:59)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> print(django.get_version())
1.8
>>> from selenium import webdriver
>>> browser = webdriver.Chrome()
>>> browser.get('http://www.google.com')
>>> print(browser.title)
Google
>>> quit()
```


## General Approach

- Write initial functional test to FAIL for detecting Django.
- Create new Django project and start servers.
- Move functional test into project folder root.
- Run functional test again and PASS (silently).
- Test and Develop iteratively.


## Walk-through of Initial Test and Project Setup.

1. Create file `functional_tests.py`
2. Edit file as follows:

    ```
    from selenium import webdriver

    # browser = webdriver.Firefox()     # Firefox throws selenium errors.
    browser = webdriver.Chrome()

    browser.get('http://localhost:8000')
    assert 'Django' in browser.title
    ```

3. Run test:

    ```
    > python functional_tests.py
    Traceback (most recent call last):
      File "functional_tests.py", line 7, in <module>
        assert 'Django' in browser.title
    AssertionError
    ```

4. Create new django project named `superlists`:

    ```
    > django-admin.py startproject superlists
    > tree
    .
    ├── TDD_Django.md
    ├── functional_tests.py
    └── superlists
        ├── manage.py
        └── superlists
            ├── __init__.py
            ├── settings.py
            ├── urls.py
            └── wsgi.py

    2 directories, 8 files
    ```

5. Move the `functional_tests.py` file into the project root:
    `> mv functional_tests.py superlists`

6. Navigate into the project root:
    '> cd superlists'

7. Run the functional_tests.py file again to verify still failing correctly:

    ```
    python functional_tests.py
    Traceback (most recent call last):
      File "functional_tests.py", line 7, in <module>
        assert 'Django' in browser.title
    AssertionError
    ```

8. Start the django project:
    `python manage.py runserver`

9. In a new terminal, run functional_tests.py again and PASS:

    ```
    > python functional_tests.py
    # Will open chrome with default django project page displaying.
    ```

10. Make intial commit of project:

    ```
    > git init .
    > touch .gitignore
    > vim .gitignore
    # Edit to include: __pycache__ , *.pyc and db.sqlite3
    > git add .
    > git commit -m "Initial commit of TDD Django project using Selenium."
    [master (root-commit) b3ce320] Initial commit of TDD Django project using Selenium.
     7 files changed, 149 insertions(+)
     create mode 100644 .gitignore
     create mode 100644 functional_tests.py
     create mode 100755 manage.py
     create mode 100644 superlists/__init__.py
     create mode 100644 superlists/settings.py
     create mode 100644 superlists/urls.py
     create mode 100644 superlists/wsgi.py
    > git status
    On branch master
    nothing to commit, working tree clean
    ```

    NOTE: This completes the initial red-gren refactor! YAY! Onward...


## Improving the TDD Workflow

- There is no logging of tests when they PASS
- The browser window remains open after tests complete.
- We want to test for something beyond just 'Django' in title.

Since many of these things are standard in testing, we will use a standard library to provide a test runner which will give us most of tese features out of the box.

Let's refactor our test script to properly use the `unittest` module for running the tests and providing setup, teardown and logging.

  ```
  # functional_tests.py

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
      # If you get too many warnings you can also use:
      #unittest.main(warnings='ignore')
  ```

Now run the refactored `functional_tests.py` script:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 16, in test_home_page
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'Welcome to Django'

----------------------------------------------------------------------
Ran 1 test in 1.757s

FAILED (failures=1)
```

A succesful FAIL! =)

Now let's enhance this to test the behavior of the site based on a User Story.


## Enhancing our Test with User Stories

A User Story captures requirements for how a user expects the application to behave based on user input or actions. Usually these are captured ina word document, but this can be then included into the functional test as comments to explicitly stipulate the behavior being tested for. Let's update our example test script to include a basic user story.

```
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
    unittest.main()
```

## A Brief Note on Failing

Sometimes you will not have time to complete writing your test and you will want to ensure you remember where you left off. You can simply insert this line of test code into your test script to ensure it fails there and remind you wehere you left off:

`self.fail('Finish writing the test!')`


## Adding Content and Testing

Time to write some actual Django code now in order to have a site to test. To begin lets make an app for the todo lists named `lists`:

  ```
  > python manage.py startapp lists
  > tree
  .
  ├── db.sqlite3
  ├── functional_tests.py
  ├── lists
  │   ├── __init__.py
  │   ├── admin.py
  │   ├── migrations
  │   │   └── __init__.py
  │   ├── models.py
  │   ├── tests.py
  │   └── views.py
  ├── manage.py
  └── superlists
      ├── __init__.py
      ├── __pycache__
      │   ├── __init__.cpython-36.pyc
      │   ├── settings.cpython-36.pyc
      │   ├── urls.cpython-36.pyc
      │   └── wsgi.cpython-36.pyc
      ├── settings.py
      ├── urls.py
      └── wsgi.py

  4 directories, 17 files
  ```

Pay close attention to the file created in the new app named `tests.py`. This is where we will keep our unit tests for the application.


## Functional Tests vs Unit Tests

**Functional tests** test the application from the perspective of the user (from the outside) and are intended to emulate real-world usage.

**Unit tests** test the application from the perspective of the programmer (from the inside) and are intended to evaluate functions and classes.

**Double-loop TDD** uses both functional and unit tests, which combines the two test types to validate the application both internally and externally.


## Webservers and Django (Briefly)

The webserver receives a `request` from the user's browser for a webpage (URL). The webserver passes the request to Django, which looks up the URL and finds the associated `view function` that processes the request and returns a `response` (usually in the form of html) which is then rendered in the user's browser.

In the testing context, we test these view functions by building an example fo a user request, passing it into the view function, and verifying we get the correct response back.


## Writing Our First Unit Test

Inside of our new `lists` application, edit the `tests.py` file to test for our lists app view.

```
from django.test import TestCase
from django.http import HttpRequest

# Import a reference to the views.
from lists.views import home_page

# Create your tests here.

class HomePageViewTest(Testcase):
    """Testing HomePageView"""

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # Verify content title contains `To-Do Lists`.
        self.assertIn('<title>To-Do Lists</title>', response.content)
```

We can run this test with the command: `python manage.py test lists`

NOTE: This test should FAIL (for now).


## The Unit Test Code Cycle

When writing application code, our workflow will be faster. It is basically an iterative sequence as follows:

- writing the test
- running the test
- writing the code required by the test
- running the test again
- reading the test errors for the new code
- editing the code until it passes the test
- continuing writing more tests, etc.


## Writing a Minimal View

If we run our test on the current list view, we will get this error:

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: lists.tests (unittest.loader._FailedTest)
----------------------------------------------------------------------
ImportError: Failed to import test module: lists.tests
Traceback (most recent call last):
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/lib/python3.6/unittest/loader.py", line 428, in _find_test_path
    module = self._get_module_from_name(name)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/lib/python3.6/unittest/loader.py", line 369, in _get_module_from_name
    __import__(name)
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 5, in <module>
    from lists.views import home_page
ImportError: cannot import name 'home_page'


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

This is telling us there is no view named home_page to import.
We can solve this error by creating the most minimal view function possible:

```
# lists/views.py

from django.shortcuts import render

# Create your views here.

home_page = None
```

If we run the test again, we will see a new error:

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 14, in test_home_page_retiurns_correct_html
    response = home_page(request)
TypeError: 'NoneType' object is not callable

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

Now we are finding the view function, but Django cannot call a function of None type. Progress!

This is the smallest example possible which ensures the test covers every aspect of the code.

Let's fix the next error by making the view function callable:

```
# lists/views.py

from django.shortcuts import render

# Create your views here.

def home_page():
    pass

```

This will in turn give us yet another error:

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 14, in test_home_page_retiurns_correct_html
    response = home_page(request)
TypeError: home_page() takes 0 positional arguments but 1 was given

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

Now the error is informing us that the view function was not expecting an argument but was passed one, so lets make the callable accept an argument:

```
# lists/views.py

from django.shortcuts import render

# Create your views here.

def home_page(request):
    pass
```

And (you guessed it) we get yet another error:

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 19, in test_home_page_returns_correct_html
    self.assertIn('<title>To-Do Lists</title>', response.content)
AttributeError: 'NoneType' object has no attribute 'content'

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

This error is telling us that our view function returned a None (from the pass) and NoneType has no content.

We can resolve this error by returning an HttpResponse from our view function as follows:

```
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return HttpResponse()
```

If we run the test now we will get this error:

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 19, in test_home_page_returns_correct_html
    self.assertIn('<title>To-Do Lists</title>', response.content)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/lib/python3.6/unittest/case.py", line 1086, in assertIn
    if member not in container:
TypeError: a bytes-like object is required, not 'str'

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

This error indicates that the content returned by the HttpResponse does not include the `<title>To-Do Lists</title>` value we expected in our test - which makes sense as it is currently an empty response.

Let's update our view function to return some actual content now:

```
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return HttpResponse('<html><title>To-Do Lists</title></html>')
```

And the subsequent error message form our test:

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 19, in test_home_page_returns_correct_html
    self.assertIn('<title>To-Do Lists</title>', response.content)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/lib/python3.6/unittest/case.py", line 1086, in assertIn
    if member not in container:
TypeError: a bytes-like object is required, not 'str'

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

**Wait a minute!**

We just returned the `<title>To-Do Lists</title>` string, why is this failing?

The answer has to do with encoding, bytes and strings.


#### A Quick Note on Bytes vs Strings

The response content sent back by Django is in the form of a string. However, content transmitted over the internet must be in the form of bytes. So what is the issue here?

The following is a conceptually useful distinction to make between strings and bytes:

- Strings are imaginary things that only exists inside of Python/Django but do not manifest in the real world.
- Bytes (1 and 0) are physical objects that can be read/written to disc and can be transmitted over the internet.

In order to manipulate the bytes that are transmitted to an application, it needs to be able to encode/decode them, to understand what the bytes are representing (in this case convert them into a string). In order to test, we need to compare like vs like therefore we must know how the bytes are encoded in order to do a proper test.

Let's update our test class to do an inline decode on the response as utf8 string data:

```
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

        # Verify content title contains `To-Do Lists`.
        self.assertIn('<title>To-Do Lists</title>', response.content.decode('utf8'))
```

Now if we run our test:

```
> python manage.py test lists
Creating test database for alias 'default'...
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
```

**HOORAY!** A passing unit test!

Alas, if we were to run the functional test now, it will fail because it is not yet calling the home_page view. Let's wire that up:

```
#superlists/urls.py

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
```

And now if we run our functional tests again:

```
> python functional_tests.py
.
----------------------------------------------------------------------
Ran 1 test in 1.706s

OK
```

**VICTORY!!!**

Now let's enhance our unit test for the list home_page view function. Rather than constantly do inline decoding on the byte data, lets decode the entire response and run tests against that instead. While we are at it. lets also check for the presence of opening an dclosing `<html></html>` tags.

```
# lists/tests.py

from django.test import TestCase
from django.http import HttpRequest

# Import a reference to the views.
from lists.views import home_page

# Create your tests here.

class HomePageViewTest(Testcase):
    """Testing HomePageView"""

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # Decode the byte data as utf-8.
        html = response.content.decode('utf8')

        # Verify content title contains `To-Do Lists`.
        self.assertIn('<title>To-Do Lists</title>', html)

        # Verify content starts with proper html tag.
        self.assertTrue(html.startswith('<html>'))

        # Verify content ends with proper html tag.
        self.assertTrue(html.endswith('</html>'))
```

If you rerun your unit test, it should still pass. Also, your functional tests should still be passing.

Also uncomment the line `self.fail('Finish writing the test!')` in `functional_tests.py` as a reminder of where we are. Don't forget to make a git commit to capture your work.

That is quite a bit for one sitting! Go take a coffee break, strech your legs, and we will dive back in for further testing fun.


## Why So Many Types of Tests?

At this point we have covered the general setup required to accomplish TDD in Django projects along with the basics of functional and unit tests. If we were to itemize:

- We discussed functional test
- We implemented a basic working functional tests
- We used the untitest framework
- We examined using setUp() and tearDown()
- We used the Django testrunner to run our unit tests
- We discussed functional vs unit tests

So why do we have all these types of tests?

Functional and unit tests almost seem to duplicate one another, but the idea is that the functional test is external behavior a user would experience - using a real web browser to interact with your application in the real world. It is more of an end-to-end test as it test the integration of your components (your webserver is running, it is responding on the correct URLs, it is returning the expected values, etc.).

Meanwhile the unit tests are there to test individual classes and functions - the building blocks of your application. Unit tests will help you to write cleaner code by forcing you to think about the code before you write it. This is design-lead thinking in a sense, forcing you think about how the function will be used before you use it (an outside in approach).

Together these tests validate that things do what you expect them to do.

#### The Goat and the Kata

TDD is a discipline, it does not come naturally. You have to learn and practice the process in order to become comfortable with it. Like a kata in a martial art, the idea is to learn the motions in a controlled context, when there is no adversity, so that the techiques are part of your muscle memory. It seems trivial now, because we’ve started with a very simple example. The problem comes when your application gets complex—​that’s when you really need your tests. And the danger is that complexity tends to sneak up on you, gradually. You may not notice it happening, but quite soon you’re a boiled frog.

Some of these examples have been absurdly rudimentary in order to be demonstrative, you would not do this in real practice (eg. `home_page = None`). However, if you were refactoring a payments engine that needs to start taking payments from paypal as wlll as credit cards and you have to refactor the entire system, you will be tearing it apart line by line and will want test coverage to ensure that your core business logic still behaves as expected. That is when TDD will be worth its weight in code.

**Obey the Testing Goat!**

Now let's dive into refactoring the test code.

## Refactoring and TDD

Refactoring, the process of changing the code without altering the inputs or outputs (behavioral change of how, but not changing what it does). You can not refactor without tests. Otherwise you are just tinkering about with your code until everything suddenly breaks (eg. Refactoring Cat - https://goo.gl/images/koRj8o).

So how do we use TDD to properly refactor our code?

Let's update our functional tests  to include some additional tests.

```
# functional_tests.py

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
        self.fail('Finish writing the test!')

if __name__ == '__main__':
    # unittest.main()
    unittest.main(warnings='ignore')
```

And run it....

```
> python functional_tests.py
E
======================================================================
ERROR: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 23, in test_home_page
    header = self.browser.find_element_by_tag_name('h1')
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 521, in find_element_by_tag_name
    return self.find_element(by=By.TAG_NAME, value=name)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 955, in find_element
    'value': value})['value']
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 312, in execute
    self.error_handler.check_response(response)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 237, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"tag name","selector":"h1"}
  (Session info: chrome=64.0.3282.119)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.13.3 x86_64)


----------------------------------------------------------------------
Ran 1 test in 1.774s

FAILED (errors=1)
```

We are now getting a 'no such element' error (as expected) for the missing h1 tag.

This works for small examples, but in reality we would not want to keep writing html strings and passing them back through the view function. Instead we want to return an actual html file from disk that contains proper html code in it (which will also render correctly i our IDE and allow us to use syntax highlighting, intellisense, linting, etc.).

So lets wire up a proper template file in our Django lists app. This is refactor!! We want the application to behave exactly the same as before, but we are changing the way it achieves those results internally (eg. - returning a template file, not an html string).

First re-run your unit tests to verify everything still passes (it should).

Now create a new folder under `superlists/lists` named `templates`. Inside of the new `templates` folder create a file named `home.html`.

NOTE: Django will pick up any folder named templates inside of an application (so long as` APP_DIRS :True` is set under the `settings.py` `TEMPLATES` configuration) and be able to fnd the template files residing therein.

Your project structure should now look like this:

```
> tree
.
├── db.sqlite3
├── functional_tests.py
├── lists
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── tests.cpython-36.pyc
│   │   └── views.cpython-36.pyc
│   ├── admin.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       └── __init__.cpython-36.pyc
│   ├── models.py
│   ├── templates
│   │   └── home.html
│   ├── tests.py
│   └── views.py
├── manage.py
└── superlists
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-36.pyc
    │   ├── settings.cpython-36.pyc
    │   ├── urls.cpython-36.pyc
    │   └── wsgi.cpython-36.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

7 directories, 22 files
```

Now edit the contents of `home.html` to match the current html string in the view function:

```
# lists/templates/home.html

<html>
<title>To-Do Lists</title>

</html>
```

In order to have the view return the template, update the view function as follows:

```
# lists/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return render(request, 'home.html')
```

All good now right? WRONG!

```
> python manage.py test lists
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 14, in test_home_page_returns_correct_html
    response = home_page(request)
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/views.py", line 8, in home_page
    return render(request, 'home.html')
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/django/shortcuts.py", line 67, in render
    template_name, context, request=request, using=using)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/django/template/loader.py", line 98, in render_to_string
    template = get_template(template_name, using=using)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/django/template/loader.py", line 46, in get_template
    raise TemplateDoesNotExist(template_name)
django.template.base.TemplateDoesNotExist: home.html

----------------------------------------------------------------------
Ran 1 test in 0.003s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

What is happening here? We know our template is where it should be and we know our view code is correct. However, the lists app has not been added to the `settings.py` `INSTALLED_APPS` configuration.

Let's edit our settings to match these:

```
# settings.py

...
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps.
    'lists',
)
...
```

If we rerun our unit tests, we will see that Django can now find the template, but there are still some errors:

```
python manage.py test lists
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 26, in test_home_page_returns_correct_html
    self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

This is what is called an _unexpected error_. We expected this to pass but the test is failing. Why is this?

According to the error the template file does not end in `</html>`. Let's add a print statement into our unit test to see what we are getting back from the view function.

```
# lists/tests.py

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

        print(response.content)

        # Verify content ends with proper html tag.
        self.assertTrue(html.endswith('</html>'))

```

When we run the test again we see that the output is logged as:

```
b'<html>\n<title>To-Do Lists</title>\n\n</html>\n'
```

*Aha!*

The trailing newline character is throwing the test off. Lets modify our test to strip off the newline characters at the end:

```
# lists/tests.py

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

        # print(response.content)

        # Verify content ends with proper html tag.
        self.assertTrue(html.strip().endswith('</html>'))
```

If we rerun our test it will now pass.

If you rerun the functional test it still blows up again at the same place (getting the h1 element).

We have completed our refactor and we are now using proper templates instead of html strings.

We can also refactor our tests. It is unlikely we would actually test a template for basic string content (though not impossible). This leads to a constant question in TDD - what should we test?

There are a few rules to adhere to, one of them being **don't test constants**. Rather than testing what your code is (implementation), test the behavior of the code.

So in our current unit tests, we are testing constants and implementation. Let's update that so instead of testing the specific bits of html the view function returns, we test that the view function returns the correct template.

```
# lists/tests.py

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

        print(response.content)

        # Verify content ends with proper html tag.
        self.assertTrue(html.strip().endswith('</html>'))

        # Read in the template file.
        expected_content = open('lists/templates/home.html').read()

        # Compare the template content with the response content.
        self.assertEqual(response.content, expected_content)
```

If we run our unit test again we get this error:

```
# python manage.py test lists
Creating test database for alias 'default'...
b'<html>\n<title>To-Do Lists</title>\n\n</html>\n'
F
======================================================================
FAIL: test_home_page_returns_correct_html (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 34, in test_home_page_returns_correct_html
    self.assertEqual(response.content, expected_content)
AssertionError: b'<html>\n<title>To-Do Lists</title>\n\n</html>\n' != '<html>\n<title>To-Do Lists</title>\n\n</html>\n'

----------------------------------------------------------------------
Ran 1 test in 0.003s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

This is telling us that bytes do not equal strings. We forgot to decode our template response as utf-8. Let's fix that:

```
# lists/tests.py

...
# Compare the template content with the response content.
self.assertEqual(response.content.decode('utf8'), expected_content)
```

And now it will pass. Let's also remove the previous example tests so our new unit tests code will look like this:

```
# lists/tests.py

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

        # Read in the template file.
        expected_content = open('home.html').read()

        # Compare the template content with the response content.
        self.assertEqual(response.content.decode('utf8'), expected_content)
```

We have now succesfully refactored out unit test!

Let's make one more refinement to how we are unit testing our templates and use the Django template loader module instead of opening the file directly.

```
# lists/tests.py

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
```

And once again we are passing out unit tests. BRILLIANT!

Now if we want to edit home.html we can, because this is a constant from the unit testing perspective. Let's edit our template further and prove that it still works fine.

```
# lists/templates/home.html

<html>
<head>
  <title>To-Do Lists</title>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
</body>
</html>
```

Our unit tests should still pass and now we should also be able to pass another of our fuctional tests (finding the h1 element).

Let's wrap up our functional tests now by editing our html file to include the inout element.

```
# lists/templates/home.html

<html>
<head>
  <title>To-Do Lists</title>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
  <input id="id_new_item" />
</body>
</html>
```

When you run the funcitonal test you will see it failing with the error:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 31, in test_home_page
    'Enter a to-do item'
AssertionError: '' != 'Enter a to-do item'
+ Enter a to-do item

----------------------------------------------------------------------
Ran 1 test in 1.812s

FAILED (failures=1)
```

Oops! No placeholder text! Let's fix that....

```
# lists/templates/home.html

<html>
<head>
  <title>To-Do Lists</title>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
  <input id="id_new_item" placeholder="Enter a to-do item" />
</body>
</html>
```

And if we run our functiyonal tests again we are finally back at our self imposed failure:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 52, in test_home_page
    self.fail('Finish writing the test!')
AssertionError: Finish writing the test!

----------------------------------------------------------------------
Ran 1 test in 1.869s

FAILED (failures=1)
```

This is as far as we can get without starting to include responses from servers, databases, etc. Our user can type input into the field (our test even passes) but we aren't doing anything with that yet.

Let's move onward...
