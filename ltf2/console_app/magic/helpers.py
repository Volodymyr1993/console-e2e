from __future__ import annotations
from random import randint, choice
import string

from playwright.sync_api import Page

from ltf2.console_app.magic.elements import TrElements


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


class RuleCondition:
    """ Class for work with Conditions in the Rule tab """
    def __init__(self, page):
        self.page = page

    def add_path(self, operator='Matches', value=''):
        self.page.add_condition.last.click()
        self.page.variable_input.click()
        self.page.variable_select(name='Path').click()
        self.page.operator_input.click()
        self.page.select_by_name(name=operator).click()
        self.page.match_value.fill(value)
        self.page.add_condition_button.click()


class RuleFeature:
    """ Class for work with Features in the Rule tab """
    def __init__(self, page):
        self.page = page

    def __getattr__(self, item):
        try:
            prefix, method = item.split('_', 1)
            if prefix == 'add':
                # Add feature
                self.page.add_feature.last.click()
                self.page.feature_type_input.click()
                # DOTO add decorator to methods
                return getattr(self, method)
        except ValueError:
            pass

    def url(self, feature='', code=302, source='', destination='',
            ignore_case=False, follow_redirects=True):
        # Select 'URL' feature
        self.page.select_by_name(name='URL').click()
        self.page.feature_input.click()
        self.page.select_by_name(name=feature).click()
        if feature == 'Follow Redirects':
            self.page.rule_checkbox.set_checked(follow_redirects)
            self.page.add_feature_button.click()
            return
        elif feature == 'URL Redirect':
            # TODO uncomment when bug with Status code is fixed
            # self.page.code_input.fill(str(code))
            pass
        self.page.rule_checkbox.set_checked(ignore_case)
        self.page.source_input.fill(source)
        self.page.destination_input.fill(destination)
        self.page.add_feature_button.click()

    def headers(self, feature='', header_name='', header_value='', debug_header=True):
        self.page.select_by_name(name='Headers').click()
        self.page.feature_input.click()
        self.page.select_by_name(name=feature).click()
        if feature in ('Set Response Header',
                       'Add Response Header',
                       'Set Request Header'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)
        elif feature == 'Debug Header':
            self.page.rule_checkbox.set_checked(debug_header)
        elif feature == 'Remove Origin Response Headers':
            self.page.origin_response_headers.fill(header_name)
        elif feature == 'Remove Response Headers':
            self.page.response_headers.fill(header_name)
        self.page.add_feature_button.click()

    def set_variables(self, name='', value=''):
        self.page.select_by_name(name='Set Variables').click()
        self.page.variable_name.fill(name)
        self.page.variable_value.fill(value)
        self.page.add_feature_button.click()

    def access(self, feature='', enable=True):
        self.page.select_by_name(name='Access').click()
        self.page.feature_input.click()
        self.page.select_by_name(name=feature).click()
        self.page.rule_checkbox.set_checked(enable)
        self.page.add_feature_button.click()

    def logs(self, feature='', custom_log_field='', enable=True):
        self.page.select_by_name(name='Logs').click()
        self.page.feature_input.click()
        self.page.select_by_name(name=feature).click()
        if feature == 'Custom Log Field':
            self.page.custom_log_field.fill(custom_log_field)
        else:
            self.page.rule_checkbox.set_checked(enable)
        self.page.add_feature_button.click()

    def response(self, feature='', custom_log_field='', enable=True):
        self.page.select_by_name(name='Response').click()
        self.page.feature_input.click()
        self.page.select_by_name(name=feature).click()
        breakpoint()
        if feature == 'Set Status Code':
            pass
        elif feature == 'Set Done':
            self.page.rule_checkbox.set_checked(enable)
        elif feature == 'Set Response Body':
            pass
        self.page.add_feature_button.click()
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