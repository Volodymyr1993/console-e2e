"""
Classes that represent pages.

Each page should be inherited from mixins that describe the elements of the page
and BasePage class. Please note that the position of the mixins and BasePage is important
(BasePage should follow mixin) as super() follows the MRO.
"""

from ltf2.console_app.magic.pages.components import (LoginMixin, TeamMixin, CommonMixin,
                                                     SecurityMixin, EnvironmentMixin)
from ltf2.console_app.magic.pages.base_page import BasePage


class LoginPage(CommonMixin, LoginMixin, BasePage):
    pass


class TeamPage(CommonMixin, TeamMixin, BasePage):
    pass


class PropertyPage(CommonMixin, EnvironmentMixin, BasePage):
    pass


class SecurityPage(CommonMixin, SecurityMixin, BasePage):
    pass
