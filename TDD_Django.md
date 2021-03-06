# TDD with Django


Based on these works by Harry Percival:
- [TDD PyCon 2015 video](https://www.youtube.com/watch?v=vQjmz9wCjLA)
- [Test Driven Development with Python (by Harry Percival)](https://www.obeythetestinggoat.com/pages/book.html#toc)

_NOTE: This tutorial covers Part 1: The Basics of TDD and Django (Chapters 1 - 5ish)_

Also see:
- [TDD by Example (by Kent Beck)](https://www.eecs.yorku.ca/course_archive/2003-04/W/3311/sectionM/case_studies/money/KentBeck_TDD_byexample.pdf)
- [Working Effectively with Legacy Code (by Michael Feathers)](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)

Other References:
- [Selenium Docs: API](http://www.seleniumhq.org/docs/03_webdriver.jsp#selenium-webdriver-api-commands-and-operations)
- [Python Docs: unittest](https://docs.python.org/3.6/library/unittest.html)


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

### Populating the Lists

The next test we want to run is verifying user input to the list table. We will need to get a reference to the table (by id), grab each row in the table, and inspect its content. Let's add the logic to our functional tests for this.

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
        # The user should now see their todo in the list:
        # "1: Buy peacock feathers"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        # NOTE: any (boolean func) + list comprehension generator expression.
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # The user clicks on the 'add another' option and enters another todo.
        # The user refreshes the page and should now see their new todo in the list.
        # TestCase

        # Etc.

        # Intentionally failing the test.
        self.fail('Finish writing the test! 1:55:00...')

if __name__ == '__main__':
    # unittest.main()
    unittest.main(warnings='ignore')
```

If we run our functional tests now, we will see this error:

```
> python functional_tests.py
E
======================================================================
ERROR: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 44, in test_home_page
    table = self.browser.find_element_by_id('id_list_table')
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 351, in find_element_by_id
    return self.find_element(by=By.ID, value=id_)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 955, in find_element
    'value': value})['value']
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 312, in execute
    self.error_handler.check_response(response)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 237, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"id","selector":"id_list_table"}
  (Session info: chrome=64.0.3282.119)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.13.3 x86_64)


----------------------------------------------------------------------
Ran 1 test in 1.901s

FAILED (errors=1)
```

This error is telling us that there is no element with the id `id_list_table` in our template.

Let's add some more details to our current `home.html` template in order to test our user interactions with the list table. Update your file to look like this:

```
<html>
<head>
  <title>To-Do Lists</title>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
  <input id="id_new_item" placeholder="Enter a to-do item" />
  <table id="id_list_table">
  </table>
</body>
</html>
```

Now if we run our test again we get a new error:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 50, in test_home_page
    any(row.text == '1: Buy peacock feathers' for row in rows)
AssertionError: False is not true

----------------------------------------------------------------------
Ran 1 test in 1.914s

FAILED (failures=1)
```

What is this tellng us? We see that we are failing to pass our test, but the error message is not very helpful is it? This has to do with how we wrote our test in the first place. Let's take a closer look at these specific lines of test code:

```
# functional_tests.py

self.assertTrue(
    any(row.text == '1: Buy peacock feathers' for row in rows)
)
```

If we break this code down we see that we have two parts:
- an `any` function that accepts an iterable (a list if things) and will return true if any of the things in the list are true (or truthy).
- a `list comprehension` for generating a list from the content of all the rows.

**An Aside on List Comprehensions in Python**

If you wanted to do this in a long form, imagine you want to build up a list of things (in this case you have a table and you want to look at the text of each row). You would probably declare a `row_text` variable and initialize it to an empty list, then iterate over all the rows in the table adding their text content to the `row_text` variable one by one.

Python provides a shortcut method for building up a list like this in a single line by using a list comprehension (ex. `row.text for row in rows`). This will give you a list object of row.text values. In our test code we are going further by adding a boolean check to the `row.text` value which causes the list comrpehension to produce a list of `true` and `false` values based on the boolean condition being evaluated (eg. `row.text == '1: Buy peacock feathers'`).

What is wrong with this code? Technically nothing, however it is too clever for its own good (code smell warning!). In addition to being slightly difficult to reason about, it also obscures the reason for the test failure with an overly simplified error message (eg. `False is not true`). While we know there was an error, we know very little else about the cause of the error due to the test code obscuring the root cause.

So let's refactor this test into something that will give us better error messaging as to the underlying cause for the test failing. Replace the `self.assertTrue` block with this code instead:

```
# Simpler logic with better error output.
self.assertIn(
    '1: Buy peacock feathers',
    [row.text for row in rows]
)
```

If we run our functional tests again we get a different error message:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 57, in test_home_page
    [row.text for row in rows]
AssertionError: '1: Buy peacock feathers' not found in []

----------------------------------------------------------------------
Ran 1 test in 1.946s

FAILED (failures=1)
```

Now we can more clearly see that the test failed because the text `1: Buy peacock feathers` was not found in the list of rows (which is an empty list `[]`).

We still generated the list of rows, but we tested for the content of the row.text rather than simply returning a boolean value based on the presence of the condition we were testing. This is much easier to reason about with more specific error messaging.

Now let's get the test to pass.

Since the test is telling us that the row list is empty, we can infer that we have no rows in our table. Let's update our table in the `home.html` template to include a row:

```
# lists/templates/home.html

<html>
<head>
  <title>To-Do Lists</title>
  <style>
    body {
      background: #222;
      color: #FFF;
    }
  </style>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
  <input id="id_new_item" placeholder="Enter a to-do item" />
  <table id="id_list_table">
    <tr>
      <td>stuff</td>
    </tr>
  </table>
</body>
</html>
```

Now if we run our functional tests again we get this error:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 57, in test_home_page
    [row.text for row in rows]
AssertionError: '1: Buy peacock feathers' not found in ['stuff']

----------------------------------------------------------------------
Ran 1 test in 1.936s

FAILED (failures=1)
```

Progress!!

We can now see that we are getting some row text in our list (eg. `['stuff']`) and the error clearly indicates that the text we are testing for does not exists in the rows.

We are now getting as far as inputting text, submitting it and looking to see if that text is now in the list of results. However, when we attempt to submit our text, the server is unable to save the data because we have not yet built the form controls required to submit the user data nor setup the database to store the submitted user data. Let's do that now.

## POST Requests and Forms

First we add in a basic form element to wrap our user input field as follows:

```
# lists/templates/home.html

<html>
<head>
  <title>To-Do Lists</title>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
  <form method="POST">
    <input id="id_new_item" placeholder="Enter a to-do item" />
  </form>
  <table id="id_list_table">
    <tr>
      <td>stuff</td>
    </tr>
  </table>
</body>
</html>
```

If you open your browser to `http://localhost:8000` and try to input some text intp the input field you will get a CSRF verification error. Let's run the functional tests again and see what error they give us.

```
> python functional_tests.py
E
======================================================================
ERROR: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 44, in test_home_page
    table = self.browser.find_element_by_id('id_list_table')
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 351, in find_element_by_id
    return self.find_element(by=By.ID, value=id_)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 955, in find_element
    'value': value})['value']
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 312, in execute
    self.error_handler.check_response(response)
  File "/Users/jgentle/.pyenv/versions/3.6.4rc1/envs/python-tdd/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 237, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"id","selector":"id_list_table"}
  (Session info: chrome=64.0.3282.119)
  (Driver info: chromedriver=2.35.528157 (4429ca2590d6988c0745c24c8858745aaaec01ef),platform=Mac OS X 10.13.3 x86_64)


----------------------------------------------------------------------
Ran 1 test in 1.948s

FAILED (errors=1)
```

Suddenly the test can't even find the `id_list_table` anymore! We have made our test results even worse. This is an unexpected failure, so we can try several techniques to identify the cause:
- Add a print statement in the test to debug
- Manually interact with the webpage
- Add a time.sleep into the test to pause it for a period long enbough to inspect the error.

We will try using time.sleep approach. Edit you functional tests to match this:

```
import unittest
import time
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
        # The user should now see their todo in the list:
        # "1: Buy peacock feathers"

        # We are unexpectedly failing here with our form element.
        # Let's pause and inspect the browser during testing.
        time.sleep(10)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        """
        # NOTE: any (boolean func) + list comprehension generator expression.
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )
        """

        # Simpler logic with better error output.
        self.assertIn(
            '1: Buy peacock feathers',
            [row.text for row in rows]
        )

        # The user clicks on the 'add another' option and enters another todo.
        # The user refreshes the page and should now see their new todo in the list.
        # TestCase

        # Etc.

        # Intentionally failing the test.
        self.fail('Finish writing the test! 2:21:46...')

if __name__ == '__main__':
    # unittest.main()
    unittest.main(warnings='ignore')
```

Now if we run our functional tests, the browser wil stay open for 10 seconds so that we can examine the error message. In this case it is identical to what we saw when manually visiting the site, the CRSF error.

**An Aside on CSRF**

A Cross-Site Request Forgery (CRSF) is an attack that can be used to subvert the security of a web application by POSTing form data to another web application as the user account of a valid user on our web application. In order to prevent these sort of injected attacks from working, we use token values that are dynamically generated by our web application, inserted into the web forms from our server, and must be returned with the POST data from the client in order to ensure that the form was indeed from our system and not some malicious third-party. This is a partial soluton to the general problem of unexpected inputs in web applications.

Note: Read the book **Security Engineering** by Ross Anderson _(Cambridge University)_ for detailed exploration of this and many other aspects of security.

Now back to the testing!

We need to add a crsf token into our form, let's do it!

```
# lists/templates/home.html

<html>
<head>
  <title>To-Do Lists</title>
</head>
<body>
  <h1>To-Do Lists Is Coming!</h1>
  <form method="POST">
    <input id="id_new_item" placeholder="Enter a to-do item" />
    {% csrf_token %}
  </form>
  <table id="id_list_table">
    <tr>
      <td>stuff</td>
    </tr>
  </table>
</body>
</html>
```

Now if we run our functional tests again...

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 63, in test_home_page
    [row.text for row in rows]
AssertionError: '1: Buy peacock feathers' not found in ['stuff']

----------------------------------------------------------------------
Ran 1 test in 11.988s

FAILED (failures=1)
```

We see that there is no csrf error, although the server is still silently ignoring all user input data being POSTed. You can also manually test this on your localhost. Since the server still does not return a list item with the correct text content, our test is still failing.

In order to test the server's ability to retain or store data, we will need to create a new test method in our unit tests. We will also update the name of our current unit test method `test_home_page_returns_correct_html` to instead be `test_home_page_uses_home_template`.

```
# lists/tests.py

...
class HomePageViewTest(TestCase):
    """Testing HomePageView"""

    def test_home_page_uses_home_template(self):
        request = HttpRequest()
        response = home_page(request)

        # Read in the template file.
        expected_content = render_to_string('home.html')

        # Compare the template content with the response content.
        self.assertEqual(response.content.decode('utf8'), expected_content)

    def test_home_page_can_store_post_requests(self):
        request = HttpRequest()
        request.POST['item_text'] = 'new item'
        response = home_page(request)
        self.assertIn(
            'new item',
            response.content.decode('utf8')
        )
```

We will also need to update our home.html template to include a name on the input field.

```
# lists/templates/home.html

...
<form method="POST">
  <input id="id_new_item" name="item_text" placeholder="Enter a to-do item" />
  {% csrf_token %}
</form>
...
```

When we run the unit tests, we will get this error now:

```
> python manage.py test lists
Creating test database for alias 'default'...
F.
======================================================================
FAIL: test_home_page_can_store_post_requests (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 29, in test_home_page_can_store_post_requests
    response.content.decode('utf8')
AssertionError: 'new item' not found in '<html>\n<head>\n  <title>To-Do Lists</title>\n  <style>\n    body {\n      background: #222;\n      color: #FFF;\n    }\n  </style>\n</head>\n<body>\n  <h1>To-Do Lists Is Coming!</h1>\n\n  <form method="POST">\n    <input id="id_new_item" name="item_text" placeholder="Enter a to-do item" />\n    \n  </form>\n\n  <table id="id_list_table">\n    <tr>\n      <td>stuff</td>\n    </tr>\n  </table>\n</body>\n</html>\n'

----------------------------------------------------------------------
Ran 2 tests in 0.006s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

We are seeing that the text string is not found in the html response. This indicates that the server is not storing the values being submitted via the form POST. We will need to first update our view function to distinguish between `POST` and `GET` requests from the client. Let's refactor our view function as follows:

```
# lists/views.py

...
def home_page(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])

    return render(request, 'home.html')
```

We will also need to set the request method in the unit test as follows:

```
# lists/tests.py

...
def test_home_page_can_store_post_requests(self):
      request = HttpRequest()
      request.method = 'POST'
      request.POST['item_text'] = 'new item'
      response = home_page(request)
      self.assertIn(
          'new item',
          response.content.decode('utf8')
      )
```

If we run our unit tests again we get a passing test!

```
> python manage.py test lists
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.005s

OK
Destroying test database for alias 'default'...
```

However if we run our functional tests we will see that the site takes our `POST` request text and returns it directly, replacing our UI with just the text we submitted. This is not what we want, instead we want the view function to put the `POST` request text into the table element.

First we need to update our unit test t look for the new item inside the `<td>` element of a row.

```
# lists/tests.py

...
def test_home_page_can_store_post_requests(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = 'new item'
    response = home_page(request)
    self.assertIn(
        '<td>new item</td>',
        response.content.decode('utf8')
    )
```

Second, we will need to update our `home.html` template to include a placeholder for inserting new list items in the table. This uses django template syntax for variables which will allow DJango to inject data into the template before returning it to the client for rendering.

```
# lists/templates/home.html

...
<table id="id_list_table">
  <tr>
    <td>{{ new_item_text }}</td>
  </tr>
</table>
...
```

To make the template syntax variable work, we need to pass a dictionary into the view function (a `context dictionary` in this case) which maps some variable names (from the template) to some values (from the user or database, etc.). Let's update our `test_home_page_can_store_post_requests` unit test to reflect this:

```
# lists/tests.py

...
def test_home_page_can_store_post_requests(self):
      request = HttpRequest()
      request.method = 'POST'
      request.POST['item_text'] = 'new item'
      response = home_page(request)

      expected_content = render_to_string(
          'home.html',
          {'new_item_text': 'new item'}
      )

      self.assertEqual(
          response.content.decode('utf8'),
          expected_content
      )
```

If we run our unit tests again, we will see this error:

```
> python manage.py test
Creating test database for alias 'default'...
F.
======================================================================
FAIL: test_home_page_can_store_post_requests (lists.tests.HomePageViewTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/jgentle/Code/code_practices/python/TDD/django/superlists/lists/tests.py", line 44, in test_home_page_can_store_post_requests
    expected_content
AssertionError: 'new item' != '<html>\n<head>\n  <title>To-Do Lists</tit[373 chars]l>\n'

----------------------------------------------------------------------
Ran 2 tests in 0.007s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

This is complaining because of our simlistic `home_page` view function. We need to setup a proper request method for handling the `POST` data.

```
# lists/views.py

...
def home_page(request):
    if request.method == 'POST':
        return render(request, 'home.html', {
            'new_item_text': request.POST['item_text']
        })

    return render(request, 'home.html')
```

This code basically says if it is a POST request, find the users input, assign it to a new_item_text variable and inject it into the template.

This iteration of the code has moved the applicatio forward from a todo list that can handle zero items, into a todo list tha can handle exactly one item - which is progress!

Let's run our unit tests again to esnure they are passing:

```
> python manage.py test
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.006s

OK
Destroying test database for alias 'default'...
```

Looking good! Now let's try the functional tests:

```
> python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 63, in test_home_page
    [row.text for row in rows]
AssertionError: '1: Buy peacock feathers' not found in ['Buy peacock feathers']

----------------------------------------------------------------------
Ran 1 test in 12.024s

FAILED (failures=1)
```

Hmmm, if you looked at the browser while it was sleeping you will have seen that indeed, our POST request data was properly remdered in out template under the list table. Yet our functional tests are still failing. Why is this?

Closer inspection shows that it is the `1:` prefix that is missing from our todo list item. We can hard code that into the POST value for the time being to pass the test.

```
# lists/templates/home.test_home_page_uses_home_template

...
<table id="id_list_table">
  <tr>
    <td>1: {{ new_item_text }}</td>
  </tr>
</table>
...
```

Now run your functional tests again and...

```
python functional_tests.py
F
======================================================================
FAIL: test_home_page (__main__.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 73, in test_home_page
    self.fail('Finish writing the test! 2:21:46...')
AssertionError: Finish writing the test! 2:21:46...

----------------------------------------------------------------------
Ran 1 test in 12.010s

FAILED (failures=1)
```

SUCCESS! (of a kind). We are now passing the test for the list content and back to our self imposed test failure to remind us to keep testing.

However, there is still a problem. A list is generally not a list without more than one item and if we were to write a second test that submitted a new POST value, we would see that the first POST value will have been removed and replaced by the new value instead of being appended to the list. This is becuse our list only handles one item currently. Now we want to extend it to hanlde n-items.

## TODO

- Extend list to support n-items
- Extend application to support per user lists
- Deploy application live to web
