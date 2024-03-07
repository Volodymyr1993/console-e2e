"""
Classes that describe page elements
"""
from itertools import product

from playwright.sync_api import Page

from ltf2.console_app.magic.constants import ACCESS_CONTROL_TYPE, HTTP_METHODS
from ltf2.console_app.magic.elements import PageElement, UlElement, MembersTableElement, \
    TableElement, ListElement, DynamicPageElement, DynamicSelectElement, IframeElement, \
    CreatedRuleElement, DynamicRateConditions, DynamicIndexElement


class LoginMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.login_button = PageElement(self.page, "//button//span[text()='Login']")
        self.username = PageElement(self.page, "//input[@id='username']")
        self.password = PageElement(self.page, "//input[@id='password']")
        self.next_button = PageElement(self.page, "//button//span[text()='Next']")
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
        self.client_snackbar = PageElement(self.page, "//*[@id='client-snackbar']")
        self.apply = PageElement(self.page, "//button//span[text()='Apply']")
        self.save = PageElement(self.page, "//button//span[text()='Save']")
        self.create = PageElement(self.page, "//button//span[text()='Create']")
        self.close = PageElement(self.page, "//button//span[text()='Close']").nth(1)
        self.cancel_button = PageElement(self.page, "//span[text()='Cancel']")
        self.select = UlElement(self.page, "//ul[@role='listbox']")
        self.select_by_name = DynamicSelectElement(
            self.page, "//ul[@role='listbox']/li[text()='{name}']")
        # self.select_by_name = DynamicPageElement(self.page, "//ul[@role='listbox']/li[text()='{name}']")
        self.table = TableElement(self.page, "//table")
        self.submit_button = PageElement(self.page, "//button//span[text()='Submit']")
        self.delete_button = PageElement(self.page, "//button//span[text()='Delete']")
        self.confirm_button = PageElement(self.page, "//button//span[text()='Confirm']")
        self.revert_button = PageElement(self.page, "//button[./*[text()='Revert']]")
        self.revert_confirm_button = PageElement(self.page, "//button[./*[text()='Revert Changes']]")
        self.delete_button_list = ListElement(self.page,"//button[@data-qa='delete-button']")
        self.deploy_changes_button = PageElement(self.page, "//button//*[text()='Deploy Changes']")
        self.create_org_button = PageElement(self.page, "//span[text()='Create an Organization']")

        self.docs = PageElement(self.page, "//li[text()='Docs']")
        self.forums = PageElement(self.page, "//li[text()='Forums']")
        self.status = PageElement(self.page, "//li[text()='Status']")
        self.support = PageElement(self.page, "//li[text()='Support']")

        self.overview = PageElement(self.page, "//span[text()='Overview']")
        self.activity = PageElement(self.page, "//span[text()='Activity']")
        self.members = PageElement(self.page, "//span[text()='Members']")
        self.settings = PageElement(self.page, "//span[text()='Settings']")
        self.security = PageElement(self.page, "//div/span[text()='Security']")

        # Create organization dialog
        self.button_create_org_dialog = PageElement(
            self.page,
            '//div[@role="dialog"]//span[text()="Create an Organization"]')

        self.org_switcher_button = PageElement(self.page, "//button[@id='organization-switcher']")
        self.org_switcher_list = UlElement(self.page, "//ul[@role='menu']")
        self.delete_org_checkbox = PageElement(
            self.page,
            "//span[text()='Confirm that I want to delete this organization.']/../..//input[@type='checkbox']")
        self.delete_org_button = PageElement(self.page, "//span[text()='Delete Organization']")

        self.visible_page_content = PageElement(self.page,
                                                "//div[@id='__next' and not(@aria-hidden='true')]")
        self.status_iframe = PageElement(self.page, "//iframe[@title='Layer0 Status']")
        self.status_iframe_close_button = IframeElement(self.status_iframe,
                                                        "//div[contains(@class, 'frame-close')]//button")
        self.status_snackbar_close = PageElement(self.page, "//div[@aria-describedby='client-snackbar']//button")


class OrgMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.add_member_button = PageElement(self.page, "//button//span[text()='Add Member']")
        self.invite_member_button = PageElement(self.page,
                                                "//button//span[text()='Invite']")
        self.member_permission = DynamicPageElement(self.page, "//div/p/span[text()='{role}']")
        self.email = PageElement(self.page, "//input[@id='email']")
        self.plus_button = PageElement(self.page, "//button[@title='Add']")

        self.members_table = MembersTableElement(self.page, "//table")
        self.selected_org = DynamicPageElement(self.page,
                                               "//header//p[text()='{name}']")
        # Create property
        self.new_property_button = PageElement(self.page, "//span[text()='New Property']")
        self.origin_hostname_input = PageElement(
            self.page, "//input[@name='origins.0.hosts.0.hostname']")
        self.create_property_button = PageElement(self.page,
                                                  "//span[text()='Create Property']")


class EnvironmentMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.environments = PageElement(self.page, "//span[text()='Environments']")
        self.new_environment_button = PageElement(self.page,
                                                  "//span[text()='New Environment']")
        self.configuration = PageElement(self.page, "//span[text()='Configuration']")
        self.hostnames = PageElement(self.page, "//span[text()='Hostnames']")
        self.origins = PageElement(self.page, "//span[text()='Origins']")
        self.rules = PageElement(self.page, "//span[text()='Rules']")

        self.environment = DynamicPageElement(self.page, "//a/div[@role='button']//span[text()='{name}']")
        self.revert_button = PageElement(self.page, "//button//span[text()='Revert']")
        self.revert_changes_button = PageElement(self.page,
                                                 "//button//span[text()='Revert Changes']")
        # ======== Rules =========
        self.add_rule = PageElement(self.page, "//button//span[text()='Add Rule']")
        self.add_element = PageElement(self.page, "//button//span[text()='Add']")
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
        self.delete_rule_button = PageElement(self.page, "//button//span[text()='Delete Rule']")
        self.add_feature_button = PageElement(
            self.page, "//button[@type='submit']/span[text()='Add Feature']")
        self.deploy_changes = PageElement(self.page, "//button//span[text()='Deploy Changes']")

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
            self.page, "//button[@type='submit']/span[text()='Add Condition']")
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
                                                 "//button//span[text()='Add an Expression']")
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
                                             "//button//span[text()='Add Rule Using AI...']")
        self.add_rule_using_ai_input = PageElement(
            self.page, "//input[@data-qa='add-rule-using-ai-text']")
        self.generate_rule = PageElement(self.page, "//button//span[text()='Generate Rule']")
        self.created_rule = CreatedRuleElement(
            self.page,
            "((//div[@data-qa='rule-conditions'])[{rule_num}]//div[@data-qa='rule-condition'])[{{num}}]",
            "((//div[@data-qa='rule-features'])[{rule_num}]//div[@data-qa='rule-feature'])[{{num}}]")
        self.single_condition = ListElement(self.page, "//div[@data-qa='rule-condition']")
        self.rule_div = PageElement(self.page,
                                    "//form/div/div/div[@data-rbd-draggable-context-id]")
        self.nested_rule_add_element_button = DynamicPageElement(
            self.page,
            "((//div[@data-rbd-droppable-id='{id}']/div)[{num}]//button[span='Add'])[last()]")
        self.rule_add_element_button = DynamicIndexElement(
            self.page,
            "(//form/div/div/div[@data-rbd-draggable-id][{num}]//button[span='Add'])[last()]")
        self.ai_rule_generation_error = PageElement(self.page,
                                                    "//p[contains(@class, 'MuiTypography-colorError')]")
        # ====== Cache =====

        self.purge_the_cache = PageElement(self.page,
                                           "//button//span[text()='Purge the Cache...']")
        self.purge_cache = PageElement(self.page, "//button//span[text()='Purge Cache']")
        self.purge = PageElement(self.page, "//button//span[text()='Purge']")
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
        self.date_picker_apply_button = PageElement(self.page, "//span[text()='Apply']")

        # Traffic Overview elements
        self.traffic_header = PageElement(self.page, "//h2/span[text()='Traffic']")
        self.traffic_overview_tab_button = PageElement(self.page,
            "//button[@role='tab']/..//span[text()='Overview']")
        self.traffic_metric_selector = PageElement(self.page,
            '//input[@data-qa="data-usage-metricsSelector"]')
        self.traffic_requests_grid_summary = PageElement(self.page,
            "//div[@data-qa='urls-chart']//span[contains(text(), 'Requests')]")
        self.traffic_errors_grid_summary = PageElement(self.page,
            '//div[@data-qa="errors-card"]//span[contains(text(), "Errors")]')
        self.traffic_rules_grid_summary = PageElement(self.page,
            '//div[@class="MuiCardHeader-content"]//span[text()="Rules"]')
        self.traffic_rules_metric_selector = PageElement(self.page,
            '//input[@data-qa="rules-metricsSelector"]')
        self.traffic_rules_percentile_selector = PageElement(self.page,
            '//input[@data-qa="rules-percentilesSelector"]')
        self.traffic_origin_latency_over_time_summary = PageElement(self.page,
            '//div[@data-qa="urls-chart"]//span[text()="Origin Latency Over Time"]')
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
        self.traffic_main_chart_summary = PageElement(self.page, "//span[@data-qa='data-usage-summary']")
        self.traffic_rules_coulumn_with_metrics_data = PageElement(self.page,
            '//table//tr//th[10]//span[@aria-disabled]')
        # By Country tab elements
        self.country_tab = PageElement(self.page, "//div[@role='tablist']//span[contains(text(), 'By Country')]")
        self.country_map = PageElement(self.page, "//div[@data-qa='geo-map']")
        self.country_metric_selector = PageElement(self.page,
            '//input[@data-qa="geo-metricsSelector"]')
        self.country_percentile_selector = PageElement(self.page,
            '//input[@data-qa="geo-percentilesSelector"]')
        self.country_tab_origin_latency_by_country_grid = PageElement(self.page,
            "//div[@data-qa='geo-table']//span[text()='Origin Latency by Country']")


class RedirectsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.add_a_redirect_button = PageElement(self.page, "//button[@data-qa='redirect-add-btn']")
        self.remove_selected_redirect = PageElement(self.page, "//button[@data-qa='redirect-remove-btn']")
        self.confirm_remove_redirect = PageElement(self.page, "//span[text()='Remove ']")
        self.search_field = PageElement(self.page, "//input[@id='search']")
        self.default_status_dropdown = PageElement(self.page, "//div[@data-qa='redirect-default-status-picker']")
        self.import_button = PageElement(self.page, "//button[@data-qa='redirect-import-btn']")
        self.export_button = PageElement(self.page, "//button[@data-qa='redirect-export-btn']")
        self.redirect_from = PageElement(self.page, "//input[@id='from']")
        self.redirect_to = PageElement(self.page, "//input[@id='to']")
        self.response_status = PageElement(self.page, "//div[@data-qa='redirect-status-picker']//div[@role='button']")
        self.forward_query_string = PageElement(self.page, "//span[@data-qa='redirect-forward-query-string-checkbox']")
        self.save_redirect_button = PageElement(self.page, "//button[@data-qa='redirect-add-save-popup-btn']")
        self.import_override_existing = PageElement(self.page, "//span[text()='Override existing list with file content']")
        self.import_append_file = PageElement(self.page, "//span[text()='Append file content to existing redirects list']")
        self.upload_redirect_button = PageElement(self.page, "//span[text()='Upload redirects']")
        self.redeploy_button = PageElement(self.page, "//button[@data-qa='redeploy-btn']")
        self.redeploy_confirmation = PageElement(self.page, "//div[@role='dialog']//span[contains(text(), 'Deploy Now')]")
        self.delete_all_checkbox = PageElement(self.page, "//table//tr//th//input[@type='checkbox']")
        self.first_checkbox_from_the_table = PageElement(self.page, "//table//tbody//td//input[@type='checkbox']")
        self.empty_list_message = PageElement(self.page, "//div[text()='This environment has no redirects']")
        self.table_value_from_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[2]")
        self.table_value_to_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[3]")
        self.table_value_status_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[4]")
        self.table_value_query_field = DynamicPageElement(self.page, "//table//tbody//tr[{row}]//td[5]")
        self.import_browse_button = PageElement(self.page, "//button[@data-qa='redirect-import-browse-btn']")
        self.redirects_page = PageElement(self.page, "//span[text()='Redirects']")
        self.online_status = PageElement(self.page, "//i[text()='Deployed']")
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
        self.event_logs = PageElement(self.page, "//span[text()='Logs']")
        self.security_application = PageElement(self.page,
                                                "//span[text()='Security Apps']")
        self.dashboard = PageElement(self.page, "//span[text()='Dashboard']")
        self.rules_manager = PageElement(self.page, "//span[text()='Rules Manager']")
        self.access_rules = PageElement(self.page, "//span[text()='Access Rules']")
        self.rate_rules = PageElement(self.page, "//span[text()='Rate Rules']")
        self.bot_rules = PageElement(self.page, "//span[text()='Bot Rules']")
        self.custom_rules = PageElement(self.page, "//span[text()='Custom Rules']")
        self.managed_rules = PageElement(self.page, "//span[text()='Managed Rules']")

        self.add_rule = PageElement(self.page, "//button//span[text()='Add Rule']")
        self.no_data_to_display = PageElement(self.page, "//div[text()='No data to display']")

        # ========= Rate Rules ======

        self.input_num = PageElement(self.page, "//input[@id='num']")
        self.add_rate_rule = PageElement(self.page, "//button//span[text()='New Rate Ruleset']")
        self.rate_new_condition_group = PageElement(
            self.page,"//button//span[text()='New Condition Group']")
        self.rate_new_condition = PageElement(self.page, "//button//span[text()= 'New Condition']")
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

        self.add_managed_rule = PageElement(self.page, "//button//span[text()='New Managed Ruleset']")

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
        self.more_details = PageElement(self.page, "//span[text()='More Details']")
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
        self.policies = PageElement(self.page, "//button//span[text()='Inbound Policies']")
        self.ruleset_input = PageElement(self.page, "//input[@name='rulesetVersion']")
        self.ruleset_select = UlElement(self.page, "//ul[@role='listbox']//ul")
        self.threshold_input = PageElement(self.page,
                                           "//input[@name='generalSettings.anomalyThreshold']")
        self.paranoia_level_input = PageElement(
            self.page, "//input[@name='generalSettings.paranoiaLevel']")
        self.ruleset_switch = PageElement(self.page, "//input[@name='rulesetswitch']")
        # Exceptions
        self.exceptions = PageElement(self.page, "//button//span[text()='Exceptions']")
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
        self.save_secapp = PageElement(
            self.page,
            "//div[text()='You have unsaved changes.']/../..//span[text()='Save']")
        self.new_seccurity_application = PageElement(
            self.page, "//button//span[text()='New Security Application']")
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
        # Custom Rules
        self.config_custom_rules = PageElement(
            self.page,
            "//div[@aria-label='Managed rule exceptions']//button[text()='Custom Rule']")
        self.prod_custom_rule_input = PageElement(self.page, "//input[@name='rulesProdId']")
        self.action_custom_rule_input = PageElement(self.page,
                                                    "//input[@name='rulesProdAction.enfType']")
        self.audit_custom_rule_input = PageElement(self.page, "//input[@name='rulesAuditId']")
        # Managed Rules
        self.config_managed_rules = PageElement(
            self.page,
            "//div[@aria-label='Managed rule exceptions']//button[text()='Managed Rule']")
        self.prod_managed_rule_input = PageElement(self.page, "//input[@name='rulesProdId']")
        self.action_managed_rule_input = PageElement(self.page, "//input[@name='rulesProdAction.enfType']")
        self.audit_managed_rule_input = PageElement(self.page, "//input[@name='rulesAuditId']")
        # Bot Rules
        self.config_bot_rules = PageElement(
            self.page,
            "//div[@aria-label='Managed rule exceptions']//button[text()='Bot Rule']")
        self.prod_bot_rule_input = PageElement(self.page, "//input[@name='botsProdId']")
        self.action_bot_rule_input = PageElement(self.page,
                                                 "//input[@name='botsProdAction.enfType']")
        self.status_bot_rule_input = PageElement(self.page,
                                                 "//input[@name='botsProdAction.status']")
        self.valid_bot_rule_input = PageElement(self.page,
                                                "//input[@name='botsProdAction.validForSec']")

        # ================= Access Rules ==========

        self.add_access_rule = PageElement(self.page, "//button//span[text()='New Access Ruleset']")
        # Access Control
        self.access_control_input = PageElement(self.page,
                                                "//input[@name='access-control-dropdown']")
        self.whitelist = PageElement(self.page, "//button//span[text()='whitelist']")
        self.blacklist = PageElement(self.page, "//button//span[text()='blacklist']")
        self.accesslist = PageElement(self.page, "//button//span[text()='accesslist']")
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
                    PageElement(self.page, f"//p[span='{type_title}']/../../../..//p[span='{list_}']"))
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

        # =========== Bot Rules =============

        self.add_bot_rule = PageElement(self.page, "button :text('Add Bot Rule')")
        self.rule_type_input = DynamicPageElement(
            self.page, '//input[@name="directive[{directive}].include"]')
        self.bot_rule_name_input = DynamicPageElement(
            self.page, '//input[@name="directive[{directive}].name"]')
        self.bot_rule_msg = DynamicPageElement(
            self.page, '//input[@name="directive[{directive}].actionMsg"]')

        self.bot_condition_variable = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].variable[0].type"]')
        self.bot_condition_count = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].variable[0].isCount"]')
        self.bot_condition_operator = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].operatorType"]')
        self.add_match = PageElement(self.page, "//button//span[text()='Add Match']")
        self.bot_condition_match = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].operatorValue"]')
        self.bot_condition_match_name = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].variable[0].match[{match}].value"]')

        # =========== Custom Rules =============

        self.add_custom_rule = PageElement(self.page, "//button[text()='Add Custom Rule']")

        self.custom_rule_name = DynamicPageElement(
            self.page, '//input[@name="directive[{directive}].name"]')
        self.custom_rule_id = DynamicPageElement(
            self.page, '//input[@name="directive[{directive}].actionId"]')
        self.custom_rule_msg = DynamicPageElement(
            self.page, '//input[@name="directive[{directive}].actionMsg"]')
        self.custom_variable_count = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].variable[{variable}].isCount"]')
        self.custom_variable = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].variable[{variable}].type"]')
        self.custom_condition_operator = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].operatorType"]')
        self.custom_condition_operator_value = DynamicPageElement(
            self.page,
            '//input[@name="directive[{directive}].conditions[{condition}].operatorValue"]')

        # ==================== Dashboard & Event Logs ==============

        self.dashboard_time_frame_input = PageElement(
            self.page, "//input[@id='time']")
        self.view_input = PageElement(self.page, "//input[@name='view']")
        self.refresh_input = PageElement(self.page, "//input[@name='refresh']")

        self.threats_button = PageElement(self.page, "//button//span[text()='Threats']")
        self.browser_challenges_button = PageElement(self.page,
                                                     "//button//span[text()='Browser Challenges']")
        self.rates_button = PageElement(self.page, "//button//span[text()='Rates']")
        self.rate_enforcement_button = PageElement(self.page,
                                                   "//button//span[text()='Rate Enforcement']")
        # Advanced filters
        self.add_edit_filters = PageElement(self.page, "//button//span[text()='Edit/Add Filters']")
        self.add_filter = PageElement(self.page, "//button//span[text()='Add Filter']")

        self.field_input = PageElement(self.page, "//input[@placeholder='Select Field']")
        self.value_input = PageElement(self.page, "//input[@name='domain']")

        self.filter_names = ListElement(
            self.page,
            "//div[contains(@class, 'MuiGrid-container')]/div[contains(@class, 'MuiGrid-item')]/div[@role='button']")
        self.filter_remove = ListElement(self.page,
                                         "//div[p[contains(., 'Filters:')]]//button")
        self.dashboard_current_time = PageElement(
            self.page, "//h2[contains(text(), 'Security')]/../h6")


class ExperimentsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.experiments_title = PageElement(self.page, "//h2/*[text()='Experimentation']")
        self.add_experiment_button = PageElement(self.page,
                                                 "//button//*[text()='Add Experiment']")
        # === Experiment parameters ===
        self.experiment_name = DynamicPageElement(self.page, "//*[text()='Experiment: ']/..//b[text()='{name}']")
        self.experiment_name_input = DynamicPageElement(self.page, "//input[@id='experiments.{id}.name']")
        self.variant_name_input = DynamicPageElement(self.page, "//input[@id='experiments.{exp_id}.variants.{var_id}.name']")
        self.variant_percentage_input = DynamicPageElement(self.page, "//input[@id='experiments.{exp_id}.variants.{var_id}.weight']")
        self.add_variant_button = PageElement(self.page, "//button[./*[text()='Add Variant']]")
        self.delete_experiment_button = PageElement(self.page, "(//button[@data-qa='delete-button'])[1]")
        self.delete_experiment_list = ListElement(self.page,
                                            "//button[@data-qa='delete-button']")
        self.is_active_checkbox_list = ListElement(self.page, "//form//input[@type='checkbox']")
        self.delete_experiment_confirm_button = PageElement(self.page, "//button//*[text()='Delete experiment']")
        self.wrong_percentage_message = PageElement(self.page, "//*[text()='Percentage total have to be 100']")
        # === Conditions ===
        self.add_criteria_button = PageElement(self.page, "//button[.//text()='Add Criteria']")
        self.add_condition_button = PageElement(self.page, "//button[./*[text()='Add Condition']]")
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
        self.add_feature_confirm_button = PageElement(self.page, "//button[./*[text()='Add Feature']]")
        self.feature_input = PageElement(self.page,
                                         "input[placeholder='Search Features...']")
        self.feature_select = DynamicSelectElement(
            self.page,
            "//ul[@role='listbox']/li/div[text()='{type}']/../ul/li[text()='{name}']")
        self.header_name = PageElement(
            self.page,
            "//label[contains(text(), 'Header Name')]/..//div[@role='textbox']")
        self.add_action_button = PageElement(self.page, "(//button[./*[text()='Add Action']])[1]")
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


class OriginsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.origins_title = PageElement(self.page, "//h2/*[text()='Origins']")
        self.delete_origin_button_confirmation = PageElement(self.page, "//span[text()='Delete Origin']")
        self.origin_name_field = DynamicPageElement(self.page, "//input[@name='origins.{origin}.name']")
        self.origin_override_host_headers = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.override_host_header']")
        self.origin_hostname = DynamicPageElement(self.page, "//input[@name='origins.{origin}.hosts.{row}.hostname']")
        self.origin_scheme = DynamicPageElement(self.page, "//input[@name='origins.{origin}.hosts.{row}.scheme']")
        self.origin_port = DynamicPageElement(self.page, "//input[@name='origins.{origin}.hosts.{row}.port']")
        self.origin_ip_version_preference = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.hosts.{row}.dns_preference']")
        self.origin_add_host = PageElement(self.page, "//button//span[text()='Add Host']")
        self.origin_use_sni = ListElement(self.page, "//input[@type='checkbox']")
        self.origin_use_the_following_sni_field = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.tls_verify.sni_hint_and_strict_san_check']")
        self.add_pin_button = PageElement(self.page, "//button//span[text()='Add Pin']")
        self.pinned_certs = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.tls_verify.pinned_certs.{row}.pinned_cert']")
        self.shields_drop_down = DynamicPageElement(
            self.page, "//input[@name='origins.{origin}.shields']")
        self.shields_row = PageElement(self.page, "//div[text()='Shields']")
        self.add_origin_button = PageElement(self.page, "//button//span[text()='Add Origin']")
        self.origin_json_editor = PageElement(self.page, "//button//span[text()='JSON Editor']")
        self.origin_editor = PageElement(self.page, "//button//span[text()='Origins Editor']")
        self.json_field = PageElement(self.page, "//div[@class='lines-content monaco-editor-background']")
        self.balancer_type = DynamicPageElement(self.page, "//input[@name='origins.{origin}.balancer']")