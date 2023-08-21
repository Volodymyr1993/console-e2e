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

from ltf2.console_app.magic.helpers import delete_teams
from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import LoginPage, TeamPage

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
def create_team(team_page) -> Generator[str, None, None]:
    teams = []
    team_name = f'testname-{time.time()}'
    team_page.team_switcher_button.click()
    team_page.team_switcher_list.li[-1].click()
    team_page.input_name.fill(team_name)
    team_page.button_create_team_dialog.click()
    # Team name is a current team
    team_page.locator('p', has_text=team_name).wait_for(timeout=8000)
    teams.append((team_page, team_name))

    yield team_name

    # Delete team
    delete_teams(teams)


@pytest.fixture
def teams_to_delete() -> Generator[list, None, None]:
    """ Delete teams at test tear down

    teams = [(page, team_name), ...]
    """
    teams = []

    yield teams

    # Remove all mock schedules
    for page, _ in teams:
        page.mock.clear()

    delete_teams(teams)


# ========= Pages =============


@pytest.fixture
def team_page(use_login_state: dict,
              page: Page,
              base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    team_page = TeamPage(page, base_url)
    team_page.goto()
    yield team_page


@pytest.fixture
def login_page(page: Page,
               base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    login_page = LoginPage(page, url=base_url)
    login_page.goto()
    login_page.login_button.click()
    yield login_page
