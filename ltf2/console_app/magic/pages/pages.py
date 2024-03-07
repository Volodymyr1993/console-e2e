"""
Classes that represent pages.

Each page should be inherited from mixins that describe the elements of the page
and BasePage class. Please note that the position of the mixins and BasePage is important
(BasePage should follow mixin) as super() follows the MRO.
"""
from __future__ import annotations

import csv
from io import StringIO

from playwright.sync_api import Page, TimeoutError

from ltf2.console_app.magic.nested_rules import NestedRules
from ltf2.console_app.magic.pages.base_page import BasePage
from ltf2.console_app.magic.pages.components import (CommonMixin,
                                                     DeploymentsMixin,
                                                     EnvironmentMixin,
                                                     ExperimentsMixin,
                                                     LoginMixin, OrgMixin,
                                                     RedirectsMixin,
                                                     SecurityMixin,
                                                     TrafficMixin,
                                                     OriginsMixin)
from ltf2.console_app.magic.ruleconfig import (ExperimentCondition,
                                               ExperimentFeature,
                                               RuleCondition, RuleFeature)


class LoginPage(CommonMixin, LoginMixin, BasePage):
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.submit.click()
        self.password.fill(password)
        self.submit.click()
        # Skip multi-factor auth if present
        try:
            self.skip_this_step.click(timeout=2000)
        except TimeoutError:
            pass
        try:
            self.overview.wait_for()
        except TimeoutError as e:
            if self.reset_pasword.is_visible():
                raise AssertionError(
                    "Password has been expired. "
                    "Please reset the password") from e
            raise AssertionError(f"Cannot login to {self.url}") from e


class OrgPage(CommonMixin, OrgMixin, BasePage):
    def delete_orgs(self, orgs: list[str]) -> None:
        for org_name in orgs:
            # To make sure that org_switcher_button will be available
            self.goto()
            self.org_switcher_button.click()
            self.org_switcher_list.get_by_text(org_name).click()
            self.settings.click()
            self.delete_org_checkbox.click()
            self.delete_org_button.click()


