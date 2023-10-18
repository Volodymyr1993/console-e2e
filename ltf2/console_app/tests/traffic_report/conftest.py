from typing import Generator
from urllib.parse import urljoin

import pytest
from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import TrafficPage
from playwright.sync_api import Page


@pytest.fixture
def traffic_page(use_login_state: dict,
                  page: Page,
                  ltfrc_console_app: dict,
                  base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)

    try:
        traffic_path = (f"{ltfrc_console_app['team']}/{ltfrc_console_app['property']}"
                         "/env/production/traffic")
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')
    traffic = TrafficPage(page, url=urljoin(base_url, traffic_path))
    traffic.goto()
    yield traffic

