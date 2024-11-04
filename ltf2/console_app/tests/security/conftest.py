from __future__ import annotations

from typing import Generator
from urllib.parse import urljoin

import pytest
from playwright.sync_api import TimeoutError
from playwright.sync_api import Page, Browser

from ltf2.console_app.magic.constants import PAGE_TIMEOUT, SECURITY_RULE_NAME_PREFIX
from ltf2.console_app.magic.pages.pages import SecurityPage


def generate_fixture(delete_method: str):
    @pytest.fixture
    def delete_rule(security_logged):
        rules = []

        yield rules

        getattr(security_logged, delete_method)(rules)
    return delete_rule


def inject_fixture(name: str):
    globals()[name] = generate_fixture(name)


# Add fixtures that delete specified rules
inject_fixture('delete_access_rules')
inject_fixture('delete_managed_rules')
inject_fixture('delete_rate_rules')


@pytest.fixture
def delete_sec_app(security_app_page):
    """ Delete security app rules created in test case """
    rules = []

    yield rules

    security_app_page.delete_security_app_rules(rules)


@pytest.fixture(scope="module")
def setup_security_rules(browser: Browser,
                         base_url: str,
                         ltfrc_console_app: dict,
                         browser_context_args: dict,
                         saved_login: dict) -> Generator[SecurityPage, None, None]:
    """ Create Security Page for fixtures with module scope """
    browser_context_args = browser_context_args.copy()
    browser_context_args['storage_state'] = saved_login
    br_context = browser.new_context(**browser_context_args)
    page = br_context.new_page()
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    sec_page = SecurityPage(page, url=urljoin(base_url, ltfrc_console_app['team']))
    sec_page.goto()
    sec_page.security.click()
    # Close the status banner if present
    try:
        sec_page.status_snackbar_close.click(timeout=1500)
    except TimeoutError:
        print('Status banner not found')

    yield sec_page


@pytest.fixture(scope="module")
def cleanup_managed_rules(setup_security_rules: SecurityPage,
                        cmp) -> None:
    """ Delete Managed Rules from previous run """
    setup_security_rules.managed_rules.click()
    setup_security_rules.delete_managed_rules(
        [cmp.re_match(SECURITY_RULE_NAME_PREFIX)])
    setup_security_rules.page.close()


@pytest.fixture(scope="module")
def cleanup_access_rules(setup_security_rules: SecurityPage,
                       cmp) -> None:
    """ Delete Access Rules from previous run """
    setup_security_rules.access_rules.click()
    setup_security_rules.delete_access_rules(
        [cmp.re_match(SECURITY_RULE_NAME_PREFIX)])
    setup_security_rules.page.close()


@pytest.fixture(scope="module")
def cleanup_rate_rules(setup_security_rules: SecurityPage,
                     cmp) -> None:
    """ Delete Rate Rules from previous run """
    setup_security_rules.rate_rules.click()
    setup_security_rules.delete_rate_rules(
        [cmp.re_match(SECURITY_RULE_NAME_PREFIX)])
    setup_security_rules.page.close()


@pytest.fixture(scope="module")
def cleanup_security_app_rules(setup_security_rules: SecurityPage) -> None:
    """ Delete Security App Rules from previous run """
    setup_security_rules.security_application.click()
    # Check if there is no rules present
    try:
        setup_security_rules.no_data_to_display.wait_for(timeout=3000)  # ms
        setup_security_rules.page.close()
        return
    except TimeoutError:
        pass

    setup_security_rules.secapp_names.wait_for()
    secapps_rule = setup_security_rules.secapp_names.all_inner_texts()
    rules = [rule for rule in secapps_rule if rule.startswith(SECURITY_RULE_NAME_PREFIX)]

    setup_security_rules.delete_security_app_rules(rules)
    setup_security_rules.page.close()


# =============== Pages ======================


@pytest.fixture
def security_logged(use_login_state: dict,
                    page: Page,
                    base_url: str,
                    ltfrc_console_app) -> Generator[SecurityPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    main_page = SecurityPage(page, url=urljoin(base_url, ltfrc_console_app['team']))
    main_page.goto()
    main_page.security.click()
    # Close the status banner if present
    try:
        main_page.status_snackbar_close.click(timeout=1500)
    except TimeoutError:
        print('Status banner not found')
    yield main_page
    main_page.mock.clear()


@pytest.fixture
def dashboard_page(security_logged) -> Generator[SecurityPage, None, None]:
    security_logged.dashboard.click()
    yield security_logged


@pytest.fixture
def managed_rules_page(cleanup_managed_rules,
                       security_logged: SecurityPage) -> Generator[SecurityPage, None, None]:
    security_logged.managed_rules.click()
    yield security_logged


@pytest.fixture
def access_rules_page(cleanup_access_rules,
                      security_logged: SecurityPage) -> Generator[SecurityPage, None, None]:
    security_logged.access_rules.click()
    yield security_logged


@pytest.fixture
def rate_rules_page(cleanup_rate_rules,
                    security_logged: SecurityPage) -> Generator[SecurityPage, None, None]:
    security_logged.rate_rules.click()
    yield security_logged


@pytest.fixture
def security_app_page(cleanup_security_app_rules,
                      security_logged: SecurityPage) -> Generator[SecurityPage, None, None]:
    security_logged.security_application.click()
    yield security_logged
