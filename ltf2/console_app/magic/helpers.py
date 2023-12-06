from __future__ import annotations
from random import randint, choice
import string

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError

from ltf2.console_app.magic.elements import TrElements


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


def delete_orgs(orgs: list[(Page, str)]) -> None:
    for page, org_name, in orgs:
        # To make sure that org_switcher_button will be available
        page.goto()
        page.org_switcher_button.click()
        page.org_switcher_list.get_by_text(org_name).click()
        page.settings.click()
        page.delete_org_checkbox.click()
        page.delete_org_button.click()


def delete_rules(rules: list[(Page, str)], url_section: str) -> None:
    for page, rule in rules:
        url = f"{page.url.strip('/')}/security/{url_section}"
        page.goto(url)
        try:
            page.table.wait_for(timeout=10000)  # ms
        except TimeoutError:
            # Check if there is no rules present
            page.no_data_to_display.wait_for(timeout=500)  # ms
            return
        for row in page.table.tbody.tr:
            if row[0].text_content() == rule:
                row[0].click()
                page.delete_button.click()
                page.confirm_button.click()
                # Wait message on snackbar to change
                page.client_snackbar.get_by_text('Successfully deleted').wait_for()
                break


def open_rule_editor(page: Page, url_section: str,
                     name: str, name_index: int = 0) -> TrElements:
    # Make sure every dialog is closed - refresh page
    url = f"{page.url.strip('/')}/security/{url_section}"
    page.goto(url)
    page.table.wait_for()
    for row in page.table.tbody.tr:
        if row[name_index].text_content() == name:
            row[name_index].click()
            return True
    else:
        raise AssertionError("Rule was not saved")


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
