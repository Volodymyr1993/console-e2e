"""
Classes that represent pages.

Each page should be inherited from mixins that describe the elements of the page
and BasePage class. Please note that the position of the mixins and BasePage is important
(BasePage should follow mixin) as super() follows the MRO.
"""
from __future__ import annotations

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError

from ltf2.console_app.magic.nested_rules import NestedRules
from ltf2.console_app.magic.pages.base_page import BasePage
from ltf2.console_app.magic.pages.components import (CommonMixin,
                                                     DeploymentsMixin,
                                                     EnvironmentMixin,
                                                     ExperimentsMixin,
                                                     LoginMixin, OrgMixin,
                                                     SecurityMixin,
                                                     TrafficMixin)
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

    def deploy_changes(self):
        self.deploy_changes_button.last.click()
        self.wait_for_timeout(timeout=1000)
        self.deploy_changes_button.last.click()
        # wait for success message
        message = self.client_snackbar.get_by_text(
            'Changes deployed successfully')
        message.first.wait_for(timeout=40000)
        return message.first


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


class DeploymentsPage(CommonMixin, DeploymentsMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.last_deployed = self.table.tbody.tr[0][1]


class TrafficPage(CommonMixin, TrafficMixin, BasePage):
    pass