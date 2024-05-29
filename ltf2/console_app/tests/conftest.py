from __future__ import annotations

import pickle

import os
import time
from collections import namedtuple
from pathlib import Path
from typing import Generator
from urllib.parse import urljoin

import pytest
from ltf2.util import comparators
from ltf2.util.config import get_ltfrc_section
from playwright.sync_api import Browser, Page, TimeoutError
# Explicitly import to avoid using the `context` fixture from ltf2.utils
from pytest_playwright.pytest_playwright import context
from requests.structures import CaseInsensitiveDict

from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import (ExperimentsPage, LoginPage,
                                                OrgPage, PropertyPage,
                                                TrafficPage, RedirectsPage,
                                                OriginsPage, EnvironmentVariablesPage)

Credentials = namedtuple('Credentials', 'users password')


ENV_URL_PATH = "env/production/"
TRAFFIC_URL_PATH = f"{ENV_URL_PATH}traffic"
EXPERIMENTS_URL_PATH = f"{ENV_URL_PATH}configuration/experiments"
PROPERTY_URL_PATH = f"{ENV_URL_PATH}configuration/rules"
REDIRECTS_URL_PATH = f"{ENV_URL_PATH}redirects"
ORIGINS_URL_PATH = f"{ENV_URL_PATH}configuration/origins"
ENV_VARIABLE_URL_PATH = f"{ENV_URL_PATH}variables"


@pytest.fixture(scope='session')
def project_dir():
    """
    Returns pathlib.Path instance of project data directory
    """
    return Path(__file__).parent.absolute()


@pytest.fixture(scope='session')
def ltfrc_console_app() -> CaseInsensitiveDict | dict:
    """
    Returns .ltfrc config dict
    """
    return get_ltfrc_section("edgio-console-app")


@pytest.fixture(scope='session')
def base_url(ltfrc_console_app: CaseInsensitiveDict) -> str:
    return ltfrc_console_app['url']


@pytest.fixture(scope='session')
def cmp():
    """ LTF2 comparators """
    return comparators


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
def saved_login(project_dir,
                browser: Browser,
                base_url: str,
                credentials: namedtuple) -> dict:
    """ Save signed in state for reusing that state to skip log-in in tests.

    Return cookies
    """
    cookies_file = project_dir / 'cookies.pkl'
    if cookies_file.exists():
        return pickle.load(cookies_file.open('rb'))
    br_context = browser.new_context()
    page = br_context.new_page()
    # go to login page
    login_page = LoginPage(page, url=base_url)
    login_page.goto()
    # perform login
    login_page.login(credentials.users[0], credentials.password)
    assert not login_page.submit.is_visible()
    # Close the status banner if present
    try:
        login_page.status_snackbar_close.click(timeout=1500)
    except TimeoutError:
        print('Status banner not found')
    # Save storage state into the file.
    storage_state = {'cookies': br_context.cookies()}

    with cookies_file.open('wb') as f:
        pickle.dump(storage_state, f)
    br_context.close()
    return storage_state


@pytest.fixture
def use_login_state(browser_context_args: dict, saved_login: dict) -> dict:
    """ Use previously saved login state.

    Update `browser_context_args` with storage state that will be used in context
    creation.

    NOTE: to apply `browser_context_args` on the context `use_login_state` fixture should
    be specified before `page` fixture!
    """
    browser_context_args['storage_state'] = saved_login
    yield
    del browser_context_args['storage_state']


@pytest.fixture
def create_org(org_page) -> Generator[str, None, None]:
    """ Create org and delete on teardown """
    orgs = []
    org_name = f'test-organization-{int(time.time()*1000)}'
    org_page.org_switcher_button.click()
    org_page.org_switcher_list.li[-1].click()
    org_page.input_name.fill(org_name)
    org_page.button_create_org_dialog.click()
    # Organization name is a current org
    org_page.selected_org(name=org_name).wait_for(timeout=8000)
    orgs.append(org_name)

    yield org_name

    # Delete org
    org_page.delete_orgs(orgs)


@pytest.fixture
def orgs_to_delete(org_page) -> Generator[list, None, None]:
    """ Delete orgs at test tear down """
    orgs = []

    yield orgs

    # Remove mock schedules
    org_page.mock.clear()

    org_page.delete_orgs(orgs)


# ========= Pages =============


