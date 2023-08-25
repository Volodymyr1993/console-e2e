from __future__ import annotations

import os
import time
from collections import namedtuple
from typing import Generator
from urllib.parse import urljoin

import pytest
from ltf2.util.config import get_ltfrc_section
from playwright.sync_api import Page, Browser
from requests.structures import CaseInsensitiveDict
from playwright._impl._api_types import TimeoutError

from ltf2.console_app.magic.helpers import delete_orgs
from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import LoginPage, OrgPage

# Explicitly import to avoid using the `context` fixture from ltf2.utils
from pytest_playwright.pytest_playwright import context

Credentials = namedtuple('Credentials', 'users password')


@pytest.fixture(scope='session')
def ltfrc_console_app() -> CaseInsensitiveDict:
    """
    Returns .ltfrc config dict
    """
    return get_ltfrc_section("edgio-console-app")


@pytest.fixture(scope='session')
def base_url(ltfrc_console_app: CaseInsensitiveDict) -> str:
    return ltfrc_console_app['url']


@pytest.fixture(scope='session')
def credentials(ltfrc_console_app: CaseInsensitiveDict) -> Credentials:
    users_str = os.getenv('EDGIO_USER') or ltfrc_console_app.get('users')
    password = os.getenv('EDGIO_PASSWORD') or ltfrc_console_app.get('password')
    if not password or not users_str:
        raise RuntimeError('EDGIO_USER and EDGIO_PASSWORD should be '
                           'set as env variables or in ~/.ltfrc file')
    return Credentials([u.strip() for u in users_str.split(',') if u],
                       password)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict,
                             ltfrc_console_app: CaseInsensitiveDict,
                             request):
    """ Update browser parameters """
    headed = request.config.getoption('--headed')
    slow_mo = request.config.getoption('--slowmo')
    return {
        **browser_type_launch_args,
        'headless': not (headed or bool(ltfrc_console_app.get('headed'))),
        'slow_mo': slow_mo,
        'timeout': 60 * 1000,  # 60 sec
       # 'devtools': True,
    }


@pytest.fixture(scope="session")
def saved_login(browser: Browser,
                base_url: str,
                credentials: namedtuple) -> Generator[str, None, None]:
    """ Save signed-in state for reusing that state to skip log-in in tests.

    Return cookies
    """
    context = browser.new_context()
    page = context.new_page()
    # go to login page
    login_page = LoginPage(page, url=base_url)
    login_page.goto()
    login_page.login_button.click()
    # perform login
    login_page.username.fill(credentials.users[0])
    login_page.submit.click()
    login_page.password.fill(credentials.password)
    login_page.submit.click()

    # Skip multi-factor auth if present
    try:
        login_page.skip_this_step.click(timeout=2000)
    except TimeoutError:
        pass
    try:
        login_page.overview.wait_for()
    except TimeoutError:
        raise AssertionError(f"Cannot login to {base_url}")
    assert not login_page.submit.is_visible()
    # Save storage state into the file.
    storage_state = {'cookies': context.cookies()}
    context.close()
    yield storage_state


@pytest.fixture
def use_login_state(browser_context_args: dict, saved_login: dict) -> dict:
    """ Use previously saved login state.

    Update `browser_context_args` with storage state that will be used in context
    creation.

    NOTE: to apply `browser_context_args` on the context `use_login_state` fixture should
    be specified before `page` fixture!
    """
    browser_context_args['storage_state'] = saved_login


@pytest.fixture
def create_org(org_page) -> Generator[str, None, None]:
    orgs = []
    org_name = f'testname-{time.time()}'
    org_page.org_switcher_button.click()
    org_page.org_switcher_list.li[-1].click()
    org_page.input_name.fill(org_name)
    org_page.button_create_org_dialog.click()
    # Organization name is a current org
    org_page.locator('p', has_text=org_name).wait_for(timeout=8000)
    orgs.append((org_page, org_name))

    yield org_name

    # Delete org
    delete_orgs(orgs)


@pytest.fixture
def orgs_to_delete() -> Generator[list, None, None]:
    """ Delete orgs at test tear down

    orgs = [(page, org_name), ...]
    """
    orgs = []

    yield orgs

    # Remove all mock schedules
    for page, _ in orgs:
        page.mock.clear()

    delete_orgs(orgs)


# ========= Pages =============


@pytest.fixture
def org_page(use_login_state: dict,
              page: Page,
              base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    org_page = OrgPage(page, base_url)
    org_page.goto()
    yield org_page


@pytest.fixture
def login_page(page: Page,
               base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    login_page = LoginPage(page, url=base_url)
    login_page.goto()
    login_page.login_button.click()
    yield login_page