class ExperimentsPage(CommonMixin, ExperimentsMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.condition = ExperimentCondition(self, self.add_criteria_button)
        self.feature = ExperimentFeature(self, self.add_action_button)

    def delete_all_experiments(self):
        for _ in range(self.delete_experiment_list.count()):
            self.delete_experiment_list.first.click()
            self.delete_experiment_confirm_button.click()

    def add_experiment(self, name: str, variants: list):
        self.add_experiment_button.click()
        for id, variant in enumerate(variants):
            self.variant_name_input(exp_id=0, var_id=id).fill(variant)
            self.variant_name_input(exp_id=0, var_id=id).press("Enter")
        self.experiment_name_input(id=0).fill(name)
        self.experiment_name_input(id=0).press("Enter")
        deploy_button = self.deploy_changes_button
        deploy_button.wait_for(timeout=10000)


class PropertyPage(CommonMixin, EnvironmentMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.condition = RuleCondition(self)
        self.feature = RuleFeature(self)
        self.nested_rule = NestedRules(self)

    def delete_all_rules(self):
        for _ in range(self.delete_rule_list.count()):
            self.delete_rule_list.first.click()
            self.delete_rule_button.click()

    def change_conditions_operator(self, value: str):
        self.condition_operator_list.last.click()
        self.select_operator_name(name=value).click()

    def set_conditions_operator_or(self):
        self.change_conditions_operator('or')

    def set_conditions_operator_and(self):
        self.change_conditions_operator('and')

    def revert_rules(self):
        try:
            # Click `Revert` button if available
            self.revert_button.click(timeout=4000)
            self.revert_changes_button.click(timeout=2000)
            self.wait_for_timeout(timeout=2000)
        except TimeoutError:
            pass


class SecurityPage(CommonMixin, SecurityMixin, BasePage):
    def _delete_rules(self, rules: list[(Page, str)], url_section: str) -> None:
        self.mock.clear()
        for rule in rules:
            url = f"{self.url.strip('/')}/security/{url_section}"
            self.goto(url)
            try:
                self.table.wait_for(timeout=10000)  # ms
            except TimeoutError:
                # Check if there is no rules present
                self.no_data_to_display.wait_for(timeout=500)  # ms
                return
            for row in self.table.tbody.tr:
                if row[0].text_content() == rule:
                    row[0].click()
                    self.delete_button.click()
                    self.confirm_button.click()
                    # Wait message on snackbar to change
                    self.client_snackbar.get_by_text('Successfully deleted').wait_for()
                    break

    def _open_rule_editor(self, url_section: str,
                          name: str, name_index: int = 0):
        # Make sure every dialog is closed - refresh page
        url = f"{self.url.strip('/')}/security/{url_section}"
        self.goto(url)
        self.table.wait_for()
        for row in self.table.tbody.tr:
            if row[name_index].text_content() == name:
                row[name_index].click()
                return True

        raise AssertionError("Rule was not saved")

    def delete_managed_rules(self, rules: list[str]):
        self._delete_rules(rules, 'managed_rules')

    def delete_access_rules(self, rules: list[str]):
        self._delete_rules(rules, 'access_rules')

    def delete_rate_rules(self, rules: list[str]):
        self._delete_rules(rules, 'rate_rules')

    def open_managed_rule_editor(self, name: str, name_index: int = 0):
        self._open_rule_editor('managed_rules', name, name_index)

    def open_access_rule_editor(self, name: str, name_index: int = 0):
        self._open_rule_editor('access_rules', name, name_index)

    def open_rate_rule_editor(self, name: str, name_index: int = 0):
        self._open_rule_editor('rate_rules', name, name_index)


class DeploymentsPage(CommonMixin, DeploymentsMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.last_deployed = self.table.tbody.tr[0][1]


class TrafficPage(CommonMixin, TrafficMixin, BasePage):
    pass


class RedirectsPage(CommonMixin, RedirectsMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

    def delete_all_redirects(self):
        self.delete_all_checkbox.first.set_checked(True)
        self.remove_selected_redirect.click()
        self.confirm_remove_redirect.click()

    def add_redirect(self, from_, to):
        self.add_a_redirect_button.click()
        self.redirect_from.fill('/' + from_)
        self.redirect_to.fill('/' + to)
        self.save_redirect_button.click()

    def csv_for_import(self, data_to_upload: list, headers=None):
        if headers is None:
            headers = ["from", "to", "status", "forwardQueryString"]
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(headers)
        csv_writer.writerows(data_to_upload)
        csv_buffer.seek(0)
        return csv_buffer

    def verify_exported_csv(self, csv_file_name, expected_content):
        with open(csv_file_name, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            actual_headers = next(csv_reader)

            # Compare headers
            if actual_headers != expected_content[0]:
                return False, f"{actual_headers} do not match the {expected_content}"

            # Compare data rows
            for row, actual_row_data in enumerate(csv_reader, start=0):
                if actual_row_data != expected_content[1][row]:
                    return False, print(f"Row {row} {actual_row_data} != {expected_content[1][row]} data.")
        # If no mismatches found, return True
        return True

    def upload_csv_file(self, file_obj: str, method_for_import=True):
        with self.expect_file_chooser() as fc_info:
            self.import_button.click()
            self.import_browse_button.click()
            # True for 'Override list with file content' option
            if method_for_import:
                self.import_override_existing.click()
            else:
                self.import_append_file.click()

        file_chooser = fc_info.value
        file_chooser.set_files(
            files=[{"name": "test.csv", "mimeType": "text/plain", "buffer": file_obj.read().encode('utf-8')}])
        self.upload_redirect_button.click()


class OriginsPage(CommonMixin, OriginsMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

    def delete_all_origins(self):
        for _ in range(self.delete_button_list.count()):
            self.delete_button_list.first.click()
            self.delete_origin_button_confirmation.click()

    def add_origin(self, name: str, override_host_header: str, origin_hostname: str, origins_number: int, row=0):
        # Only required fields are fulfilled
        self.add_origin_button.click()
        self.origin_name_field(origin=origins_number).fill(name)
        self.origin_hostname(origin=origins_number, row=row).fill(origin_hostname)
        self.origin_override_host_headers(origin=origins_number).fill(override_host_header)