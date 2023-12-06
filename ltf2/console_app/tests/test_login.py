from collections import namedtuple

import pytest

from ltf2.console_app.magic.helpers import login
from ltf2.console_app.magic.pages.pages import LoginPage


@pytest.mark.regression
def test_negative_wrong_email_format(login_page: LoginPage):
    """ Login - Negative - Wrong email format

    Precondition:
    -------------
    1. Navigate to Login page

    Steps:
    ------
    1. Put wrong email format string in Email field
    2. Push 'Next' button

    Expected Results:
    -----------------
    2. 'Invalid username' message should appear
    """
    login_page.username.fill('wrong username format')
    login_page.submit.click()
    assert login_page.invalid_email_or_password_message.text_content() == 'Invalid username'


@pytest.mark.regression
def test_negative_empty_email_password(login_page: LoginPage, credentials: namedtuple):
    """ Login - Negative - Empty email or password

    Precondition:
    -------------
    1. Navigate to Login page

    Steps:
    ------
    1. Put empty email
    2. Push 'Sign In' button
    3. Put some email and empty password
    4. Push 'Sign In' button

    Expected Results:
    -----------------
    2. 'Required' message should appear
    4. 'Required' message should appear
    """
    login_page.username.fill('')
    login_page.submit.click()
    assert login_page.error_message.text_content() == 'Required'

    login_page.username.fill(credentials.users[0])
    login_page.submit.click()
    login_page.password.fill('')
    login_page.submit.click()
    assert login_page.error_message.text_content() == 'Required'


@pytest.mark.regression
def test_negative_wrong_password(login_page: LoginPage, credentials: namedtuple):
    """ Login - Negative - Wrong password

    Precondition:
    -------------
    1. Navigate to Login page

    Steps:
    ------
    1. Put correct email and wrong password
    2. Push 'Sign In' button

    Expected Results:
    -----------------
    2. 'Invalid login or password ' message should appear
    """
    login_page.username.fill(credentials.users[0])
    login_page.submit.click()
    login_page.password.fill('wrong_password')
    login_page.submit.click()
    assert login_page.invalid_email_or_password_message.text_content() == \
           'Invalid username or password'


@pytest.mark.regression
def test_positive_login(login_page: LoginPage, credentials: namedtuple):
    """ Login - Positive login

    Precondition:
    -------------
    1. Navigate to Login page

    Steps:
    ------
    1. Put correct email and password

    Expected Results:
    -----------------
    1. Get 'Login successful!' message and team switcher appears
    """
    login(login_page, credentials.users[0], credentials.password)
    assert not login_page.submit.is_visible()
