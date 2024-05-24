"""
Classes that describe page elements
"""
import time
from itertools import product

from playwright._impl import _errors
from playwright.sync_api import Page, expect

from ltf2.console_app.magic.constants import ACCESS_CONTROL_TYPE, HTTP_METHODS
from ltf2.console_app.magic.elements import PageElement, UlElement, MembersTableElement, \
    TableElement, ListElement, DynamicPageElement, DynamicSelectElement, IframeElement, \
    CreatedRuleElement, DynamicRateConditions, DynamicIndexElement


class LoginMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.login_button = PageElement(self.page, "//button[text()='Login']")
        self.username = PageElement(self.page, "//input[@id='username']")
        self.password = PageElement(self.page, "//input[@id='password']")
        self.next_button = PageElement(self.page, "//button[text()='Next']")
        self.submit = PageElement(self.page, "//button[@type='submit']")
        self.error_message = PageElement(self.page, "//p[contains(@class, 'Mui-error')]")
        self.invalid_email_or_password_message = PageElement(
            self.page,
            '//*[contains(@class, "Login-errorWhite")]/*[text()]')
        self.skip_this_step = PageElement(self.page,
                                          "//label[text()='Skip This Step']")
        self.reset_pasword = PageElement(self.page,
                                         "//form[@class='change-password-form']")


class CommonMixin:
    """ Shared elements """
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        # General
        self.input_name = PageElement(self.page, "//input[@id='name']")
        self.client_snackbar = PageElement(self.page, "//*[@id='notistack-snackbar']")
        self.apply = PageElement(self.page, "//button[text()='Apply']")
        self.save = PageElement(self.page, "//button[text()='Save']")
        self.create = PageElement(self.page, "//button[text()='Create']")
        self.close = PageElement(self.page, "//button[text()='Close']").nth(1)
        self.cancel_button = PageElement(self.page, "//*[text()='Cancel']")
        self.select = UlElement(self.page, "//ul[@role='listbox']")
        self.redeploy_button = PageElement(self.page, "//button[@data-qa='redeploy-btn']")
        self.select_by_name = DynamicSelectElement(
            self.page, "//ul[@role='listbox']/li[text()='{name}']")
        # self.select_by_name = DynamicPageElement(self.page, "//ul[@role='listbox']/li[text()='{name}']")
        self.table = TableElement(self.page, "//table")
        self.submit_button = PageElement(self.page, "//button[text()='Submit']")
        self.delete_button = PageElement(self.page, "//button[text()='Delete']")
        self.confirm_button = PageElement(self.page, "//button[text()='Confirm']")
        self.revert_button = PageElement(self.page, "//button[text()='Revert']")
        self.revert_confirm_button = PageElement(self.page, "//button[text()='Revert Changes']")
        self.delete_button_list = ListElement(self.page,"//button[@data-qa='delete-button']")
        self.deploy_changes_button = PageElement(self.page, "//button[text()='Deploy Changes']")
        self.create_org_button = PageElement(self.page, "//*[text()='Create an Organization']")

        self.docs = PageElement(self.page, "//li[text()='Docs']")
        self.forums = PageElement(self.page, "//li[text()='Forums']")
        self.status = PageElement(self.page, "//li[text()='Status']")
        self.support = PageElement(self.page, "//li[text()='Support']")

        self.overview = PageElement(self.page, "//*[text()='Overview']")
        self.activity = PageElement(self.page, "//*[text()='Activity']")
        self.members = PageElement(self.page, "//*[text()='Members']")
        self.settings = PageElement(self.page, "//*[text()='Settings']")
        self.security = PageElement(self.page, "//div/span[text()='Security']")
        self.attack_surfaces = PageElement(self.page, "//div/span[text()='Attack Surfaces']")

        # Create organization dialog
        self.button_create_org_dialog = PageElement(
            self.page,
            '//button[text()="Create an Organization"]')

        self.org_switcher_button = PageElement(self.page, "//button[@id='organization-switcher']")
        self.org_switcher_list = UlElement(self.page, "//ul[@role='menu']")
        self.delete_org_checkbox = PageElement(
            self.page,
            "//*[text()='Confirm that I want to delete this organization.']/../..//input[@type='checkbox']")
        self.delete_org_button = PageElement(self.page, "//*[text()='Delete Organization']")

        self.visible_page_content = PageElement(self.page,
                                                "//div[@id='__next' and not(@aria-hidden='true')]")
        self.status_iframe = PageElement(self.page, "//iframe[@title='Layer0 Status']")
        self.status_iframe_close_button = IframeElement(self.status_iframe,
                                                        "//div[contains(@class, 'frame-close')]//button")
        self.status_snackbar_close = PageElement(self.page, "//div[@id='notistack-snackbar']/..//button")
        self.online_status = PageElement(self.page, "//i[text()='Deployed']")


class OrgMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.add_member_button = PageElement(self.page, "//button[text()='Add Member']")
        self.invite_member_button = PageElement(self.page,
                                                "//button[text()='Invite']")
        self.member_permission = DynamicPageElement(self.page, "//div/p[text()='{role}']")
        self.email = PageElement(self.page, "//input[@id='email']")
        self.plus_button = PageElement(self.page, "//button[@title='Add']")

        self.members_table = MembersTableElement(self.page, "//table")
        self.selected_org = DynamicPageElement(self.page,
                                               "//header//p[text()='{name}']")
        # Create property
        self.new_property_button = PageElement(self.page, "//*[text()='New Property']")
        self.origin_hostname_input = PageElement(
            self.page, "//input[@name='origins.0.hosts.0.hostname']")
        self.create_property_button = PageElement(self.page,
                                                  "//*[text()='Create Property']")


class EnvironmentMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.environments = PageElement(self.page, "//*[text()='Environments']")
        self.new_environment_button = PageElement(self.page,
                                                  "//*[text()='New Environment']")
        self.configuration = PageElement(self.page, "//*[text()='Configuration']")
        self.hostnames = PageElement(self.page, "//*[text()='Hostnames']")
        self.origins = PageElement(self.page, "//*[text()='Origins']")
        self.rules = PageElement(self.page, "//*[text()='Rules']")

        self.environment = DynamicPageElement(self.page, "//a/div[@role='button' and text()='{name}']")
        self.revert_button = PageElement(self.page, "//button[text()='Revert']")
        self.revert_changes_button = PageElement(self.page,
                                                 "//button[text()='Revert Changes']")
        # ======== Rules =========
        self.add_rule = PageElement(self.page, "//button[text()='Add Rule']")
        self.add_element = PageElement(self.page, "//button[text()='Add']")
        self.select_rule_element = DynamicSelectElement(
            self.page,
            "//div[not(@aria-hidden='true')]/div/ul[@role='menu']/*[@role='menuitem' and text()='{name}']")
        self.delete_rule_list = ListElement(self.page,
                                            "//button[@data-qa='delete-button']")
        self.condition_operator_list = ListElement(
            self.page, "//div[contains(@class, 'MuiCollapse-entered')]//div[@role='button']")
        self.select_operator_name = DynamicSelectElement(
            self.page,
            "//div[@role='presentation' and not(@aria-hidden='true')]/div/ul[@role='menu']/li[text()='{name}']")
        self.delete_rule_button = PageElement(self.page, "//button[text()='Delete Rule']")
        self.add_feature_button = PageElement(
            self.page, "//button[@type='submit' and text()='Add Feature']")
        self.deploy_changes = PageElement(self.page, "//button[text()='Deploy Changes']")
        self.variable_input = PageElement(self.page,
                                          "//label[text()='Variable']/../div/input")
        self.variable_select = DynamicPageElement(
            self.page, "//div[text()='All Variables']/../ul/li//p[text()='{name}']")
        self.operator_input = PageElement(self.page,
                                          "//label[text()='Operator']/../div/input")
        self.rule_checkbox = PageElement(self.page, "//label//input[@type='checkbox']")
        self.code_input = PageElement(self.page, "//input[@name='feature.value.code']")
        self.name_input = PageElement(
            self.page, "//label[contains(text(), 'Name')]/..//div[@role='textbox']")
        self.value_div = PageElement(
            self.page, "//label[contains(text(), 'Value')]/..//div[@role='textbox']")
        self.match_value_input = PageElement(
            self.page, "//label[contains(text(), 'Value')]/../div/input")
        self.match_tags_inputs = PageElement(
            self.page, "//label[contains(text(), 'Value')]/../div")
        self.match_compress_content_type_inputs = PageElement(
            self.page, "//label[contains(text(), 'Compress Content Type')]/../div")
        self.match_value_regex = PageElement(
            self.page, "//label[contains(text(), 'Match Value')]/..//div[@role='textbox']")
        self.values_list = PageElement(
            self.page, "//label[contains(text(), 'Value(s')]/../div")
        self.add_condition_button = PageElement(
            self.page, "//button[@type='submit' and text()='Add Condition']")
        self.feature_input = PageElement(self.page,
                                         "//input[@placeholder='Search Features...']")
        self.feature_select = DynamicSelectElement(
            self.page,
            "//ul[@role='listbox']/li/div[text()='{type}']/../ul/li[text()='{name}']")
        self.header_name = PageElement(
            self.page,
            "//label[contains(text(), 'Header Name')]/..//div[@role='textbox']")
        self.response_headers = PageElement(
            self.page, "//input[@name='remove_response_headers']")
        self.origin_response_headers = PageElement(
            self.page, "//label[text()='Response Headers']/../div/input")
        self.match_style_input = PageElement(
            self.page, "//input[@name='feature.value.0.syntax']")
        self.source_input = PageElement(
            self.page, "//label[contains(text(), 'Source')]/..//div[@role='textbox']")
        self.destination_input = PageElement(
            self.page, "//label[contains(text(), 'Destination')]/..//div[@role='textbox']")
        self.variable_name = PageElement(
            self.page, "//label[text()='Name']/..//div[@role='textbox']")
        self.variable_value = PageElement(
            self.page, "//label[text()='Value']/..//div[@role='textbox']")
        self.number_input = PageElement(self.page,
                                        "//input[@name='condition.ruleVariable.value']")
        self.response_headers = PageElement(
            self.page,
            "//label[text()='Response Headers']/../div/input")
        self.parameter_name = PageElement(self.page,
                                          "//label[text()='Parameter Name']/..//div[@role='textbox']")
        self.custom_log_field = PageElement(
            self.page, "//label[text()='Custom Log Field']/../div/input")
        self.response_body = PageElement(
            self.page, "//label[text()='Response Body']/..//textarea")
        self.kbytes_per_second = PageElement(
            self.page, "//input[@name='feature.value.kbytes_per_sec']")
        self.prebuf_seconds = PageElement(
            self.page, "//input[@name='feature.value.prebuf_seconds']")
        self.header_treatment_input = PageElement(
            self.page, "//label[text()='Cache Control Header Treatment']/../div/input")
        self.cache_key_option_input = PageElement(self.page, "//input[@name='cache-key']")
        self.headers_input = PageElement(self.page, "//input[@name='headers']")
        self.cookies_input = PageElement(self.page, "//input[@name='cookies']")
        self.add_expression_button = PageElement(self.page,
                                                 "//button[text()='Add an Expression']")
        self.expression_input = PageElement(self.page, "//div[@role='textbox']/div")
        self.option_input = PageElement(self.page, "//input[@name='cache-key-query-string']")
        self.include_input = PageElement(self.page, "//input[@name='include']")
        self.exclude_input = PageElement(self.page, "//input[@name='exclude']")
        self.cacheable_request_body_size = PageElement(
            self.page, "//label[text()='Cacheable Request Body Size']/../div/input")
        self.compress_content_types_input = PageElement(
            self.page, "//label[text()='Compress Content Types']/../div/input")
        self.post_input = PageElement(self.page, "//label[text()='POST']/..//input")
        self.put_input = PageElement(self.page, "//label[text()='PUT']/..//input")
        self.h264_support_input = PageElement(
            self.page,
            "//label[text()='Enable H264 encoding']/../div/input")
        self.expires_header_treatment_input = PageElement(
            self.page, "//label[text()='Expires Header Treatment']/../div/input")
        self.duration_value = PageElement(
            self.page, "//input[@name='feature.value' and @type='number']")
        self.duration_unit = PageElement(self.page,
                                         "//input[@name='feature.value' and @type='text']")
        self.response_status_code = PageElement(
            self.page, "//input[@name='feature.value.0.key']")
        self.max_age_value = PageElement(self.page,
                                         "//input[@name='feature.value.0.value' and @type='number']")
        self.max_age_unit = PageElement(self.page,
                                        "//input[@name='feature.value.0.value' and @type='text']")
        self.service_worker_max_age_value = PageElement(
            self.page, "//input[@name='feature.value' and @type='number']")
        self.service_worker_max_age_unit = PageElement(
            self.page, "//input[@name='feature.value' and @type='text']")
        self.ignore_origin_no_cache = PageElement(self.page,
                "//label[text()='Ignore no-cache headers when the origin returns one of these status codes:']/../div/input")
        self.cacheable_status_codes = PageElement(
            self.page, "//label[text()='Cacheable Status Codes']/../div/input")
        self.feature_value_input = PageElement(
            self.page, "//input[@name='feature.value']")
        self.proxy_special_headers_input = PageElement(
            self.page, "//label[text()='Proxy Special Headers']/../div/input")
        self.set_origin_input = PageElement(self.page,
                                            "//label[text()='Origin Name']/../div/input")
        # AI Rules
        self.add_rule_using_ai = PageElement(self.page,
                                             "//button[text()='Add Rule Using AI...']")
        self.add_rule_using_ai_input = PageElement(
            self.page, "//input[@data-qa='add-rule-using-ai-text']")
        self.generate_rule = PageElement(self.page, "//button[text()='Generate Rule']")
        self.rules_list = ListElement(self.page, "//div[@data-rbd-droppable-id='droppable-rules']/div")
        self.created_rule = CreatedRuleElement(
            self.page,
            "((//div[@data-qa='rule-conditions'])[{rule_num}]//div[@data-qa='rule-condition'])[{{num}}]",
            "((//div[@data-qa='rule-features'])[{rule_num}]//div[@data-qa='rule-feature'])[{{num}}]")
        self.single_condition = ListElement(self.page, "//div[@data-qa='rule-condition']")
        self.rule_div = PageElement(self.page,
                                    "//form/div/div/div[@data-rbd-draggable-context-id]")
        self.nested_rule_add_element_button = DynamicPageElement(
            self.page,
            "((//div[@data-rbd-droppable-id='{id}']/div)[{num}]//button[text()='Add'])[last()]")
        self.rule_add_element_button = DynamicIndexElement(
            self.page,
            "(//form/div/div/div[@data-rbd-draggable-id][{num}]//button[text()='Add'])[last()]")
        self.ai_rule_generation_error = PageElement(self.page,
                                                    "//form//p[contains(@class, 'MuiTypography-body1')]")
        # ====== Cache =====

        self.purge_the_cache = PageElement(self.page,
                                           "//button[text()='Purge the Cache...']")
        self.purge_cache = PageElement(self.page, "//button[text()='Purge Cache']")
        self.purge = PageElement(self.page, "//button[text()='Purge']")
        self.purge_all_entries = PageElement(self.page, "//input[@value='all_entries']")
        self.purge_by_path = PageElement(self.page, "//input[@value='path']")
        self.purge_by_key = PageElement(self.page, "//input[@value='surrogate_key']")


class ActivityMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        # TODO


class TrafficMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

        # Date Picker
        self.date_picker = PageElement(self.page, "//div[@data-qa='date-range-picker']")
        self.date_picker_today = PageElement(self.page, "//div[@data-qa='dp-range-TODAY']")
        self.date_picker_last_24_hours = PageElement(self.page, "//div[@data-qa='dp-range-LAST_24_HOURS']")
        self.date_picker_last_7_days = PageElement(self.page, "//div[@data-qa='dp-range-LAST_7_DAYS']")
        self.date_picker_this_month = PageElement(self.page, "//div[@data-qa='dp-range-THIS_MONTH']")
        self.date_picker_last_month = PageElement(self.page, "//div[@data-qa='dp-range-LAST_MONTH']")
        self.date_picker_last_30_days = PageElement(self.page, "//div[@data-qa='dp-range-LAST_30_DAYS']")
        self.date_picker_last_90_days = PageElement(self.page, "//div[@data-qa='dp-range-LAST_90_DAYS']")
        self.date_picker_daily = PageElement(self.page, "//div[@data-qa='dp-range-DAY']")
        self.date_picker_monthly = PageElement(self.page, "//div[@data-qa='dp-range-MONTH']")
        self.date_picker_custom_date_range = PageElement(self.page, "//div[@data-qa='dp-range-CUSTOM_RANGE']")
        self.date_picker_apply_button = PageElement(self.page, "//button[text()='Apply']")

        # Traffic Overview elements
        self.traffic_header = PageElement(self.page, "//h2[text()='Traffic']")
        self.traffic_overview_tab_button = PageElement(self.page,
            "//button[@role='tab']/..//*[text()='Overview']")
        self.traffic_metric_selector = PageElement(self.page,
            '//input[@data-qa="data-usage-metricsSelector"]')
        self.traffic_requests_grid_summary = PageElement(self.page,
            "//div[@data-qa='urls-chart']//*[contains(text(), 'Requests')]")
        self.traffic_errors_grid_summary = PageElement(self.page,
            '//div[@data-qa="errors-card"]//*[contains(text(), "Errors")]')
        self.traffic_rules_grid_summary = PageElement(self.page,
            '//main//span[text()="Rules"]')
        self.traffic_rules_metric_selector = PageElement(self.page,
            '//input[@data-qa="rules-metricsSelector"]')
        self.traffic_rules_percentile_selector = PageElement(self.page,
            '//input[@data-qa="rules-percentilesSelector"]')
        self.traffic_origin_latency_over_time_summary = PageElement(self.page,
            '//div[@data-qa="urls-chart"]//*[text()="Origin Latency Over Time"]')
        self.show_request_count_button = PageElement(self.page,
            '//div[@data-qa="rules-percentageToggle"]//button[@value="count"]')
        self.show_as_percentage_of_total_requests_button = PageElement(self.page,
            '//div[@data-qa="rules-percentageToggle"]//button[@value="percent"]')
        self.chart_filter_button = ListElement(self.page, '//button[@data-qa="chart-settings"]')
        self.chart_filter_button_full_cache_flushes = ListElement(self.page,
            '//div[@data-qa="settings-show-cacheFlushes"]//input[@type="checkbox"]')
        self.chart_filter_button_deployments = ListElement(self.page,
            '//div[@data-qa="settings-show-deployments"]//input[@type="checkbox"]')
        self.traffic_origin_latency_drop_down_filter = PageElement(self.page,
            "//input[@data-qa='originLatency-breakdownSelector']")
        self.traffic_origin_latency_metrics_selector = PageElement(self.page,
            "//input[@data-qa='originLatency-metricsSelector']")
        self.traffic_origin_latency_percentile_selector = PageElement(self.page,
            "//input[@data-qa='originLatency-percentilesSelector']")
        self.traffic_main_chart_summary = PageElement(self.page, "//*[@data-qa='data-usage-summary']")
        self.traffic_rules_coulumn_with_metrics_data = PageElement(self.page,
            '//table//tr//th[10]//*[@aria-disabled]')
        # By Country tab elements
        self.country_tab = PageElement(self.page, "//button[@role='tab'][contains(text(), 'By Country')]")
        self.country_map = PageElement(self.page, "//div[@data-qa='geo-map']")
        self.country_metric_selector = PageElement(self.page,
            '//input[@data-qa="geo-metricsSelector"]')
        self.country_percentile_selector = PageElement(self.page,
            '//input[@data-qa="geo-percentilesSelector"]')
        self.country_tab_origin_latency_by_country_grid = PageElement(self.page,
            "//div[@data-qa='geo-table']//*[text()='Origin Latency by Country']")


class RedirectsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.add_a_redirect_button = PageElement(self.page, "//button[@data-qa='redirect-add-btn']")
        self.remove_selected_redirect = PageElement(self.page, "//button[@data-qa='redirect-remove-btn']")
        self.confirm_remove_redirect = PageElement(self.page, "//button[text()='Remove ']")
        self.search_field = PageElement(self.page, "//input[@id='search']")
        self.default_status_dropdown = PageElement(self.page, "//div[@data-qa='redirect-default-status-picker']")
        self.import_button = PageElement(self.page, "//button[@data-qa='redirect-import-btn']")
        self.export_button = PageElement(self.page, "//button[@data-qa='redirect-export-btn']")
        self.redirect_from = PageElement(self.page, "//input[@id='from']")
        self.redirect_to = PageElement(self.page, "//input[@id='to']")
        self.response_status = PageElement(self.page, "//div[@data-qa='redirect-status-picker']//div[@role='combobox']")
        self.forward_query_string = PageElement(self.page, "//span[@data-qa='redirect-forward-query-string-checkbox']")
        self.save_redirect_button = PageElement(self.page, "//button[@data-qa='redirect-add-save-popup-btn']")
        self.import_override_existing = PageElement(self.page, "//span[text()='Override existing list with file content']")
        self.import_append_file = PageElement(self.page, "//span[text()='Append file content to existing redirects list']")
        self.upload_redirect_button = PageElement(self.page, "//button[text()='Upload redirects']")
        self.redeploy_confirmation = PageElement(self.page, "//div[@role='dialog']//button[contains(text(), 'Deploy Now')]")
        self.delete_all_checkbox = PageElement(self.page, "//table//tr//th//input[@type='checkbox']")
        self.first_checkbox_from_the_table = PageElement(self.page, "//table//tbody//td//input[@type='checkbox']")
        self.empty_list_message = PageElement(self.page, "//div[text()='This environment has no redirects']")
        self.table_value_from_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[2]")
        self.table_value_to_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[3]")
        self.table_value_status_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[4]")
        self.table_value_query_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[5]")
        self.import_browse_button = PageElement(self.page, "//button[@data-qa='redirect-import-browse-btn']")
        self.redirects_page = PageElement(self.page, "//span[text()='Redirects']")
        self.no_redirects_matching = PageElement(self.page, "//div[text()='No redirects matching \"']")


class DeploymentsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.serverless = PageElement(self.page, "//button[@id='server-logs']")
        # Change it when data-qa attr is ready
        self.resume_logs = PageElement(
            self.page,
            "//button[@data-qa='resume-logs']")


class SecurityMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.event_logs = PageElement(self.page, "//*[text()='Logs']")
        self.security_application = PageElement(self.page,
                                                "//*[text()='Security Apps']")
        self.dashboard = PageElement(self.page, "//*[text()='Dashboard']")
        self.rules_manager = PageElement(self.page, "//*[text()='Rules Manager']")
        self.access_rules = PageElement(self.page, "//*[text()='Access Rules']")
        self.rate_rules = PageElement(self.page, "//*[text()='Rate Rules']")
        self.bot_rules = PageElement(self.page, "//*[text()='Bot Rules']")
        self.custom_rules = PageElement(self.page, "//*[text()='Custom Rules']")
        self.managed_rules = PageElement(self.page, "//*[text()='Managed Rules']")

        self.add_rule = PageElement(self.page, "//button[text()='Add Rule']")
        self.no_data_to_display = PageElement(self.page, "//div[text()='No data to display']")

        # ========= Rate Rules ======

        self.input_num = PageElement(self.page, "//input[@id='num']")
        self.add_rate_rule = PageElement(self.page, "//button[text()='New Rate Ruleset']")
        self.rate_new_condition_group = PageElement(
            self.page,"//button[text()='New Condition Group']")
        self.rate_new_condition = PageElement(self.page, "//span[text()= 'New Condition']")
        self.rate_condition_value_input = PageElement(self.page, "//input[@placeholder='Add...']")
        self.rate_conditions = DynamicRateConditions(
            self.page,
            "//button[@data-rbd-draggable-context-id='{group}' and @title='Condition {condition}']"
            )
        self.rate_condition_match_by = DynamicPageElement(
            self.page,
            "//input[@name='conditionGroups[{group}].conditions[{condition}].target.type']")
        self.rate_condition_values = ListElement(
            self.page,
            "//label[text()='Values']/..//div[@role='button']")
        self.match_req_header_input = PageElement(self.page, '//input[@placeholder="Type or select header name"]')

        # ======== Managed Rules ==========

        self.add_managed_rule = PageElement(self.page, "//button[text()='New Managed Ruleset']")

        # Ignore list
        self.header_name_input = PageElement(
            self.page, "//input[@name='generalSettings.responseHeaderName']")
        self.ignore_cookies_input = PageElement(
            self.page, "//input[@name='generalSettings.ignoreCookie']")
        self.ignore_cookies_buttons = ListElement(
            self.page,
            "//input[@name='generalSettings.ignoreCookie']/..//div[@role='button']")
        self.ignore_header_input = PageElement(
            self.page, "//input[@name='generalSettings.ignoreHeader']")
        self.ignore_header_buttons = ListElement(
            self.page,
            "//input[@name='generalSettings.ignoreHeader']/..//div[@role='button']")
        self.ignore_query_args_input = PageElement(
            self.page, "//input[@name='generalSettings.ignoreQueryArgs']")
        self.ignore_query_args_buttons = ListElement(
            self.page,
            "//input[@name='generalSettings.ignoreQueryArgs']/../div[@role='button']")

        # More Details
        self.more_details = PageElement(self.page, "//div//p[text()='More Details']")
        self.max_args_reqs_input = PageElement(self.page,
                                               "//input[@name='generalSettings.maxNumArgs']")
        self.single_arg_length_input = PageElement(
            self.page, "//input[@name='generalSettings.argLength']")
        self.arg_name_length_input = PageElement(
            self.page, "//input[@name='generalSettings.argNameLength']")
        self.total_arg_length_input = PageElement(
            self.page, "//input[@name='generalSettings.totalArgLength']")
        self.json_parser_input = PageElement(
            self.page, "//input[@name='generalSettings.jsonParser']")

        # Policies
        self.policies = PageElement(self.page, "//button[text()='Inbound Policies']")
        self.ruleset_input = PageElement(self.page, "//input[@name='rulesetVersion']")
        self.ruleset_select = UlElement(self.page, "//ul[@role='listbox']//ul")
        self.threshold_input = PageElement(self.page,
                                           "//input[@name='generalSettings.anomalyThreshold']")
        self.paranoia_level_input = PageElement(
            self.page, "//input[@name='generalSettings.paranoiaLevel']")
        self.ruleset_switch = PageElement(self.page, "//input[@name='rulesetswitch']")
        # Exceptions
        self.exceptions = PageElement(self.page, "//button[text()='Exceptions']")
        self.add_condition = PageElement(self.page, "//button//span[text()='Add New Condition']")
        self.rule_ids = PageElement(self.page,
                                    "//input[@name='ruleTargetUpdates[0].ruleIds']")
        self.parameter_input = PageElement(self.page,
                                               "//input[@name='ruleTargetUpdates[0].target']")
        self.condition_name = PageElement(self.page,
                                          "//input[@name='ruleTargetUpdates[0].targetMatch']")
        self.regex_switch = PageElement(self.page, "//input[@name='regexSwitch']")
        self.rule_ids_buttons = ListElement(
            self.page,
            "//input[@name='ruleTargetUpdates[0].ruleIds']/..//div[@role='button']")

        self.conditions = ListElement(
            self.page, "//div[@aria-label='Managed rule exceptions']/button")

        # ============= Security application manager ============

        self.secapp_by_name = DynamicPageElement(
            self.page,
            "//div[@data-rbd-droppable-id='droppable']//h4[text()='{name}']/ancestor::div[2]")
        self.secapp_names = PageElement(self.page, "//div[@role='button']/div/h4")
        self.save_secapp = PageElement(
            self.page,
            "//div[text()='You have unsaved changes.']/../..//button[text()='Save']")
        self.new_seccurity_application = PageElement(
            self.page, "//button[text()='New Security Application']")
        self.host_input = PageElement(self.page, "//input[@name='host.type']")
        self.host_values_input = PageElement(self.page, "//input[@name='host.values']")
        self.host_values_buttons = PageElement(
            self.page, "//input[@name='host.values']/..//div[@role='button']")
        self.url_path_input = PageElement(self.page, "//input[@name='path.type']")
        self.url_values_input = PageElement(self.page, "//input[@name='path.values']")
        self.url_values_buttons = PageElement(
            self.page, "//input[@name='path.values']/..//div[@role='button']")
        self.host_negative_match_checkbox = PageElement(
            self.page, "//input[@name='host.isNegated']")
        self.path_negative_match_checkbox = PageElement(
            self.page, "//input[@name='path.isNegated']")
        # Access Rules
        self.config_access_rules = PageElement(
            self.page,
            "//button[@id='vertical-tab-0']")
        self.prod_access_rule_input = PageElement(self.page, "//input[@name='aclProdId']")
        self.action_access_rule_input = PageElement(self.page, "//input[@name='aclProdAction.enfType']")
        self.audit_access_rule_input = PageElement(self.page, "//input[@name='aclAuditId']")

        # Rate rules
        self.config_rate_rules = PageElement(
            self.page,
            "//div[@aria-label='Managed rule exceptions']//button[text()='Rate Rules']")
        self.prod_rate_rule_input = PageElement(self.page,
                                                "//input[@placeholder='Add Rate Rule']")
        # Managed Rules
        self.config_managed_rules = PageElement(
            self.page,
            "//div[@aria-label='Managed rule exceptions']//button[text()='Managed Rule']")
        self.prod_managed_rule_input = PageElement(self.page, "//input[@name='rulesProdId']")
        self.action_managed_rule_input = PageElement(self.page, "//input[@name='rulesProdAction.enfType']")
        self.audit_managed_rule_input = PageElement(self.page, "//input[@name='rulesAuditId']")

        # ================= Access Rules ==========

        self.add_access_rule = PageElement(self.page, "//button[text()='New Access Ruleset']")
        # Access Control
        self.access_control_input = PageElement(self.page,
                                                "//input[@name='access-control-dropdown']")
        self.whitelist = PageElement(self.page, "//button/p[text()='whitelist']")
        self.blacklist = PageElement(self.page, "//button/p[text()='blacklist']")
        self.accesslist = PageElement(self.page, "//button/p[text()='accesslist']")
        # Create Access Control inputs for dropdown list
        for type_title, list_ in product(ACCESS_CONTROL_TYPE,
                                   ('whitelist', 'blacklist', 'accesslist')):
            type_id = ACCESS_CONTROL_TYPE[type_title]
            # Inputs
            setattr(self,
                    f'{type_id.lower()}_{list_}_input',
                    PageElement(self.page, f"//textarea[@name='{type_id}.{list_}']"))
            # Buttons
            setattr(self,
                    f'{type_id.lower()}_{list_}',
                    PageElement(self.page, f"//div[p='{type_title}']/../../../..//p[text()='{list_}']"))
            # # Saved input values
            # setattr(self,
            #         f'{type_id.lower()}_{list_}_values',
            #         ListElement(self.page, f"//p[span='{type_title}']/../../../..//div[@role='button']/span"))

        # Allowed HTTP Methods
        for method in HTTP_METHODS:
            setattr(self,
                    f'method_{method.lower()}',
                    PageElement(self.page, f"//input[@value='{method}']"))

        self.other_methods = PageElement(self.page, "//input[@name='other http methods']")
        self.other_methods_buttons = ListElement(
            self.page, '//div[@placeholder="Add..."]//div[@role="button"]')

        self.response_header_name = PageElement(self.page,
                                                "//input[@name='responseHeaderName']")
        self.file_upload_limit = PageElement(
            self.page, "//input[@name='maxFileSize']")

        self.request_content_type = PageElement(self.page,
                                                "//input[@name='allowedRequestContentTypes']")
        self.request_content_type_buttons = ListElement(
            self.page,
            "//label[text()='Allowed Request Content Types']/..//div[@role='button']")
        self.request_content_type_buttons = ListElement(
            self.page,
            "//label[text()='Allowed Request Content Types']/..//div[@role='button']")
        self.request_content_type_clear = ListElement(
            self.page,
            "//label[text()='Allowed Request Content Types']/..//button[@title='Clear']")
        self.extension_blacklist = PageElement(self.page,
                                               "//input[@name='disallowedExtensions']")
        self.extension_blacklist_buttons = ListElement(
            self.page, "//label[text()='Extension Blacklist']/..//div[@role='button']")
        self.extension_blacklist_clear = ListElement(
            self.page,
            "//label[text()='Extension Blacklist']/..//button[@title='Clear']")
        self.header_blacklist = PageElement(self.page, "//input[@name='disallowedHeaders']")
        self.header_blacklist_buttons = ListElement(
            self.page,
            "//label[text()='Header Blacklist']/..//div[@role='button']")
        self.header_blacklist_clear = ListElement(
            self.page,
            "//label[text()='Header Blacklist']/..//button[@title='Clear']")

        # ==================== Dashboard & Event Logs ==============

        self.dashboard_time_frame_input = PageElement(
            self.page, "//input[@id='time']")
        self.view_input = PageElement(self.page, "//input[@name='view']")
        self.refresh_input = PageElement(self.page, "//input[@name='refresh']")

        self.threats_button = PageElement(self.page, "//button[text()='Threats']")
        self.browser_challenges_button = PageElement(self.page,
                                                     "//button[text()='Browser Challenges']")
        self.rates_button = PageElement(self.page, "//button[text()='Rates']")
        self.rate_enforcement_button = PageElement(self.page,
                                                   "//button[text()='Rate Enforcement']")
        # Advanced filters
        self.add_edit_filters = PageElement(self.page, "//button[text()='Edit/Add Filters']")
        self.add_filter = PageElement(self.page, "//button[text()='Add Filter']")

        self.field_input = PageElement(self.page, "//input[@placeholder='Select Field']")
        self.value_input = PageElement(self.page, "//input[@name='domain']")

        self.filter_names = ListElement(
            self.page,
            "//div[contains(@class, 'MuiGrid-container')]/div[contains(@class, 'MuiGrid-item')]/div[@role='button']")
        self.filter_remove = ListElement(self.page,
                                         "//div[p[contains(., 'Filters:')]]//button")
        self.dashboard_current_time = PageElement(
            self.page, "//h2[contains(text(), 'Security')]/../h6")


class AttackSurfacesMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)

        self.error_message = PageElement(self.page, "//h1[text()='Something went wrong.']")

        # menu
        self.dashboard = PageElement(self.page, "//div[@data-qa='asm-dashboard']")
        self.collections = PageElement(self.page, "//div[@data-qa='asm-collections']")
        self.entities = PageElement(self.page, "//div[@data-qa='asm-entities']")
        self.exposures = PageElement(self.page, "//div[@data-qa='asm-exposures']")
        self.technologies = PageElement(self.page, "//div[@data-qa='asm-technologies']")
        self.rules = PageElement(self.page, "//div[@data-qa='asm-rules']")

        # Dashboard items
        self.dash_header = PageElement(self.page, "//h2[text()='Attack Surfaces Dashboard']")

        # Collections items
        self.collections_header = PageElement(self.page, "//h2[text()='Collections']")
        self.create_collection_btn = PageElement(self.page, "//button[@data-qa='create-collection-btn']")
        self.collections_table = TableElement(self.page, "//table[@data-qa='collections-tbl']")

        # Collections Create dialog
        self.dlg_name = PageElement(self.page, "//input[@id='name']")
        self.dlg_descr = PageElement(self.page, "//input[@id='description']")
        # //button[@data-qa='btn-sch-sun']
        # //button[@data-qa='btn-sch-mon']
        # //button[@data-qa='btn-sch-tue']
        # //button[@data-qa='btn-sch-wed']
        # //button[@data-qa='btn-sch-thu']
        # //button[@data-qa='btn-sch-fri']
        # //button[@data-qa='btn-sch-sat']
        # //input[@id='scan_at_utc_hour']
        self.dlg_email_on_start = PageElement(self.page, "//*[@data-qa='email-on-start']//input")
        self.dlg_email_on_complete = PageElement(self.page, "//*[@data-qa='email-on-complete']//input")
        self.dlg_email_on_exposure = PageElement(self.page, "//*[@data-qa='email-on-exposure']//input")
        # //div[@data-qa='email-to']
        self.dlg_create_collection_btn = PageElement(self.page, "//button[@data-qa='create-dlg-save-btn']")
        self.dlg_cancel_btn = PageElement(self.page, "//button[@data-qa='create-dlg-cancel-btn']")

        # Collections Delete collection dialog
        self.del_dlg_cancel_btn = PageElement(self.page, "//div[@role='dialog']//button[text()='Cancel']")
        self.del_dlg_delete_btn = PageElement(self.page, "//div[@role='dialog']//button[text()='Delete']")

        # Inside collection
        self.coll_scan_now_btn = PageElement(self.page, "//button[@data-qa='scan-now-btn']")
        self.coll_edit_collection_btn = PageElement(self.page, "//button[@data-qa='edit-collection-btn']")
        # //div[@data-qa='collection-overview']
        # -------------------- TBD overview here ------------------
        # Seeds
        self.seeds_tbl = PageElement(self.page, "//div[@data-qa='collection-seeds']//table")
        self.add_seed_btn = PageElement(self.page, "//div[@data-qa='collection-seeds']//button[text()='Add a Seed...']")
        # Add Seed dialog
        self.add_seed_dlg_type = PageElement(self.page, "//input[@name='seed_type_id']")
        self.add_seed_dlg_type_select = DynamicSelectElement(self.page, "//ul[@id='seed_type_id-listbox']/li[text()='{seed_type}']")
        self.add_seed_dlg_seed = PageElement(self.page, "//input[contains(@placeholder,'e.g.')]")
        self.add_seed_dlg_cancel_btn = PageElement(self.page, "//button[text()='Cancel']")
        self.add_seed_dlg_create_btn = PageElement(self.page, "//button[text()='Create Seed']")
        # Scans
        self.scans_tbl = TableElement(self.page, "//div[@data-qa='collection-scans']//table")
        # Scan details
        self.scan_exposures_tbl = TableElement(self.page, "//div[text()='Exposures']/../../../following-sibling::div//table")
        self.scan_tasks_tbl = TableElement(self.page, "//span[text()='Tasks']/../../following-sibling::div//table")

        # Reset Collection
        self.reset_collection_btn = PageElement(self.page, "(//button[text()='Reset Collection'])[1]")
        self.reset_collection_dlg_reset_btn = PageElement(self.page, "(//button[text()='Reset Collection'])[2]")

        # Assets (Entities) items
        self.assets_header = PageElement(self.page, "//h2[text()='Assets']")

        # Exposures items
        self.exposures_header = PageElement(self.page, "//h2[text()='Exposures']")
        self.exposures_tbl = TableElement(self.page, "//h2[text()='Exposures']/../../../following-sibling::div//table")

        # Technologies items
        self.technologies_header = PageElement(self.page, "//h2[text()='Technologies']")

        # Rules items
        self.rules_header = PageElement(self.page, "//h2[text()='Rules']")
        self.rules_reset_to_defaults_btn = PageElement(self.page, "//button[text()='Reset to Default']")
        self.rules_reset_dlg_reset_btn = PageElement(self.page, "//button[text()='Reset']")

    def wait_for_error(self, timeout=1000):
        try:
            self.error_message.wait_for(timeout=timeout, state="visible")
        except _errors.TimeoutError:
            pass
        else:
            assert False, "Error displayed"

    def get_collections(self, name_filter=None):
        self.log.debug(f"List collections")
        collections = []
        self.collections_table.scroll_into_view_if_needed()
        for row in self.collections_table.tbody.tr:
            coll_name = row[0].text_content()
            collections.append({
                'name': coll_name,
                'entities': row[1].text_content(),
                'exposures': row[2].text_content(),
                'last_scanned': row[3].text_content(),
            })
            if name_filter and name_filter == coll_name:
                return collections.pop()
        return collections

    def create_collection(self, collection_name: str):
        self.log.debug(f"Creating collection '{collection_name}'")
        self.create_collection_btn.click()
        self.dlg_name.fill(collection_name)
        self.dlg_email_on_start.uncheck()  # disable checkbox
        self.dlg_email_on_complete.uncheck()  # disable checkbox
        self.dlg_create_collection_btn.click()
        self.dlg_create_collection_btn.wait_for(state='hidden', timeout=5000)
        self.coll_scan_now_btn.wait_for(state='visible', timeout=5000)
        self.go_back()  # go back to the collections list
        self.wait_for_load_state('networkidle')
        self.log.debug(f"Collections: {self.get_collections()}")

    def remove_collection(self, collection_name: str, skip_empty_table=False):
        self.log.debug(f"Removing collection '{collection_name}'")
        self.collections_table.scroll_into_view_if_needed()
        for row in self.collections_table.tbody.tr:
            coll_title = row[0].text_content()
            if coll_title in (collection_name, 'all'):
                row.get_by_role("button").click()
                self.del_dlg_delete_btn.click()
                expect(row._locator, f'{coll_title} was not removed').to_have_count(0, timeout=5000)
                return
        else:
            if not skip_empty_table:
                raise Exception(f"Collections was not found")

    def open_collection(self, collection_name: str):
        self.log.debug(f"Opening collection '{collection_name}'")
        self.collections_table.scroll_into_view_if_needed()
        for row in self.collections_table.tbody.tr:
            if row[0].text_content() == collection_name:
                # self.locator(row[0]._locator).click()
                # self.locator(row[0]).click()
                row[0].click()

    def add_seed(self, seed_type, seed):
        """seed_type: Domain, Github repository, IP Address, IP Address Range"""
        self.add_seed_btn.click()
        self.add_seed_dlg_type.click()
        self.add_seed_dlg_type_select(seed_type=seed_type).click()
        self.add_seed_dlg_seed.fill(seed)
        self.add_seed_dlg_create_btn.click()

    def get_scans(self):
        self.log.debug(f"List scans")
        scans = []
        self.scans_tbl.scroll_into_view_if_needed()
        for row in self.scans_tbl.tbody.tr:
            scans.append({
                'when': row[0].text_content(),
                'status': row[1].text_content(),
                'entities_scanned': row[2].text_content(),
                'new_entities_discovered': row[3].text_content(),
                'new_exposures': row[4].text_content(),
                'new_technology_versions': row[5].text_content(),
            })
        return scans

    def wait_for_scans_completed(self, timeout=5):
        while timeout > 0:
            scans = self.get_scans()
            if all('completed' in s['status'].lower() for s in scans):
                break
            time.sleep(1)
            timeout -= 1
        else:
            raise TimeoutError(f"Timed out waiting for scans to complete")

    def open_scan(self, index):
        self.log.debug(f"Opening scan index: {index}")
        self.collections_table.tbody.tr[index][0].click()  # 0 index - first TD
        self.wait_for_load_state('networkidle')

    def get_scan_tasks(self):
        self.log.debug(f"List scan tasks")
        tasks = []
        self.scan_tasks_tbl.scroll_into_view_if_needed()
        for row in self.scan_tasks_tbl.tbody.tr:
            tasks.append({
                'status': row[0].text_content(),
                'duration': row[1].text_content(),
                'task': row[2].text_content(),
                'entity': row[3].text_content(),
                'hostnames': row[4].text_content(),
                'last_update': row[5].text_content(),
                'exposures_found': row[6].text_content(),
            })
        return tasks

    def get_scan_exposures(self):
        self.log.debug(f"List scan exposures")
        exposures = []
        self.scan_exposures_tbl.scroll_into_view_if_needed()
        for row in self.scan_exposures_tbl.tbody.tr:
            exposures.append(row[1].text_content())
        return exposures


class ExperimentsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.experiments_title = PageElement(self.page, "//h2/*[text()='Experimentation']")
        self.add_experiment_button = PageElement(self.page,
                                                 "//button[text()='Add Experiment']")
        # === Experiment parameters ===
        self.experiment_name = DynamicPageElement(self.page, "//*[text()='Experiment: ']/..//b[text()='{name}']")
        self.experiment_name_input = DynamicPageElement(self.page, "//input[@id='experiments.{id}.name']")
        self.variant_name_input = DynamicPageElement(self.page, "//input[@id='experiments.{exp_id}.variants.{var_id}.name']")
        self.variant_percentage_input = DynamicPageElement(self.page, "//input[@id='experiments.{exp_id}.variants.{var_id}.weight']")
        self.add_variant_button = PageElement(self.page, "//button[text()='Add Variant']")
        self.delete_experiment_button = PageElement(self.page, "(//button[@data-qa='delete-button'])[1]")
        self.delete_experiment_list = ListElement(self.page,
                                            "//button[@data-qa='delete-button']")
        self.is_active_checkbox_list = ListElement(self.page, "//form//input[@type='checkbox']")
        self.delete_experiment_confirm_button = PageElement(self.page, "//button[text()='Delete experiment']")
        self.wrong_percentage_message = PageElement(self.page, "//*[text()='Percentage total have to be 100']")
        # === Conditions ===
        self.add_criteria_button = PageElement(self.page, "//button[.//text()='Add Criteria']")
        self.add_condition_button = PageElement(self.page, "//button[text()='Add Condition']")
        self.variable_input = PageElement(self.page, "//label[text()='Variable']/../div/input")
        self.operator_input = PageElement(self.page, "//label[text()='Operator']/../div/input")
        self.variable_select = DynamicPageElement(
            self.page, "//div[text()='All Variables']/../ul/li//p[text()='{name}']")
        self.code_input = PageElement(self.page, "input[name='feature.value.code']")
        self.name_input = PageElement(self.page, "//label[contains(text(), 'Name')]/..//div[@role='textbox']")
        self.value_div = PageElement(self.page, "//label[contains(text(), 'Value')]/..//div[@role='textbox']")
        self.match_value_input = PageElement(self.page, "//label[contains(text(), 'Value')]/../div/input")
        self.match_tags_inputs = PageElement(self.page, "//label[contains(text(), 'Value')]/../div")
        self.match_compress_content_type_inputs = PageElement(
            self.page, "//label[contains(text(), 'Compress Content Type')]/../div")
        self.match_value_regex = PageElement(
            self.page, "//label[contains(text(), 'Match Value')]/..//div[@role='textbox']")
        self.values_list =  PageElement(self.page, "//label[contains(text(), 'Value(s')]/../div")
        self.rule_checkbox = PageElement(self.page, "(//label//input[@type='checkbox'])[1]")
        # === Features ===
        self.add_feature_confirm_button = PageElement(self.page, "//button[text()='Add Feature']")
        self.feature_input = PageElement(self.page,
                                         "input[placeholder='Search Features...']")
        self.feature_select = DynamicSelectElement(
            self.page,
            "//ul[@role='listbox']/li/div[text()='{type}']/../ul/li[text()='{name}']")
        self.header_name = PageElement(
            self.page,
            "//label[contains(text(), 'Header Name')]/..//div[@role='textbox']")
        self.add_action_button = PageElement(self.page, "(//button[text()='Add Action'])[1]")
        self.variable_input = PageElement(self.page,
                                          "//label[text()='Variable']/../div/input")
        self.variable_select = DynamicPageElement(
            self.page, "//div[text()='All Variables']/../ul/li//p[text()='{name}']")
        self.operator_input = PageElement(self.page,
                                          "//label[text()='Operator']/../div/input")
        self.rule_checkbox = PageElement(self.page, "(//label//input[@type='checkbox'])[1]")
        self.code_input = PageElement(self.page, "input[name='feature.value.code']")
        self.name_input = PageElement(
            self.page, "//label[contains(text(), 'Name')]/..//div[@role='textbox']")
        self.value_div = PageElement(
            self.page, "//label[contains(text(), 'Value')]/..//div[@role='textbox']")
        self.match_value_input = PageElement(
            self.page, "//label[contains(text(), 'Value')]/../div/input")
        self.match_tags_inputs = PageElement(
            self.page, "//label[contains(text(), 'Value')]/../div")
        self.origin_response_headers = PageElement(
            self.page, "//label[text()='Response Headers']/../div/input")
        self.match_style_input = PageElement(
            self.page, "input[name='feature.value.0.syntax']")
        self.source_input = PageElement(
            self.page, "//label[contains(text(), 'Source')]/..//div[@role='textbox']")
        self.destination_input = PageElement(
            self.page, "//label[contains(text(), 'Destination')]/..//div[@role='textbox']")
        self.variable_name = PageElement(
            self.page, "//label[text()='Name']/..//div[@role='textbox']")
        self.variable_value = PageElement(
            self.page, "//label[text()='Value']/..//div[@role='textbox']")
        self.number_input = PageElement(self.page,
                                        "input[name='condition.ruleVariable.value']")
        self.response_headers = PageElement(
            self.page,
            "//label[text()='Response Headers']/../div/input")
        self.parameter_name = PageElement(self.page,
                                          "//label[text()='Parameter Name']/..//div[@role='textbox']")
        self.custom_log_field = PageElement(
            self.page, "//label[text()='Custom Log Field']/../div/input")
        self.response_body = PageElement(
            self.page, "//label[text()='Response Body']/..//textarea")
        self.kbytes_per_second = PageElement(
            self.page, "input[name='feature.value.kbytes_per_sec']")
        self.prebuf_seconds = PageElement(
            self.page, "input[name='feature.value.prebuf_seconds']")
        self.header_treatment_input = PageElement(
            self.page, "//label[text()='Cache Control Header Treatment']/../div/input")
        self.option_input = PageElement(self.page, "input[name='cache-key-query-string']")
        self.include_input = PageElement(self.page, "input[name='include']")
        self.exclude_input = PageElement(self.page, "input[name='exclude']")
        self.cacheable_request_body_size = PageElement(
            self.page, "//label[text()='Cacheable Request Body Size']/../div/input")
        self.compress_content_types_input = PageElement(
            self.page, "//label[text()='Compress Content Types']/../div/input")
        self.post_input = PageElement(self.page, "//label[text()='POST']/..//input")
        self.put_input = PageElement(self.page, "//label[text()='PUT']/..//input")
        self.h264_support_input = PageElement(
            self.page,
            "//label[text()='Enable H264 encoding']/../div/input")
        self.expires_header_treatment_input = PageElement(
            self.page, "//label[text()='Expires Header Treatment']/../div/input")
        self.duration_value = PageElement(
            self.page, "input[name='feature.value'][type='number']")
        self.duration_unit = PageElement(self.page,
                                         "input[name='feature.value'][type='text']")
        self.response_status_code = PageElement(
            self.page, "input[name='feature.value.0.key']")
        self.max_age_value = PageElement(self.page,
                                         "input[name='feature.value.0.value'][type='number']")
        self.max_age_unit = PageElement(self.page,
                                        "input[name='feature.value.0.value'][type='text']")
        self.service_worker_max_age_value = PageElement(
            self.page, "input[name='feature.value'][type='number']")
        self.service_worker_max_age_unit = PageElement(
            self.page, "input[name='feature.value'][type='text']")
        self.ignore_origin_no_cache = PageElement(self.page,
                "//label[text()='Ignore no-cache headers when the origin returns one of these status codes:']/../div/input")
        self.cacheable_status_codes = PageElement(
            self.page, "//label[text()='Cacheable Status Codes']/../div/input")
        self.feature_value_input = PageElement(
            self.page, "input[name='feature.value']")
        self.proxy_special_headers_input = PageElement(
            self.page, "//label[text()='Proxy Special Headers']/../div/input")
        self.set_origin_input = PageElement(self.page,
                                            "//label[text()='Origin Name']/../div/input")


