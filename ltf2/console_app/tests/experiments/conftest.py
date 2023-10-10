import pytest
from playwright.sync_api import Page
from typing import Generator
from urllib.parse import urljoin

from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import ExperimentsPage


@pytest.fixture
def experiment_page(use_login_state: dict,
                         page: Page,
                         ltfrc_console_app: dict,
                         base_url: str) -> Generator[Page, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    # TODO: change property to production
    try:
        property_path = (f"{ltfrc_console_app['team']}/{ltfrc_console_app['property']}"
                         "/env/zaplatkin/configuration/experiments")
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
