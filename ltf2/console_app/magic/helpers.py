from __future__ import annotations
from random import randint, choice
import string

from playwright.sync_api import Page

from contextlib import contextmanager

# QUERY_STR_SECURITY_SECTION = '?tab=security&section='


def random_str(n: int) -> str:
    return ''.join([choice(string.ascii_lowercase) for _ in range(n)])


def random_int(n: int) -> str:
    return ''.join([str(randint(1, 9))] + [str(randint(0, 9)) for _ in range(n - 1)])


def delete_teams(teams: list[(Page, str)]) -> None:
    for page, team_name, in teams:
        # To make sure that team_switcher_button will be available
        page.goto()
        page.team_switcher_button.click()
        page.team_switcher_list.get_by_text(team_name).click()
        page.settings.click()
        page.delete_team_checkbox.click()
        page.delete_team_button.click()


# def delete_rules(rules: list[(Page, str)], url_section: str) -> None:
#     for page, rule in rules:
#         url = page.url + QUERY_STR_SECURITY_SECTION + url_section
#         page.goto(url)
#         page.table.wait_for()
#         for row in page.table.tbody.tr:
#             if row[0].text_content() == rule:
#                 row[0].click()
#                 page.delete_button.click()
#                 page.confirm_button.click()
#                 # Wait message on snackbar to change
#                 page.client_snackbar.get_by_text('Successfully deleted').wait_for()
#                 break
#
#
# def open_rule_editor(page: Page, url_section: str,
#                      name: str, name_index: int = 0) -> TrElements:
#     # Make sure every dialog is closed - refresh page
#     url = page.url + QUERY_STR_SECURITY_SECTION + url_section
#     page.goto(url)
#     page.table.wait_for()
#     for row in page.table.tbody.tr:
#         if row[name_index].text_content() == name:
#             row[name_index].click()
#             return True
#     else:
#         raise AssertionError("Rule was not saved")
#
#
# def mock_frame_request(page: Page) -> Page:
#     page.route("*/embed/frame",
#                lambda route: route.fulfill(status=200,
#                                            body=''))
#     return page