class EnvironmentVariables:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.env_variable_title = PageElement(self.page, "//h2[text()='Environment Variables']")
        self.add_env_variable_button = PageElement(self.page, "//button[text()='Add Environment Variable']")
        self.import_env_variable_button = PageElement(self.page, "//button[text()='Import Environment Variables']")
        self.the_key_field = PageElement(self.page, "//input[@id='key']")
        self.the_value_field = PageElement(self.page, "//div//textarea[@id='value']")
        self.keep_this_value_secret_checkbox = PageElement(self.page, "//span[@data-qa='secret-checkbox']")
        self.import_text_field = PageElement(self.page, "//div[@data-qa='import-textfield']//textarea[1]")
        self.add_variable_button = PageElement(self.page, "//button[text()='Add variable']")
        self.import_variables_text_area = PageElement(self.page, "//textarea[@id=':r1j:']")
        self.import_variables_button = PageElement(self.page, "//button[text()='Import Variables']")
        self.confirm_remove_var = PageElement(self.page, "//button[text()='Remove Variable']")
        self.row_key = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[1]")
        self.row_value = DynamicPageElement(self.page, "//table/tbody/tr[{row}]/td[2]")
        self.env_page = PageElement(self.page, "//span[text()='Environment Variables']")
        self.deploy_confirmation = PageElement(self.page, "//div[@role='dialog']//button[text()='Deploy Now']")



class OriginsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.origins_title = PageElement(self.page, "//h2[text()='Origins']")
        self.origin_row = ListElement(self.page, "//div[@data-qa='origin-block']")
        self.delete_origin_button_confirmation = PageElement(self.page, "//button[text()='Delete Origin']")
        self.origin_name_field = DynamicPageElement(self.page, "//input[@name='origins.{origin}.name']")
        self.origin_override_host_headers = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.override_host_header']")
        self.origin_hostname = DynamicPageElement(self.page, "//input[@name='origins.{origin}.hosts.{row}.hostname']")
        self.origin_scheme = DynamicPageElement(self.page, "//input[@name='origins.{origin}.hosts.{row}.scheme']")
        self.origin_port = DynamicPageElement(self.page, "//input[@name='origins.{origin}.hosts.{row}.port']")
        self.origin_ip_version_preference = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.hosts.{row}.dns_preference']")
        self.origin_add_host = PageElement(self.page, "//button[@data-qa='add-host-button']")
        self.origin_use_sni = ListElement(self.page, "//span[@data-qa='use-sni-checkbox']")
        self.allow_self_signed_certs = ListElement(self.page, "//span[@data-qa='allow-self-signed-certs-checkbox']")
        self.origin_use_the_following_sni_field = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.tls_verify.sni_hint_and_strict_san_check']")
        self.add_pin_button = PageElement(self.page, "(//button[@data-qa='add-pin-button'])[last()]")
        self.pinned_certs = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.tls_verify.pinned_certs.{row}.pinned_cert']")
        self.shields_drop_down = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.shields']")
        self.shields_row = PageElement(self.page, "//div[@data-qa='origin-shields-block']")
        self.add_origin_button = PageElement(self.page, "//button[@data-qa='add-origin-button']")
        self.origin_json_editor = PageElement(self.page, "//button[@data-qa='json-editor-button']")
        self.origin_editor = PageElement(self.page, "//button[@data-qa='origins-editor-button']")
        self.json_field = PageElement(self.page, "//div[@class='lines-content monaco-editor-background']")
        self.balancer_type = DynamicPageElement(self.page, "//input[@name='origins.{origin}.balancer']")