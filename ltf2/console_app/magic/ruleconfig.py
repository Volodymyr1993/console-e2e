from __future__ import annotations
from playwright.sync_api import Page
from contextlib import contextmanager


class FeatureCreator:

    feature = None

    def __init__(self, page: Page):
        self.page = page

    @contextmanager
    def prepare_feature_type(self):
        """ Setup page and save feature after creation """
        self.page.add_feature.last.click()
        self.page.feature_type_input.click()
        self.page.select_by_name(name=self.feature).click()
        try:
            yield
        except Exception:
            raise
        else:
            self.page.add_feature_button.click()

    @contextmanager
    def prepare_feature(self, feature: str):
        with self.prepare_feature_type():
            self.page.feature_input.click()
            self.page.select_by_name(name=feature).click()
            breakpoint()
            yield


class UrlCreator(FeatureCreator):

    feature = 'URL'

    def follow_redirects(self, enable: bool = True):
        with self.prepare_feature('Follow Redirects'):
            self.page.rule_checkbox.set_checked(enable)

    def url_redirect(self, code: int = 302, source: str = '',
                     destination: str = '', ignore_case: bool = True):
        with self.prepare_feature('URL Redirect'):
            # TODO uncomment when bug with Status code is fixed
            # self.page.code_input.fill(str(code))
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)

    def url_rewrite(self, source: str = '', destination: str = '',
                    ignore_case: bool = True):
        with self.prepare_feature('URL Rewrite'):
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)


class HeaderCreator(FeatureCreator):

    feature = 'Headers'

    def set_response_header(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Set Response Header'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)

    def add_response_header(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Add Response Header'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)

    def set_request_header(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Set Request Header'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)

    def debug_header(self, enable: bool = True):
        with self.prepare_feature('Debug Header'):
            self.page.rule_checkbox.set_checked(enable)

    def remove_origin_response_headers(self, header_name: str = ''):
        with self.prepare_feature('Remove Origin Response Headers'):
            self.page.origin_response_headers.fill(header_name)

    def remove_response_headers(self, header_name: str = ''):
        with self.prepare_feature('Remove Response Headers'):
            self.page.response_headers.fill(header_name)


class SetVariablesCreator(FeatureCreator):

    feature = 'Set Variables'

    def __call__(self, name: str = '', value: str = ''):
        with self.prepare_feature_type():
            self.page.variable_name.fill(name)
            self.page.variable_value.fill(value)


class AccessCreator(FeatureCreator):

    feature = 'Access'
    available_features = {
        'deny_access': 'Deny Access',
        'token_auth': 'Token Auth',
        'token_auth_ignore_url_case': 'Token Auth Ignore URL Case'
    }

    def __getattr__(self, item):
        if item in self.available_features:
            return lambda *args, **kwargs: self.add_access(self.available_features[item],
                                                           *args,
                                                           **kwargs)

    def add_access(self, feature: str = '', enable: bool = True):
        with self.prepare_feature(feature):
            self.page.rule_checkbox.set_checked(enable)


class LogsCreator(FeatureCreator):

    feature = 'Logs'

    def custom_log_field(self, custom_log_field: str = ''):
        with self.prepare_feature('Custom Log Field'):
            self.page.custom_log_field.fill(custom_log_field)

    def log_query_string(self, enable: bool = True):
        with self.prepare_feature('Log Query String'):
            self.page.rule_checkbox.set_checked(enable)

    def mask_client_subnet(self, enable: bool = True):
        with self.prepare_feature('Mask Client Subnet'):
            self.page.rule_checkbox.set_checked(enable)


class ResponseCreator(FeatureCreator):

    feature = 'Response'

    def set_status_code(self, code: int = 200):
        with self.prepare_feature('Set Status Code'):
            self.page.status_code_input.fill(str(code))

    def set_done(self, enable: bool = True):
        with self.prepare_feature('Set Done'):
            self.page.rule_checkbox.set_checked(enable)

    def set_response_body(self, body: str = '',):
        with self.prepare_feature('Set Response Body'):
            self.page.response_body.fill(body)

    def allow_prefetching_of_uncached_content(self, enable: bool = True):
        with self.prepare_feature('Allow Prefetching of Uncached Content'):
            self.page.rule_checkbox.set_checked(enable)


class CachingCreator(FeatureCreator):

    feature = 'Caching'

    def bandwidth_parameters(self, enable: bool = True):
        with self.prepare_feature('Bandwidth Parameters'):
            self.page.rule_checkbox.set_checked(enable)

    def bypass_cache(self, enable: bool = True):
        with self.prepare_feature('Bypass Cache'):
            self.page.rule_checkbox.set_checked(enable)

    def bandwidth_throttling(self, kbytes_per_second: int = 1024,
                             prebuf_seconds: int = 0):
        with self.prepare_feature('Bandwidth Throttling'):
            self.page.kbytes_per_second.fill(str(kbytes_per_second))
            self.page.prebuf_seconds.fill(str(prebuf_seconds))

    def cache_control_header_treatment(self, header_treatment: str = ''):
        with self.prepare_feature('Cache Control Header Treatment'):
            self.page.header_treatment_input.click()
            self.page.select_by_name(name=header_treatment).click()

    def cache_key_query_string(self, option: str = '', value: str = '',
                               enable: bool = True):
        with self.prepare_feature('Cache Key Query String'):
                self.page.option_input.click()
                self.page.select_by_name(name=option).click()
                if option == 'Include':
                    self.page.include_input.fill(value)
                elif option == 'Exclude':
                    self.page.exclude_input.fill(value)
                else:
                    self.page.rule_checkbox.set_checked(enable)


class RuleFeature:
    """ Class for work with Features in the Rule tab """
    def __init__(self, page):
        self.page = page
        self.add_url = UrlCreator(self.page)
        self.add_headers = HeaderCreator(self.page)
        self.add_set_variable = SetVariablesCreator(self.page)
        self.add_access = AccessCreator(self.page)
        self.add_logs = LogsCreator(self.page)
        self.add_response = ResponseCreator(self.page)
        self.add_caching = CachingCreator(self.page)
