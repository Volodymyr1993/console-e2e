from __future__ import annotations
from random import randint, choice
import string

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError


QUERY_STR_SECURITY_SECTION = '?tab=security&section='


def random_str(n: int) -> str:
    return ''.join([choice(string.ascii_lowercase) for _ in range(n)])


def random_int(n: int) -> str:
    return ''.join([str(randint(1, 9))] + [str(randint(0, 9)) for _ in range(n - 1)])


def mock_frame_request(page: Page) -> Page:
    page.route("*/embed/frame",
               lambda route: route.fulfill(status=200,
                                           body=''))
    return page
