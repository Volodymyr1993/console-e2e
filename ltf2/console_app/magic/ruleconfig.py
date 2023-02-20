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
            yield


class UrlCreator(FeatureCreator):

    feature = 'URL'

    def follow_redirects(self, enable: bool = True):
        with self.prepare_feature('Follow Redirects'):
            self.page.rule_checkbox.set_checked(enable)

    def url_redirect(self, code: int = 302, source: str = '',
                     destination: str = '', ignore_case: bool = False):
        with self.prepare_feature('URL Redirect'):
            # TODO uncomment when bug with Status code is fixed
            # self.page.code_input.fill(str(code))
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)

    def url_rewrite(self, source: str = '', destination: str = '',
                    ignore_case: bool = False):
        with self.prepare_feature('URL Rewrite'):
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)


class HeaderCreator(FeatureCreator):

    feature = 'Headers'

    def set_response_headers(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Set Response Headers'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)

    def add_response_headers(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Add Response Headers'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)

    def set_request_headers(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Set Request Headers'):
            self.page.header_name.fill(header_name)
            self.page.header_value.fill(header_value)

    def debug_header(self, enable: bool = True):
        with self.prepare_feature('Debug Header'):
            self.page.rule_checkbox.set_checked(enable)

    def remove_origin_response_headers(self, header_name: str = ''):
        with self.prepare_feature('Remove Origin Response Headers'):
            self.page.origin_response_headers.fill(header_name)
            self.page.origin_response_headers.press('Enter')

    def remove_response_headers(self, header_name: str = ''):
        with self.prepare_feature('Remove Response Headers'):
            self.page.response_headers.fill(header_name)
            self.page.response_headers.press('Enter')


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

    def cacheable_request_body_size(self, cacheable_request_body_size: str = '100MB'):
        with self.prepare_feature('Cacheable Request Body Size'):
            self.page.cacheable_request_body_size.fill(str(cacheable_request_body_size))

    def compress_file_types(self, compress_file_types: str = ''):
        with self.prepare_feature('Compress File Types'):
            self.page.compress_file_types_input.fill(compress_file_types)
            self.page.compress_file_types_input.press('Enter')

    def enable_caching_for_methods(self, post: str = '', put: str = ''):
        with self.prepare_feature('Enable Caching for Methods'):
            self.page.post_input.click()
            self.page.select_by_name(name=post).click()
            self.page.put_input.click()
            self.page.select_by_name(name=put).click()

    def enable_h264_encoding(self, h264_support: str = ''):
        with self.prepare_feature('Enable H264 encoding'):
            self.page.h264_support_input.fill(h264_support)

    def expires_header_treatment(self, expires_header_treatment: str = ''):
        with self.prepare_feature('Expires Header Treatment'):
            self.page.expires_header_treatment_input.click()
            self.page.select_by_name(name=expires_header_treatment).click()

    def external_max_age(self, value: int = 0, unit: str = ''):
        with self.prepare_feature('External Max Age'):
            self.page.duration_value.fill(str(value))
            self.page.duration_unit.click()
            self.page.select_by_name(name=unit).click()

    def force_internal_max_age(self, response_status_code: int = 200,
                               value: int = 0, unit: str = ''):
        with self.prepare_feature('Force Internal Max Age'):
            self.page.response_status_code.fill(str(response_status_code))
            self.page.max_age_value.fill(str(value))
            self.page.max_age_unit.click()
            self.page.select_by_name(name=unit).click()

    def honor_no_cache_request(self, enable: bool = True):
        with self.prepare_feature('Honor No Cache Request'):
            self.page.rule_checkbox.set_checked(enable)

    def ignore_origin_no_cache(self, value: int = 300):
        with self.prepare_feature('Ignore Origin No Cache'):
            self.page.ignore_origin_no_cache.fill(str(value))
            self.page.ignore_origin_no_cache.press('Enter')

    def ignore_unsatisfiable_ranges(self, enable: bool = True):
        with self.prepare_feature('Ignore Unsatisfiable Ranges'):
            self.page.rule_checkbox.set_checked(enable)

    def internal_max_stale(self, response_status_code: int = 200,
                           value: int = 0, unit: str = ''):
        with self.prepare_feature('Internal Max Stale'):
            self.page.response_status_code.fill(str(response_status_code))
            self.page.max_age_value.fill(str(value))
            self.page.max_age_unit.click()
            self.page.select_by_name(name=unit).click()

    def partial_cache_sharing_min_hit_size(self, value: int = 0):
        with self.prepare_feature('Partial Cache Sharing Min Hit Size'):
            self.page.partial_cache_sharing_min_hit_size.fill(str(value))

    def prevalidate_cached_content(self, value: int = 0, unit: str = ''):
        with self.prepare_feature('Prevalidate Cached Content'):
            self.page.duration_value.fill(str(value))
            self.page.duration_unit.click()
            self.page.select_by_name(name=unit).click()

    def refresh_zero_byte_cache_files(self, enable: bool = True):
        with self.prepare_feature('Refresh Zero Byte Cache Files'):
            self.page.rule_checkbox.set_checked(enable)

    def revalidate_while_stale(self, enable: bool = True):
        with self.prepare_feature('Revalidate While Stale'):
            self.page.rule_checkbox.set_checked(enable)

    def rewrite_cache_key(self, source: str = '', destination: str = '',
                          ignore_case: bool = True):
        with self.prepare_feature('Rewrite Cache Key'):
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)

    def set_cacheable_status_codes(self, value: int = 200):
        with self.prepare_feature('Set Cacheable Status Codes'):
            self.page.set_cacheable_status_codes.fill(str(value))
            self.page.set_cacheable_status_codes.press('Enter')

    def stale_content_delivery_on_error(self, enable: bool = True):
        with self.prepare_feature('Stale Content Delivery On Error'):
            self.page.rule_checkbox.set_checked(enable)

    def stale_while_revalidate(self, value: int = 0, unit: str = ''):
        with self.prepare_feature('Stale While Revalidate'):
            self.page.duration_value.fill(str(value))
            self.page.duration_unit.click()
            self.page.select_by_name(name=unit).click()


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


class RuleCondition:
    """ Class for work with Conditions in the Rule tab """
    def __init__(self, page):
        self.page = page

    def add_path(self, operator='Matches', value=''):
        self.page.add_condition.last.click()
        self.page.variable_input.click()
        self.page.variable_select(name='Path').click()
        self.page.operator_input.click()
        self.page.select_by_name(name=operator).click()
        self.page.match_value.fill(value)
        self.page.add_condition_button.click()