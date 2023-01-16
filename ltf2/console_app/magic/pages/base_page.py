import logging
import time
from collections import namedtuple, UserList

from ltf2.console_app.magic.elements import PageElement
from ltf2.console_app.magic.mock import GraphQLMock

from playwright.sync_api import Page


RespItem = namedtuple('RespItem', ['ts', 'url', 'status'])


def current_time():
    return int(time.time() * 1000)


class History(UserList):
    """Class for storing history info.

    Uses for simple filtering and searching through elements.

    Example:
        ...
        from ltf2.utils.comparators import contains
        items = history.get(url=contains('login'))
    """
    def get(self, **kwargs):
        return [h for h in self if h == kwargs]


class BasePage:
    """ Simple base class for pages.

    Call Page's method if it is not specified in this or a derived class.
    """
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        self.mock = GraphQLMock(page)
        self.request_history = History()
        self.response_history = History()
        self.page.on('response',
                     lambda res: self.response_history.append(
                         RespItem(current_time(), res.url, res.status)))
        self.log = logging.getLogger(self.__class__.__name__)

    def __getattr__(self, attr):
        if hasattr(self.page, attr):
            return getattr(self.page, attr)

    @property
    def page_url(self):
        return self.page.url

    def _set_element(self, element_type: PageElement, locator: str):
        return element_type(self.page, locator)

    def goto(self, url=None, **kwargs):
        self.log.info(f'Navigating to page: {url or self.url}')
        timeout = kwargs.pop('timeout', 30) * 1000
        self.page.goto(self.url if url is None else url, timeout=timeout, **kwargs)
