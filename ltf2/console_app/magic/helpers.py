from __future__ import annotations
from random import randint, choice
import string

from playwright.sync_api import Page

from ltf2.console_app.magic.elements import TrElements
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

    @contextmanager
    def prepare_feature_type(self):
        """ Setup page and save feature after creation """
        self.page.add_feature.last.click()
        self.page.feature_type_input.click()
        try:
            yield
        except Exception:
            raise
        else:
            self.page.add_feature_button.click()

    @contextmanager
    def prepare_feature(self, feature_type, feature):
        with self.prepare_feature_type():
            self.page.select_by_name(name=feature_type).click()
            self.page.feature_input.click()
            self.page.select_by_name(name=feature).click()
            yield

    def add_url(self, feature: str = '', code: int = 302, source: str = '',
                destination: str = '', ignore_case: bool = False,
                follow_redirects: bool = True):
        with self.prepare_feature('URL', feature):
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

    def add_headers(self, feature: str = '', header_name: str = '',
                    header_value: str = '', enable: bool = True):
        with self.prepare_feature('Headers', feature):
            if feature in ('Set Response Header',
                           'Add Response Header',
                           'Set Request Header'):
                self.page.header_name.fill(header_name)
                self.page.header_value.fill(header_value)
            elif feature == 'Debug Header':
                self.page.rule_checkbox.set_checked(enable)
            elif feature == 'Remove Origin Response Headers':
                self.page.origin_response_headers.fill(header_name)
            elif feature == 'Remove Response Headers':
                self.page.response_headers.fill(header_name)

    def add_set_variables(self, name: str = '', value: str = ''):
        with self.prepare_feature_type('Set Variables'):
            self.page.variable_name.fill(name)
            self.page.variable_value.fill(value)

    def add_access(self, feature: str = '', enable: bool = True):
        with self.prepare_feature('Access', feature):
            self.page.rule_checkbox.set_checked(enable)

    def add_logs(self, feature: str = '', custom_log_field: str = '',
                 enable: bool = True):
        with self.prepare_feature('Logs', feature):
            if feature == 'Custom Log Field':
                self.page.custom_log_field.fill(custom_log_field)
            else:
                self.page.rule_checkbox.set_checked(enable)

    def add_response(self, feature: str = '', code: int = 200, body: str = '',
                     enable: bool = True):
        with self.prepare_feature('Response', feature):
            if feature == 'Set Status Code':
                self.page.status_code_input.fill(str(code))
            elif feature == 'Set Done':
                self.page.rule_checkbox.set_checked(enable)
            elif feature == 'Set Response Body':
                self.page.response_body.fill(body)

    def add_caching(self, feature: str = '', kbytes_per_second: int = 1024,
                    prebuf_seconds: int = 0, enable: bool = True,
                    header_treatment: str = '', option: str = '', value: str = '',
                    cacheable_request_body_size: int = 0, compress_file_types: str = '',
                    ):
        with self.prepare_feature('Caching', feature):
            if feature in ('Bandwidth Parameters', 'Bypass Cache'):
                self.page.rule_checkbox.set_checked(enable)
            elif feature == 'Bandwidth Throttling':
                self.page.kbytes_per_second.fill(str(kbytes_per_second))
                self.page.prebuf_seconds.fill(str(prebuf_seconds))
            elif feature == 'Cache Control Header Treatment':
                self.page.header_treatment_input.click()
                self.page.select_by_name(name=header_treatment).click()
            elif feature == 'Cache Key Query String':
                self.page.option_input.click()
                self.page.select_by_name(name=option).click()
                if option == 'Include':
                    self.page.include_input.fill(value)
                elif option == 'Exclude':
                    self.page.exclude_input.fill(value)
                else:
                    self.page.rule_checkbox.set_checked(enable)
            elif feature == 'Cacheable Request Body Size':
                self.page.cacheable_request_body_size.fill(str(cacheable_request_body_size))
            elif feature == 'Compress File Types':
                self.page.compress_file_types.fill(compress_file_types)
                self.page.compress_file_types.press('Enter')

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