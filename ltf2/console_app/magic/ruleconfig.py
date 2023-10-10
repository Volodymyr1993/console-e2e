from __future__ import annotations

from playwright.sync_api import Page
from contextlib import contextmanager
from typing import Union, Optional, List

from ltf2.console_app.magic.elements import PageElement


CONDITIONS_MAP = {
    'asn': 'ASN',
    'brand_name': 'Brand Name',
    'city': 'City',
    'client_ip': 'Client IP',
    # 'continent': 'Continent',
    'cookie': 'Cookie',
    # 'country': 'Country',
    'directory': 'Directory',
    'dma_code': 'DMA Code',
    'dual_orientation': 'Dual Orientation',
    'extension': 'Extension',
    'filename': 'Filename',
    'html_preferred_dtd': 'HTML Preferred DTD',
    'image_inlining': 'Image Inlining',
    'is_android': 'Is Android',
    'is_app': 'Is App',
    'is_ios': 'Is iOS',
    'is_robot': 'Is Robot',
    'is_smartphone': 'Is Smartphone',
 #   'is_full_desktop': 'Is Full Desktop',
 #   'is_html_preferred': 'Is HTML Preferred',
 #   'is_largescreen': 'Is Largescreen',
 #   'is_mobile': 'Is Mobile',
    'is_smarttv': 'Is SmartTV',
    'is_tablet': 'Is Tablet',
    'is_touchscreen': 'Is Touchscreen',
    'is_windows_phone': 'Is Windows Phone',
    'is_wireless_device': 'Is Wireless Device',
    # 'is_wml_preferred': 'Is WML Preferred',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'marketing_name': 'Marketing Name',
    # 'method': 'Method',
    'metro_code': 'Metro Code',
    'mobile_browser': 'Mobile Browser',
    'model_name': 'Model Name',
    'origin_path': 'Origin Path',
    'path': 'Path',
 #   'pointing_method': 'Pointing Method',
    'pop_code': 'POP Code',
    'postal_code': 'Postal Code',
 #   'preferred_markup': 'Preferred Markup',
    'progressive_download': 'Progressive Download',
    'query': 'Query',
    'query_parameter': 'Query Parameter',
    'query_string': 'Query String',
    'random_integer': 'Random Integer',
    'referring_domain': 'Referring Domain',
    'region_code': 'Region Code',
    'release_date': 'Release Date',
    'request_header': 'Request Header',
    'resolution_height': 'Resolution Height',
    'resolution_width': 'Resolution Width',
    'response_status_code': 'Response Status Code',
    'scheme': 'Scheme',
 #   'ux_full_desktop': 'UX Full Desktop',
 #   'xhtml_support_level': 'XHTML Support Level',
}


MATCHES = 'matches regular expression'
DOES_NOT_MATCH = 'does not match regular expression'
MATCHES_SIMPLE = 'matches (simple)'


