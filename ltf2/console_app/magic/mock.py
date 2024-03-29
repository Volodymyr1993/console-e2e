import json
import logging
import time
from typing import Optional, Callable

from playwright.sync_api import Page


def match_dicts(first: dict, second: dict) -> bool:
    """ Check if the first dict is a subdict of the second """
    for key, val in first.items():
        if isinstance(val, dict):
            if not match_dicts(first[key], second[key]):
                return False
        else:
            # Plain dict
            if first[key] == second.get(key):
                continue
            else:
                return False
    return True


class GraphQLMock:
    """ Class for mocking graphql requests """
    def __init__(self, page: Page, delay: float = 0):
        self.page = page
        self.delay = delay
        self.schedules = []
        self.page.route("**/graphql", self.handle_route)
        self.log = logging.getLogger(self.__class__.__name__)

    def schedule(self,
                 match: dict = {},
                 status: int = 200,
                 headers: Optional[dict] = None,
                 body_json: Optional[dict] = None,
                 body: Optional[str] = None,
                 delay: Optional[float] = None) -> None:
        """ Schedule response on mock for specified request

        Support comparators.

        Example:
            from ltf2.util import comparators as cmp

            mock.schedule(match={'variables': {'path': cmp.contains('/waf'),
                                               'params': {'field': cmp.re_match('acl_*')}}}),
                          status=204,
                          body_json={"data":{"edgeInsights":{"results":..}}})
        """
        response = dict(status=status,
                        headers=headers,
                        body=json.dumps(body_json) if body_json else body)
        self.schedules.insert(0, (match, response, delay))

    def handle_route(self, route: Callable):
        """ Handle all requests on /graphql """
        self.log.debug(f'>> {route.request.post_data_json}')
        for expected_request, response, delay in self.schedules:
            if match_dicts(expected_request, route.request.post_data_json):
                self.log.debug(f'<< Scheduled response: {response}')
                time.sleep(self.delay if delay is None else delay)
                route.fulfill(**response)
                break
        else:
            route.continue_()

    def clear(self):
        """ Clear all schedules """
        self.schedules = []