@pytest.fixture
def org_page(use_login_state: dict,
             page: Page,
             base_url: str) -> Generator[OrgPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    org_page = OrgPage(page, base_url)
    org_page.goto()
    yield org_page


@pytest.fixture
def login_page(page: Page,
               base_url: str) -> Generator[LoginPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    loginpage = LoginPage(page, url=base_url)
    loginpage.goto()
    yield loginpage


@pytest.fixture
def property_page(use_login_state: dict,
                  page: Page,
                  ltfrc_console_app: dict,
                  base_url: str) -> Generator[PropertyPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)

    try:
        property_path = (f"{ltfrc_console_app['team']}/"
                         f"{ltfrc_console_app['property']}/"
                         f"{PROPERTY_URL_PATH}")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')
    prop_page = PropertyPage(page, url=urljoin(base_url, property_path))
    prop_page.mock.page.unroute("**/graphql")
    prop_page.goto()
    # Revert previously added rules
    prop_page.revert_rules()
    yield prop_page


@pytest.fixture
def experiment_page(use_login_state: dict,
                    page: Page,
                    ltfrc_console_app: dict,
                    base_url: str) -> Generator[ExperimentsPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    try:
        property_path = (f"{ltfrc_console_app['team']}/"
                         f"{ltfrc_console_app['property']}/"
                         f"{EXPERIMENTS_URL_PATH}")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')

    exp_page = ExperimentsPage(page, url=urljoin(base_url, property_path))
    exp_page.goto()
    exp_page.add_experiment_button.wait_for(timeout=30000)

    # click revert button if present
    if exp_page.revert_button.is_visible():
        exp_page.revert_button.click()
        exp_page.revert_confirm_button.click()
        exp_page.add_experiment_button.wait_for(timeout=30000)

    # delete all experiments and deploy changes
    exp_page.delete_all_experiments()
    if exp_page.deploy_changes_button.is_visible():
        exp_page.deploy_changes()

    yield exp_page
    # delete all experiments and deploy changes
    if exp_page.delete_experiment_list.is_visible():
        exp_page.delete_all_experiments()


@pytest.fixture
def traffic_page(use_login_state: dict,
                 page: Page,
                 ltfrc_console_app: dict,
                 base_url: str) -> Generator[TrafficPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)

    try:
        traffic_path = (f"{ltfrc_console_app['team']}/"
                        f"{ltfrc_console_app['property']}/"
                        f"{TRAFFIC_URL_PATH}")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')
    traffic = TrafficPage(page, url=urljoin(base_url, traffic_path))
    traffic.goto()
    yield traffic


@pytest.fixture
def redirect_page(use_login_state: dict,
                  page: Page,
                  ltfrc_console_app: dict,
                  base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    try:
        property_path = (f"{ltfrc_console_app['team']}/"
                         f"{ltfrc_console_app['property']}/"
                         f"{REDIRECTS_URL_PATH}")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')

    red_page = RedirectsPage(page, url=urljoin(base_url, property_path))
    # Remove GraphQl mock
    red_page.mock.page.unroute("**/graphql")
    red_page.goto()
    red_page.add_a_redirect_button.wait_for(timeout=30000)

    # delete all redirects if present
    if not red_page.empty_list_message.is_visible():
        red_page.delete_all_redirects()

    yield red_page

@pytest.fixture
def origins_page(use_login_state: dict,
                 page: Page,
                 ltfrc_console_app: dict,
                 base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    try:
        property_path = (f"{ltfrc_console_app['team']}/"
                         f"{ltfrc_console_app['property']}/"
                         f"{ORIGINS_URL_PATH}")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')

    origins_page = OriginsPage(page, url=urljoin(base_url, property_path))
    origins_page.goto()
    origins_page.origins_title.wait_for(timeout=30000)

    # delete all origins if present
    if origins_page.delete_button_list.first.is_visible():
        origins_page.delete_all_origins()
        origins_page.deploy_changes_button.wait_for(timeout=30000)

        # Delete it after bug fixing https://edgio.atlassian.net/browse/CON-1192
        origins_page.reload()

    yield origins_page

@pytest.fixture
def env_variable_page(use_login_state: dict,
                page: Page,
                ltfrc_console_app: dict,
                base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    try:
        property_path = (f"{ltfrc_console_app['team']}/"
                         f"{ltfrc_console_app['property']}/"
                         f"{ENV_VARIABLE_URL_PATH}")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')

    env_var = EnvironmentVariablesPage(page, url=urljoin(base_url, property_path))
    env_var.goto()
    env_var.env_variable_title.wait_for(timeout=30000)

    # delete all environment variables if present
    if env_var.delete_button_list.first.is_visible():
        env_var.delete_all_variables()

    yield env_var