from collections import defaultdict
from typing import Optional

from ltf2.console_app.magic.ruleconfig import RuleFeature, RuleCondition
from playwright.sync_api import Page


NESTED_RULE_ID_TMPL_PREFIX = 'droppable-rules.{rule}.ruleParts.{part}.'
NESTED_RULE_ID_TMPL_SUFFIX = 'nestedRules.{rule}.ruleParts.{part}.'

NESTED_RULE_ID_TMPL_FULL = '{id_prefix}nestedRules'


class NestedRule:
    """ Class for working with nested rule.

    Args:
        page: playwright Page instanse
        parent_index: parent rule number witch will be used in selector
            (data-rbd-droppable-id attribute)
        part: parent part number witch will be used in selector
            (data-rbd-droppable-id attribute)
        id_prefix: prefix of the data-rbd-droppable-id attribute
        index: rule number
    """
    def __init__(self,
                 page: Page,
                 parent_index: int,
                 part: int,
                 id_prefix: Optional[str] = None,
                 nrule_index: int = 0):
        self.page = page
        self.parent_index = parent_index
        self.id_prefix = id_prefix
        self.index = nrule_index
        self.child = 0

        if self.id_prefix is None:
            self.id_prefix = NESTED_RULE_ID_TMPL_PREFIX.format(rule=parent_index,
                                                               part=part)
        else:
            self.id_prefix += NESTED_RULE_ID_TMPL_SUFFIX.format(rule=parent_index,
                                                                part=part)
        self.nrule_id = NESTED_RULE_ID_TMPL_FULL.format(id_prefix=self.id_prefix)
        self.add_nrule_button = self.page.nested_rule_add_element_button(id=self.nrule_id,
                                                                         num=self.index + 1)
        self.condition = RuleCondition(page, self.add_nrule_button)
        self.feature = RuleFeature(page, self.add_nrule_button)

    def create_nested_rule(self, npart=0):
        self.add_nrule_button.click()
        self.page.select_rule_element(name='Add Nested Rule').click()

        nrule = NestedRule(self.page, self.index, npart, self.id_prefix, self.child)
        self.child += 1
        return nrule


class NestedRules:
    def __init__(self, page: Page):
        self.page = page
        # Count of nested rules in one rule
        self.counter = defaultdict(int)

    def create_nested_rule(self, rule=-1, part=0):
        if rule == -1:
            # Get last rule
            rule = self.page.rule_div.count() - 1

        self.page.rule_add_element_button(num=rule).click()
        self.page.select_rule_element(name='Add Nested Rule').click()

        nrule = NestedRule(self.page, rule, part, None, self.counter[(rule, part)])
        self.counter[(rule, part)] += 1
        return nrule