class RuleFeature:
    """ Class for work with Features in the Rule tab """
    def __init__(self,
                 page: Page,
                 add_feature_button: Optional[PageElement] = None):
        self.page = page
        self.add_feature_button = (self.page.add_element.last if add_feature_button is None
                                   else add_feature_button)

    @contextmanager
    def prepare_feature(self, feature: str):
        """ Setup page and save feature after creation """
        self.add_feature_button.click()
        self.page.select_rule_element(name='Add Feature').click()
        self.page.feature_input.click()
        self.page.get_by_text(feature, exact=True).last.click()
        try:
            yield
        except Exception:
            raise
        else:
            self.page.add_feature_button.click()

    # ============== Access

    def add_deny_access(self, enable: bool = True):
        with self.prepare_feature('Deny Access'):
            self.page.rule_checkbox.set_checked(enable)

    def add_token_auth(self, enable: bool = True):
        with self.prepare_feature('Token Auth'):
            self.page.rule_checkbox.set_checked(enable)

    def add_token_auth_ignore_url_case(self, enable: bool = True):
        with self.prepare_feature('Token Auth Ignore URL Case'):
            self.page.rule_checkbox.set_checked(enable)

    # ============== Caching

    def add_bandwidth_throttling(self, kbytes_per_second: int = 1024,
                                 prebuf_seconds: int = 0):
        with self.prepare_feature('Bandwidth Throttling'):
            self.page.kbytes_per_second.fill(str(kbytes_per_second))
            self.page.prebuf_seconds.fill(str(prebuf_seconds))

    def add_bypass_cache(self, enable: bool = True):
        with self.prepare_feature('Bypass Cache'):
            self.page.rule_checkbox.set_checked(enable)

    def add_cache_control_header_treatment(self, header_treatment: str = ''):
        with self.prepare_feature('Cache Control Header Treatment'):
            self.page.header_treatment_input.click()
            self.page.select_by_name(name=header_treatment).click()

    def add_bypass_client_cache(self, enable: bool = True):
        with self.prepare_feature('Bypass Client Cache'):
            self.page.rule_checkbox.set_checked(enable)

    def add_cache_key_query_string(self, option: str = '', value: str = '',
                                   enable: bool = True):
        with self.prepare_feature('Cache Key Query String'):
            self.page.option_input.click()
            self.page.select_by_name(name=option).click()
            if option == 'Include':
                self.page.include_input.fill(value)
                self.page.include_input.press('Enter')
            elif option == 'Include All Except':
                self.page.exclude_input.fill(value)
                self.page.exclude_input.press('Enter')
            else:
                self.page.rule_checkbox.set_checked(enable)

    def add_cacheable_request_body_size(self,
                                        cacheable_request_body_size: str = '100MB'):
        with self.prepare_feature('Cacheable Request Body Size'):
            self.page.cacheable_request_body_size.fill(
                str(cacheable_request_body_size))

    def add_cacheable_status_codes(self, value: int = 200):
        with self.prepare_feature('Cacheable Status Codes'):
            self.page.cacheable_status_codes.fill(str(value))
            self.page.cacheable_status_codes.press('Enter')

    def add_enable_caching_for_methods(self, post: str = '', put: str = ''):
        with self.prepare_feature('Enable Caching for Methods'):
            self.page.post_input.click()
            self.page.select_by_name(name=post).click()
            self.page.put_input.click()
            self.page.select_by_name(name=put).click()

    def add_enable_h264_encoding(self, h264_support: str = ''):
        with self.prepare_feature('Enable H264 encoding'):
            self.page.h264_support_input.fill(h264_support)

    def add_expires_header_treatment(self, expires_header_treatment: str = ''):
        with self.prepare_feature('Expires Header Treatment'):
            self.page.expires_header_treatment_input.click()
            self.page.select_by_name(name=expires_header_treatment).click()

    def add_honor_no_cache_request_header(self, enable: bool = True):
        with self.prepare_feature('Honor No Cache Request Header'):
            self.page.rule_checkbox.set_checked(enable)

    def add_ignore_origin_no_cache(self, value: int = 300):
        with self.prepare_feature('Ignore Origin No Cache'):
            self.page.ignore_origin_no_cache.fill(str(value))
            self.page.ignore_origin_no_cache.press('Enter')

    def add_ignore_unsatisfiable_ranges(self, enable: bool = True):
        with self.prepare_feature('Ignore Unsatisfiable Ranges'):
            self.page.rule_checkbox.set_checked(enable)

    def add_partial_cache_sharing_min_hit_size(self, value: int = 0):
        with self.prepare_feature('Partial Cache Sharing Min Hit Size'):
            self.page.feature_value_input.fill(str(value))

    def add_prevalidate_cached_content(self, value: int = 0, unit: str = ''):
        with self.prepare_feature('Prevalidate Cached Content'):
            self.page.duration_value.fill(str(value))
            self.page.duration_unit.click()
            self.page.select_by_name(name=unit).click()

    def add_refresh_zero_byte_cache_files(self, enable: bool = True):
        with self.prepare_feature('Refresh Zero Byte Cache Files'):
            self.page.rule_checkbox.set_checked(enable)

    def add_revalidate_after_origin_unavaliable(self, response_status_code: int = 200,
                                                value: int = 0, unit: str = ''):
        with self.prepare_feature('Revalidate After Origin Unavailable'):
            self.page.response_status_code.fill(str(response_status_code))
            self.page.max_age_value.fill(str(value))
            self.page.max_age_unit.click()
            self.page.select_by_name(name=unit).click()

    def add_revalidate_while_stale_timer(self, value: int = 0):
        with self.prepare_feature('Revalidate While Stale Timer'):
            self.page.feature_value_input.fill(str(value))

    def add_rewrite_cache_key(self, source: str = '', destination: str = '',
                              ignore_case: bool = True):
        with self.prepare_feature('Rewrite Cache Key'):
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)

    def add_set_client_max_age(self, value: int = 0, unit: str = ''):
        with self.prepare_feature('Set Client Max Age'):
            self.page.duration_value.fill(str(value))
            self.page.duration_unit.click()
            self.page.select_by_name(name=unit).click()

    def add_set_max_age(self, response_status_code: int = 200,
                        value: int = 0, unit: str = ''):
        with self.prepare_feature('Set Max Age'):
            self.page.response_status_code.fill(str(response_status_code))
            self.page.max_age_value.fill(str(value))
            self.page.max_age_unit.click()
            self.page.select_by_name(name=unit).click()

    def add_set_service_worker_max_age(self, value: int = 0,
                                       unit: str = ''):
        with self.prepare_feature('Set Service Worker Max Age'):
            self.page.service_worker_max_age_value.fill(str(value))
            self.page.service_worker_max_age_unit.click()
            self.page.select_by_name(name=unit).click()

    def add_stale_on_error(self, enable: bool = True):
        with self.prepare_feature('Stale On Error'):
            self.page.rule_checkbox.set_checked(enable)

    def add_stale_while_revalidate(self, value: int = 0, unit: str = ''):
        with self.prepare_feature('Stale While Revalidate'):
            self.page.duration_value.fill(str(value))
            self.page.duration_unit.click()
            self.page.select_by_name(name=unit).click()

    # ============== Headers

    def add_set_response_headers(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Set Response Headers'):
            self.page.header_name.fill(header_name)
            self.page.value_div.fill(header_value)

    def add_debug_header(self, enable: bool = True):
        with self.prepare_feature('Debug Header'):
            self.page.rule_checkbox.set_checked(enable)

    def add_remove_origin_response_headers(self, header_name: str = ''):
        with self.prepare_feature('Remove Origin Response Headers'):
            self.page.origin_response_headers.fill(header_name)
            self.page.origin_response_headers.press('Enter')

    def add_remove_response_headers(self, header_name: str = ''):
        with self.prepare_feature('Remove Response Headers'):
            self.page.response_headers.fill(header_name)
            self.page.response_headers.press('Enter')

    def add_server_timing_header(self, enable: bool = True):
        with self.prepare_feature('Server-Timing Header'):
            self.page.rule_checkbox.set_checked(enable)

    def add_set_client_ip_custom_header(self, header_name: str = ''):
        with self.prepare_feature('Set Client IP Custom Header'):
            self.page.feature_value_input.fill(header_name)

    def add_set_request_headers(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Set Request Headers'):
            self.page.header_name.fill(header_name)
            self.page.value_div.fill(header_value)

    def add_add_response_headers(self, header_name: str = '', header_value: str = ''):
        with self.prepare_feature('Add Response Headers'):
            self.page.header_name.fill(header_name)
            self.page.value_div.fill(header_value)

    # ========== Logs

    def add_custom_log_field(self, custom_log_field: str = ''):
        with self.prepare_feature('Custom Log Field'):
            self.page.custom_log_field.fill(custom_log_field)

    def add_log_query_string(self, enable: bool = True):
        with self.prepare_feature('Log Query String'):
            self.page.rule_checkbox.set_checked(enable)

    def add_mask_client_subnet(self, enable: bool = True):
        with self.prepare_feature('Mask Client Subnet'):
            self.page.rule_checkbox.set_checked(enable)

    # =========== Origins

    def add_max_keep_alive_requests(self, value: int = 0):
        with self.prepare_feature('Max Keep-Alive Requests'):
            self.page.feature_value_input.fill(str(value))

    def add_proxy_special_headers(self, value: Optional[Union[list, str]] = ''):
        with self.prepare_feature('Proxy Special Headers'):
            if isinstance(value, list):
                for v in value:
                    self.page.proxy_special_headers_input.fill(v)
                    self.page.proxy_special_headers_input.press('Enter')
            else:
                self.page.proxy_special_headers_input.fill(value)
                self.page.proxy_special_headers_input.press('Enter')

    def add_set_origin(self, value: str):
        with self.prepare_feature('Set Origin'):
            self.page.set_origin_input.click()
            self.page.select_by_name(name=value).click()

    # ============= Response

    def add_allow_prefetching_of_uncached_content(self, enable: bool = True):
        with self.prepare_feature('Allow Prefetching of Uncached Content'):
            self.page.rule_checkbox.set_checked(enable)

    # def add_compress_content_types(self, types: str = ''):
    #     with self.prepare_feature('Compress Content Types'):
    #         self.page.compress_content_types_input.fill(types)
    #         self.page.compress_content_types_input.press('Enter')

    def add_set_done(self, enable: bool = True):
        with self.prepare_feature('Set Done'):
            self.page.rule_checkbox.set_checked(enable)

    def add_set_response_body(self, body: str = ''):
        with self.prepare_feature('Set Response Body'):
            self.page.response_body.fill(body)

    def add_set_status_code(self, code: int = 200):
        with self.prepare_feature('Set Status Code'):
            self.page.feature_value_input.fill(str(code))

    # ============ Set Variable

    def add_set_variables(self, name: str = '', value: str = ''):
        with self.prepare_feature('Set Variables'):
            self.page.variable_name.fill(name)
            self.page.variable_value.fill(value)

    # ============ URL

    def add_follow_redirects(self, enable: bool = True):
        with self.prepare_feature('Follow Redirects'):
            self.page.rule_checkbox.set_checked(enable)

    def add_url_redirect(self, code: int = 302, source: str = '',
                         destination: str = '', ignore_case: bool = False):
        with self.prepare_feature('URL Redirect'):
            # TODO uncomment when bug with Status code is fixed
            # self.page.code_input.fill(str(code))
            self.page.rule_checkbox.set_checked(ignore_case)
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)

    def add_rewrite_url(self, source: str = '', destination: str = '',
                        match_style: str = 'simple', ignore_case: bool = False):
        with self.prepare_feature('Rewrite URL'):
            self.page.source_input.fill(source)
            self.page.destination_input.fill(destination)
            self.page.match_style_input.click()
            self.page.select_by_name(name=match_style).click()
            if match_style == 'regexp':
                self.page.rule_checkbox.set_checked(ignore_case)


class RuleCondition:
    """ Class for work with Conditions in the Rule tab """

    def __init__(self,
                 page: Page,
                 add_condition_button: Optional[PageElement] = None):
        self.page = page
        self.add_condition_button = (self.page.add_element.last if add_condition_button is None
                                   else add_condition_button)

    def __getattr__(self, item):
        if item.startswith('add_'):
            _, method = item.split('_', 1)
            if method in CONDITIONS_MAP:
                return lambda *args, **kwargs: \
                    self.set_condition(CONDITIONS_MAP[method], *args, **kwargs)
            raise AttributeError(
                f'{self.__class__} does not have {item} attribute')

    @contextmanager
    def prepare_condition(self, condition: str):
        self.add_condition_button.click()
        self.page.select_rule_element(name='Add Condition').click()
        self.page.variable_input.click()
        self.page.variable_select(name=condition).click()
        try:
            yield
        except Exception:
            raise
        else:
            self.page.add_condition_button.click()

    def set_condition(self,
                      method: str = '',
                      operator: str = '',
                      value: Optional[Union[str, float, List[str]]] = None,
                      ignore_case: bool = False,
                      name: Optional[str] = None,
                      number: Optional[int] = None):
        with self.prepare_condition(method):
            if operator == '' and value:
                if value == 'no':
                    self.page.rule_checkbox.set_checked(False)
                elif value == 'yes':
                    self.page.rule_checkbox.set_checked(True)
                # self.page.match_value_input.click()
                # self.page.select_by_name(name=value).click()
                return
            if name:
                self.page.name_input.fill(name)
            if number is not None:
                self.page.number_input.fill(str(number))
            self.page.operator_input.click()
            self.page.select_by_name(name=operator).click()
            if operator in ('is one of', 'is not one of'):
                if isinstance(value, str):
                    value = [value]
                for v in value:
                    self.page.match_value_input.fill(str(v))
                    self.page.match_value_input.press('Enter')
            elif 'less than' in operator or \
                    'greater than' in operator:
                self.page.match_value_input.fill(str(value))
            else:
                self.page.value_div.fill(value)
                if operator in (MATCHES, DOES_NOT_MATCH):
                    self.page.rule_checkbox.set_checked(ignore_case)

    # TODO refactor the following methods
    def add_scheme(self,
                   operator: str = '',
                   value: Optional[Union[str, float]] = None,
                   ignore_case: bool = False):
        with self.prepare_condition('Scheme'):
            self.page.operator_input.click()
            self.page.select_by_name(name=operator).click()
            if operator in (MATCHES, DOES_NOT_MATCH, MATCHES_SIMPLE):
                self.page.value_div.fill(value)
                if operator == MATCHES_SIMPLE: return
                self.page.rule_checkbox.set_checked(ignore_case)
            else:
                self.page.match_value_input.click()
                self.page.select_by_name(name=value).click()

    def add_method(self,
                   operator: str = '',
                   value: Optional[Union[str, float]] = None,
                   ignore_case: bool = False):
        with self.prepare_condition('Method'):
            self.page.operator_input.click()
            self.page.select_by_name(name=operator).click()
            if operator in (MATCHES, DOES_NOT_MATCH):
                self.page.value_div.fill(value)
                self.page.rule_checkbox.set_checked(ignore_case)
            else:
                self.page.match_value_input.click()
                self.page.select_by_name(name=value).click()

    def add_country(self,
                    operator: str = '',
                    value: Optional[Union[str, List[str]]] = None):
        with self.prepare_condition('Country'):
            self.page.operator_input.click()
            self.page.select_by_name(name=operator).click()
            if isinstance(value, str):
                value = [value]
            for v in value:
                self.page.match_value_input.click()
                self.page.select_by_name(name=v).click()

    def add_continent(self,
                      operator: str = '',
                      value: Optional[Union[str, List[str]]] = None):
        with self.prepare_condition('Continent'):
            self.page.operator_input.click()
            self.page.select_by_name(name=operator).click()
            if isinstance(value, str):
                value = [value]
            for v in value:
                self.page.match_value_input.click()
                self.page.select_by_name(name=v).click()


class ExperimentFeature(RuleFeature):
    @contextmanager
    def prepare_feature(self, feature: str):
      self.add_feature_button.click()
      self.page.feature_input.click()
      self.page.get_by_text(feature, exact=True).last.click()
      try:
        yield
      except Exception:
        raise
      else:
        self.page.add_feature_confirm_button.click()


class ExperimentCondition(RuleCondition):
    @contextmanager
    def prepare_condition(self, condition: str):
      self.add_condition_button.click()
      self.page.variable_input.click()
      self.page.variable_select(name=condition).click()
      try:
        yield
      except Exception:
        raise
      else:
        self.page.add_condition_button.click()