"""
Classes that represent pages.

Each page should be inherited from mixins that describe the elements of the page
and BasePage class. Please note that the position of the mixins and BasePage is important
(BasePage should follow mixin) as super() follows the MRO.
"""
from playwright.sync_api import Page

from ltf2.console_app.magic.pages.components import (LoginMixin, TeamMixin, CommonMixin,
                                                     SecurityMixin, EnvironmentMixin)
from ltf2.console_app.magic.pages.base_page import BasePage
from ltf2.console_app.magic.ruleconfig import RuleFeature, RuleCondition


class LoginPage(CommonMixin, LoginMixin, BasePage):
    pass


class TeamPage(CommonMixin, TeamMixin, BasePage):
    pass


class PropertyPage(CommonMixin, EnvironmentMixin, BasePage):
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.condition = RuleCondition(self)
        self.feature = RuleFeature(self)

    def delete_all_rules(self):
        for _ in range(self.delete_rule_list.count()):
            self.delete_rule_list.first.click()
            self.delete_rule_button.click()


class SecurityPage(CommonMixin, SecurityMixin, BasePage):
    pass
