from __future__ import annotations

from typing import Generator
from urllib.parse import urljoin

import pytest
from playwright.sync_api import TimeoutError
from playwright.sync_api import Page

from ltf2.console_app.magic.constants import PAGE_TIMEOUT
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
def delete_sec_app():
    rules = []

    yield rules

    # Remove all mock schedules
    for page, rule in rules:
        page.mock.clear()
        page.goto(f"{page.url.strip('/')}/security/application")
        page.secapp_by_name(name=rule).click()
        page.delete_button.click()
        page.confirm_button.click()
        page.save_secapp.click()
        page.client_snackbar.get_by_text('Security application updated').wait_for()


# =============== Pages ======================


@pytest.fixture
def security_logged(use_login_state: dict,
                    page: Page,
                    base_url: str,
                    ltfrc_console_app) -> Generator[Page, None, None]:
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
def managed_rules_page(security_logged) -> Generator[SecurityPage, None, None]:
    security_logged.managed_rules.click()
    yield security_logged


@pytest.fixture
def access_rules_page(security_logged) -> Generator[SecurityPage, None, None]:
    security_logged.access_rules.click()
    yield security_logged


@pytest.fixture
def rate_rules_page(security_logged) -> Generator[SecurityPage, None, None]:
    security_logged.rate_rules.click()
    yield security_logged


@pytest.fixture
def security_app_page(security_logged) -> Generator[SecurityPage, None, None]:
    security_logged.security_application.click()
    yield security_logged
