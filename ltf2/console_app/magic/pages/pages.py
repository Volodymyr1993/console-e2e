"""
Classes that represent pages.

Each page should be inherited from mixins that describe the elements of the page
and BasePage class. Please note that the position of the mixins and BasePage is important
(BasePage should follow mixin) as super() follows the MRO.
"""
from playwright.sync_api import Page

from ltf2.console_app.magic.pages.components import (LoginMixin, OrgMixin, CommonMixin,
                                                     SecurityMixin, EnvironmentMixin,
                                                     DeploymentsMixin, ExperimentsMixin,
                                                     TrafficMixin)

from ltf2.console_app.magic.pages.base_page import BasePage
from ltf2.console_app.magic.ruleconfig import RuleFeature, RuleCondition, ExperimentCondition, ExperimentFeature
from ltf2.console_app.magic.nested_rules import NestedRules


class LoginPage(CommonMixin, LoginMixin, BasePage):
    pass


class OrgPage(CommonMixin, OrgMixin, BasePage):
    pass


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


class SecurityPage(CommonMixin, SecurityMixin, BasePage):
    pass


class DeploymentsPage(CommonMixin, DeploymentsMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.last_deployed = self.table.tbody.tr[0][1]


class TrafficPage(CommonMixin, TrafficMixin, BasePage):
    pass