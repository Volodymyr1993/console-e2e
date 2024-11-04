from __future__ import annotations

from playwright.sync_api import Page
from typing import Type, List
import logging


class PageElement:
    """ Base parent-class for all elements """
    def __init__(self, page: Page, selector: str):
        self.page = page
        self.selector = selector
        self._locator = self.page.locator(selector)
        self.log = logging.getLogger(self.__class__.__name__)

    def __getattr__(self, attr: str):
        if hasattr(self._locator, attr):
            self.log.debug(f'Doing `{attr}` to: `{self.selector}`')
            return getattr(self._locator, attr)

    def __dir__(self) -> List[str]:
        """Include methods from self._locator in dir() output"""
        return sorted(set(dir(type(self)) + list(self.__dict__.keys()) + dir(self._locator)))


class IframeElement(PageElement):
    def __init__(self, iframe, selector: str):
        super().__init__(iframe, selector)
        self._locator = self.page.frame_locator(':scope').locator(selector)


class DynamicPageElement:
    """ Factory for creating elements using selector pattern

    Used when elements are created at runtime and have the same selector pattern.

    Example:
        dynamic_input = DynamicPageElement(page,
                                          'input[name="conditionGroups[{group}].type"]')

        # Create PageElement with selector 'input[name="conditionGroups[1].type"]'
        input1 = dynamic_input(group=1)
        # Work with input element
        input1.fill('value')
        ...
        # Create PageElement with selector 'input[name="conditionGroups[2].type"]'
        input2 = dynamic_input(group=2)

    """
    def __init__(self,
                 page: Page,
                 pattern: str,
                 element_type: Type[PageElement] = PageElement):
        self.page = page
        self.pattern = pattern
        self.element_type = element_type

    def __call__(self, *args, **kwargs):
        return self.element_type(self.page,
                                 self.pattern.format(*args, **kwargs))


class DynamicIndexElement(DynamicPageElement):
    """ Dynamic index element.

    Substitute index in XPATH selector pattern

    1. Add +1 to index
    2. Replace -1 index with 'last()' XPATH method
    """
    def __call__(self, *args, **kwargs):
        new_args = []
        for arg in args:
            new_args.append('last()' if arg == -1 else arg + 1)
        new_kwargs = {}
        for k, v in kwargs.items():
            new_kwargs.update({k: 'last()' if v == -1 else v + 1})
        return self.element_type(self.page,
                                 self.pattern.format(*new_args, **new_kwargs))


class DynamicSelectElement(DynamicPageElement):
    """
    Dynamic select element.

    Check if the select element contains passed value.
    """
    def verify_select(self, value):
        available_values = self.page.locator(
            self.pattern.rsplit('/', 1)[0]).inner_text().split('\n')
        if value not in available_values:
            raise ValueError(
                f'Wrong value `{value}`. Available: {available_values}')

    def __call__(self, *args, **kwargs):
        # Argument is Select value to click, so verify it
        select_value = args or list(kwargs.values())
        if len(select_value) == 1:
            self.verify_select(select_value[0])

        return super().__call__(*args, **kwargs)


class DynamicRateConditions(DynamicPageElement):
    def __call__(self, group, condition):
        return super().__call__(group=group, condition=condition+1)


class ListElement(PageElement):
    """ Class for describing an element that is composed of other elements. """
    def __init__(self, page: Page, selector: str):
        super().__init__(page, selector)
        self._curr_item = 0
        self._count = 0

    def __len__(self):
        return self.count()

    def __getitem__(self, index: int):
        return self.nth(index)

    def __iter__(self):
        self._count = self.count()
        self._curr_item = 0
        while self._curr_item < self._count:
            yield self[self._curr_item]
            self._curr_item += 1


class UlElement(PageElement):
    def __init__(self, page: Page, selector: str):
        super().__init__(page, selector)
        self.li = ListElement(page, f'{selector}/li')


# ============= Table ============================


class TdElements(ListElement):
    pass


class TrElements(ListElement):
    """ Class for describing a tr element of a table. """
    def __init__(self,
                 td_type: PageElement,
                 page: Page,
                 selector: str):
        super().__init__(page, selector)
        self.td_type = td_type

    def __getitem__(self, index: int):
        return self.td_type(self.page,
                            f'{self.selector}[{index + 1}]/td')


class TbodyElement(PageElement):
    """ Class for describing tbody of table element. """
    def __init__(self,
                 page: Page,
                 selector: str,
                 tr_type: PageElement,
                 td_type: PageElement):
        super().__init__(page, selector)
        self.tr = tr_type(td_type, page, f'{selector}/tr')


class TheadElement(PageElement):
    """ Class for describing table headers elements. """
    def __init__(self, page: Page, selector: str):
        super().__init__(page, selector)
        self.th = ListElement(page, f'{selector}/tr/th')


class TableElement(PageElement):
    """ Class for describing HTML table """
    def __init__(self, page: Page, selector: str):
        super().__init__(page, selector)
        self.thead = TheadElement(page, f'{selector}/thead')
        self.tbody = TbodyElement(page, f'{selector}/tbody', TrElements, TdElements)


class MembersTableElement(PageElement):
    class TdMembersElement(TdElements):
        def __init__(self, page: Page, selector: str):
            super().__init__(page, selector)
            self.member_checkbox = self[0].locator('input[type="checkbox"]')
            self.resend_email_button = self[2].locator('button', has_text="Resend Email")
            self.username = self[3]
            self.role = self[4]

    def __init__(self, page: Page, selector: str):
        super().__init__(page, selector)
        self.thead = TheadElement(page, f'{selector}/thead')
        self.tbody = TbodyElement(page, f'{selector}/tbody',
                                  TrElements, MembersTableElement.TdMembersElement)


class CreatedRuleElement:
    def __init__(self, page: Page, condition_selector: str, feature_selector: str):
        self.page = page
        self.condition_selector = condition_selector
        self.feature_selector = feature_selector
        self.log = logging.getLogger(self.__class__.__name__)

    def __call__(self, num=None):
        rule_num = 'last()' if num == -1 else num + 1
        for attr in ('condition', 'feature'):
            selector = getattr(self, f'{attr}_selector').format(rule_num=rule_num)
            setattr(self, attr, DynamicIndexElement(self.page, selector))
        return self
