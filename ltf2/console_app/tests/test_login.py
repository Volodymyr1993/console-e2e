from collections import namedtuple

from ltf2.console_app.magic.pages.pages import LoginPage


def test_negative_wrong_email_format(login_page: LoginPage, credentials: namedtuple):
    """ Login - Negative - Wrong email format

    Precondition:
    -------------
    1. Navigate to Login page

    Steps:
    ------
    1. Put wrong email format string in Email field
    2. Push 'Sign In' button

    Expected Results:
    -----------------
    2. 'Invalid email' message should appear
    """
    login_page.email.fill('wrong email format')
    login_page.password.fill(credentials.password)
    assert login_page.error_message.text_content() == 'Invalid email'


def test_negative_empty_email_password(login_page: LoginPage, credentials: namedtuple):
    """ Login - Negative - Empty email or password

    Precondition:
    -------------
    1. Navigate to Login page

    Steps:
    ------
    1. Put some email and empty password
    2. Push 'Sign In' button
    3. Put empty email and some password
    4. Push 'Sign In' button

    Expected Results:
    -----------------
    2. 'Required' message should appear
    4. 'Required' message should appear
    """
    login_page.email.fill(credentials.users[0])
    login_page.password.fill('')
    login_page.submit.click()
    assert login_page.error_message.text_content() == 'Required'

    login_page.email.fill('')
    login_page.password.fill(credentials.password)
    login_page.submit.click()
    assert login_page.error_message.text_content() == 'Required'


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
    login_page.email.fill(credentials.users[0])
    login_page.password.fill('wrong_password')
    login_page.submit.click()
    assert login_page.invalid_email_or_password_message.text_content() == \
           'Invalid login or password '


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
    login_page.email.fill(credentials.users[0])
    login_page.password.fill(credentials.password)
    login_page.submit.click()
    login_page.login_successful.wait_for(timeout=8 * 1000)
    assert login_page.login_successful.text_content() == 'Login successful!'

    login_page.team_switcher_button.wait_for()
