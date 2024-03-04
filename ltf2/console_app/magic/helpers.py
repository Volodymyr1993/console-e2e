from __future__ import annotations
from random import randint, choice
import string

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError


QUERY_STR_SECURITY_SECTION = '?tab=security&section='


def random_str(n: int) -> str:
    return ''.join([choice(string.ascii_lowercase) for _ in range(n)])


def random_int(n: int) -> str:
    return ''.join([str(randint(1, 9))] + [str(randint(0, 9)) for _ in range(n - 1)])


def login(login_page: Page, username: str, password: str):
    login_page.username.fill(username)
    login_page.submit.click()
    login_page.password.fill(password)
    login_page.submit.click()
    # Skip multi-factor auth if present
    try:
        login_page.skip_this_step.click(timeout=2000)
    except TimeoutError:
        pass
    try:
        login_page.overview.wait_for()
    except TimeoutError as e:
        if login_page.reset_pasword.is_visible():
            raise AssertionError(
                "Password has been expired. "
                "Please reset the password") from e
        raise AssertionError(f"Cannot login to {login_page.url}") from e


def mock_frame_request(page: Page) -> Page:
    page.route("*/embed/frame",
               lambda route: route.fulfill(status=200,
                                           body=''))
    return page


def revert_rules(page: Page):
    try:
        # Click `Revert` button if available
        page.revert_button.click(timeout=4000)
        page.revert_changes_button.click(timeout=2000)
        page.wait_for_timeout(timeout=2000)
    except TimeoutError:
        pass