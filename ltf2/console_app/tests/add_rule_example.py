import time
from typing import Generator
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Page

from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import PropertyPage


PROPERTY_PATH = 'mbondarenko-1/ltf2-test'


@pytest.fixture
def property_page(use_login_state: dict,
                  page: Page,
                  base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    prop_page = PropertyPage(page, url=urljoin(base_url, PROPERTY_PATH))
    prop_page.goto()
    yield prop_page


def test_test(property_page):
    property_page.environment(name='default').click()
    property_page.rules.click()
    property_page.edit_v1_button.click()
    property_page.confirm_button.click()
    property_page.add_rule.click()

    # Add Condition
    property_page.add_condition.click()
    property_page.variable_input.click()
    property_page.variable_select(name='Path').click()
    property_page.operator_input.click()
    property_page.select_by_name(name='Matches').click()
    variable = f'LTF-value-{time.time()}'
    property_page.match_value.fill(variable)
    property_page.add_condition_button.click()

    # Add Feature
    property_page.add_feature.click()
    property_page.feature_type_input.click()
    property_page.select_by_name(name='Headers').click()
    property_page.feature_input.click()
    property_page.select_by_name(name='Set Response Header').click()
    property_page.response_header_name.fill('X-LTF2-Header')
    header = f'ltf2-header-{time.time()}'
    property_page.response_header_value.fill(header)
    property_page.add_feature_button.click()
    # Deploy
    property_page.deploy_changes.click()
