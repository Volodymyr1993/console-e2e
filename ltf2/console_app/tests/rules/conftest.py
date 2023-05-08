from typing import Generator
from urllib.parse import urljoin

import pytest
from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.helpers import revert_rules
from ltf2.console_app.magic.pages.pages import PropertyPage
from playwright.sync_api import Page


@pytest.fixture
def property_page(use_login_state: dict,
                  page: Page,
                  ltfrc: dict,
                  base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)

    try:
        property_path = \
            f"{ltfrc['team']}/{ltfrc['property']}/env/production/configuration/rules"
    except KeyError:
        raise ValueError(f'team and property variables are missed in .ltfrc')
    prop_page = PropertyPage(page, url=urljoin(base_url, property_path))
    prop_page.mock.page.unroute("**/graphql")
    prop_page.goto()
    # Revert previously added rules
    revert_rules(prop_page)
    yield prop_page

