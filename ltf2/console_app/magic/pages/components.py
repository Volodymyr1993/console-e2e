"""
Classes that describe page elements
"""
from itertools import product

from playwright.sync_api import Page

from ltf2.console_app.magic.constants import ACCESS_CONTROL_TYPE, HTTP_METHODS
from ltf2.console_app.magic.elements import PageElement, UlElement, MembersTableElement, \
    TableElement, ListElement, DynamicPageElement, DynamicSelectElement, IframeElement


class LoginMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.email = PageElement(self.page, '#email')
        self.password = PageElement(self.page, '#password')
        self.submit = PageElement(self.page, 'button[type=submit]')
        self.error_message = PageElement(self.page, 'p.Mui-error')
        self.invalid_email_or_password_message = PageElement(
            self.page,
            'p.MuiTypography-colorError')
        self.login_successful = PageElement(self.page, '#client-snackbar')


class CommonMixin:
    """ Shared elements """
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        # General
        self.input_name = PageElement(self.page, 'input#name')
        self.client_snackbar = PageElement(self.page, '#client-snackbar')
        self.save = PageElement(self.page, "button :text('Save')")
        self.create = PageElement(self.page, "button :text('Create')")
        self.select = UlElement(self.page, "ul[role='listbox']")
        self.select_by_name = DynamicSelectElement(
            self.page, "//ul[@role='listbox']/li[text()='{name}']")
        # self.select_by_name = DynamicPageElement(self.page, "//ul[@role='listbox']/li[text()='{name}']")
        self.table = TableElement(self.page, "table")
        self.submit_button = PageElement(self.page, "button :text('Submit')")
        self.next_button = PageElement(self.page, "button :text('Next')")
        self.delete_button = PageElement(self.page, "button :text('Delete')")
        self.confirm_button = PageElement(self.page, "button :text('Confirm')")

        self.create_team_button = PageElement(self.page, "button :text('Create a team')")

        self.docs = PageElement(self.page, "li :text('Docs')")
        self.forums = PageElement(self.page, "li :text('Forums')")
        self.status = PageElement(self.page, "li :text('Status')")
        self.support = PageElement(self.page, "li :text('Support')")

        self.overview = PageElement(self.page, "div :text('Overview')")
        self.activity = PageElement(self.page, "div :text('Activity')")
        self.members = PageElement(self.page, "div :text-is('Members')")
        self.settings = PageElement(self.page, "div :text('Settings')")
        self.security = PageElement(self.page, "div :text-is('Security')")

        self.website_url = PageElement(self.page, '#url')
        self.launch_site = PageElement(self.page, "button :text('Launch my site')")

        # Create team dialog
        self.button_create_team_dialog = PageElement(
            self.page,
            'div[role="dialog"] button:has-text("Create a Team")')

        self.team_switcher_button = PageElement(self.page, '#team-switcher')
        self.team_switcher_list = UlElement(self.page, 'div:not([id="user-menu"]) div ul')
        self.delete_team_checkbox = PageElement(
            self.page,
            'div.MuiCardContent-root input[type="checkbox"]')
        self.delete_team_button = PageElement(self.page, "button :text('Delete Team')")

        self.visible_page_content = PageElement(self.page,
                                                '#__next:not([aria-hidden="true"])')
        self.status_iframe = PageElement(self.page, "iframe[title='Layer0 Status']")
        self.status_iframe_close_button = IframeElement(self.status_iframe,
                                                        'div .frame-close button')


class TeamMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.add_member_button = PageElement(self.page, "button :text('Add Members')")
        self.invite_member_button = PageElement(self.page,
                                                "button :text('Invite Members')")
        self.email = PageElement(self.page, '#email')
        self.plus_button = PageElement(self.page, "button[title='Add']")
        self.role_select_input = PageElement(
            self.page,
            'div[role="dialog"] input[name="role-select"]')
        self.role_select = UlElement(self.page, '#role-select-popup')

        self.members_table = MembersTableElement(self.page, "table")
        # Create property
        self.new_property_button = PageElement(self.page, "div :text('New Property')")
        self.origin_hostname_input = PageElement(
            self.page, "input[name='origins.0.hosts.0.hostname']")
        self.create_property_button = PageElement(self.page,
                                                  "div :text('Create Property')")


class EnvironmentMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.environments = PageElement(self.page, "div :text('Environments')")
        self.new_environment_button = PageElement(self.page,
                                                  "div :text('New Environment')")
        self.configuration = PageElement(self.page, "div :text('Configuration')")
        self.hostnames = PageElement(self.page, "div :text('Hostnames')")
        self.origins = PageElement(self.page, "div :text('Origins')")
        self.rules = PageElement(self.page, "div :text('Rules')")

        self.environment = DynamicPageElement(self.page, "a div :text('{name}')")
        self.revert_button = PageElement(self.page, "button :text('Revert')")
        self.revert_changes_button = PageElement(self.page,
                                                 "button :text('Revert changes')")
        # ======== Rules =========
        self.add_rule = PageElement(self.page, 'button :text("Add Rule")')
        self.add_condition = PageElement(self.page, 'button :text("Add Condition")')
        self.add_feature = PageElement(self.page, 'button :text("Add Feature")')
        self.delete_rule_list = ListElement(self.page,
                                            "//button[@data-qa='delete-button']")
        self.condition_operator_list = ListElement(
            self.page, "//div[contains(@class, 'MuiCollapse-entered')]//div[@role='button']")
        self.select_operator_name = DynamicSelectElement(
            self.page,
            "//div[@role='presentation' and not(@aria-hidden='true')]/div/ul[@role='menu']/li[text()='{name}']")
        self.delete_rule_button = PageElement(self.page, "button :text('Delete Rule')")
        self.add_feature_button = PageElement(
            self.page, "//button[@type='submit']/span[text()='Add Feature']")
        self.deploy_changes = PageElement(self.page, "button :text('Deploy Changes')")

        self.variable_input = PageElement(self.page,
                                          "//label[text()='Variable']/../div/input")
        self.variable_select = DynamicPageElement(
            self.page, "//div[text()='All Variables']/../ul/li//p[text()='{name}']")
        self.operator_input = PageElement(self.page,
                                          "//label[text()='Operator']/../div/input")
        self.rule_checkbox = PageElement(self.page, "//label//input[@type='checkbox']")
        self.code_input = PageElement(self.page, "input[name='feature.value.code']")
        self.name_input = PageElement(
            self.page, "//label[contains(text(), 'Name')]/..//div[@role='textbox']")
        self.value_div = PageElement(
            self.page, "//label[contains(text(), 'Value')]/..//div[@role='textbox']")
        self.method_value_input = PageElement(
            self.page, "//label[text()='Value']/../div/input")
        self.match_value_input = PageElement(
            self.page, "input[name='condition.matchValue']")
        self.add_condition_button = PageElement(
            self.page, "//button[@type='submit']/span[text()='Add Condition']")
        self.feature_input = PageElement(self.page,
                                         "input[placeholder='Search Features...']")
        self.feature_select = DynamicSelectElement(
            self.page,
            "//ul[@role='listbox']/li/div[text()='{type}']/../ul/li[text()='{name}']")
        self.header_name = PageElement(
            self.page,
            "//label[contains(text(), 'Header Name')]/..//div[@role='textbox']")
        self.response_headers = PageElement(
            self.page, "input[name='remove_response_headers']")
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
                                        "input[type='number']")
        self.response_headers = PageElement(
            self.page,
            "//label[text()='Response Headers']/../div/input")
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
        self.set_origin_input = PageElement(self.page, "//label[text()='Origin Name']/../div/input")


class ActivityMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        # TODO


class DeploymentsMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        # TODO


class SecurityMixin:
    def __init__(self, page: Page, url: str):
        super().__init__(page, url)
        self.event_logs = PageElement(self.page, "div :text('Logs')")
        self.security_application = PageElement(self.page,
                                                "div :text('Security Apps')")
        self.access_rules = PageElement(self.page, "div :text('Access Rules')")
        self.rate_rules = PageElement(self.page, "div :text('Rate Rules')")
        #self.bot_rules = PageElement(self.page, "div :text('Bot Rules')")
        #self.custom_rules = PageElement(self.page, "div :text('Custom Rules')")
        self.managed_rules = PageElement(self.page, "div :text('Managed Rules')")

        self.add_rule = PageElement(self.page, "button :text('Add Rule')")
        self.no_data_to_display = PageElement(self.page, "div :text('No data to display')")

        # ========= Rate Rules ======

        self.input_num = PageElement(self.page, 'input#num')
        self.add_rate_rule = PageElement(self.page, "button :text('Add Rate Rule')")
        self.rate_new_condition_group = PageElement(self.page, "button :text-is('New Condition Group')")
        self.rate_new_condition = PageElement(self.page, 'button :text-is("New Condition")')
        self.rate_add_condition_value = PageElement(self.page, 'input[placeholder="Add..."]')
        self.match_condition_input = DynamicPageElement(self.page,
            'input[name="conditionGroups[{group}].conditions[{condition}].target.type"]')
        self.match_req_header_input = PageElement(self.page, 'input[placeholder="Type or select header name"]')

        # ======== Managed Rules ==========

        self.add_managed_rule = PageElement(self.page, "button :text('Add Managed Rule')")

        # Ignore list
        self.header_name_input = PageElement(
            self.page, "input[name='generalSettings.responseHeaderName']")
        self.ignore_cookies_input = PageElement(
            self.page, "input[name='generalSettings.ignoreCookie']")
        self.ignore_cookies_buttons = ListElement(
            self.page,
            "//input[@name='generalSettings.ignoreCookie']/..//div[@role='button']")
        self.ignore_header_input = PageElement(
            self.page, "input[name='generalSettings.ignoreHeader']")
        self.ignore_header_buttons = ListElement(
            self.page,
            "//input[@name='generalSettings.ignoreHeader']/..//div[@role='button']")
        self.ignore_query_args_input = PageElement(
            self.page, "input[name='generalSettings.ignoreQueryArgs']")
        self.ignore_query_args_buttons = ListElement(
            self.page,
            "//input[@name='generalSettings.ignoreQueryArgs']/../div[@role='button']")

        # More Details
        self.more_details = PageElement(self.page, "span:has-text('More Details')")
        self.max_args_reqs_input = PageElement(self.page,
                                               "input[name='generalSettings.maxNumArgs']")
        self.single_arg_length_input = PageElement(
            self.page, "input[name='generalSettings.argLength']")
        self.arg_name_length_input = PageElement(
            self.page, "input[name='generalSettings.argNameLength']")
        self.total_arg_length_input = PageElement(
            self.page, "input[name='generalSettings.totalArgLength']")
        self.max_file_size_input = PageElement(
            self.page, "input[name='generalSettings.maxFileSize']")
        self.json_parser_input = PageElement(
            self.page, "input[name='generalSettings.jsonParser']")

        # Policies
        self.policies = PageElement(self.page, "button :text('Policies')")
        self.ruleset_input = PageElement(self.page, "input[name='rulesetVersion']")
        self.ruleset_select = UlElement(self.page, "ul[role='listbox'] ul")
        self.threshold_input = PageElement(self.page,
                                           "input[name='generalSettings.anomalyThreshold']")
        self.paranoia_level_input = PageElement(
            self.page, "input[name='generalSettings.paranoiaLevel']")
        self.ruleset_switch = PageElement(self.page, "input[name='rulesetswitch']")

        # Exceptions
        self.exceptions = PageElement(self.page, "button :text('Exceptions')")
        self.add_condition = PageElement(self.page, "button :text('Add New Condition')")
        self.rule_ids = PageElement(self.page,
                                    "input[name='ruleTargetUpdates[0].ruleIds']")
        self.parameter_input = PageElement(self.page,
                                               "input[name='ruleTargetUpdates[0].target']")
        self.condition_name = PageElement(self.page,
                                          "input[name='ruleTargetUpdates[0].targetMatch']")
        self.regex_switch = PageElement(self.page, "input[name='regexSwitch']")
        self.rule_ids_buttons = ListElement(
            self.page,
            "//input[@name='ruleTargetUpdates[0].ruleIds']/..//div[@role='button']")

        self.conditions = ListElement(
            self.page, "//button[span='Add New Condition']/../../../button")

        # ============= Security application manager ============

        self.add_new = PageElement(self.page, "button :text('Add new')")
        self.host_input = PageElement(self.page, "input[name='host.type']")
        self.host_values_input = PageElement(self.page, "input[name='host.values']")
        self.host_values_buttons = PageElement(
            self.page, "//input[@name='host.values']/..//div[@role='button']")
        self.url_path_input = PageElement(self.page, "input[name='path.type']")
        self.url_values_input = PageElement(self.page, "input[name='path.values']")
        self.url_values_buttons = PageElement(
            self.page, "//input[@name='path.values']/..//div[@role='button']")
        self.host_negative_match_checkbox = PageElement(
            self.page, "input[name='host.isNegated']")
        self.path_negative_match_checkbox = PageElement(
            self.page, "input[name='path.isNegated']")
        self.accept_all_changes = PageElement(self.page,
                                              "button :text('Accept All Changes')")
        # Access Rules
        self.config_access_rules = PageElement(
            self.page,
            "div[aria-label='Managed rule exceptions'] button:has-text('Access Rule')")
        self.prod_access_rule_input = PageElement(self.page, "input[name='aclProdId']")
        self.action_access_rule_input = PageElement(self.page, "input[name='aclProdAction.enfType']")
        self.audit_access_rule_input = PageElement(self.page, "input[name='aclAuditId']")

        # Rate rules
        self.config_rate_rules = PageElement(
            self.page,
            "div[aria-label='Managed rule exceptions'] button:has-text('Rate Rules')")
        self.prod_rate_rule_input = PageElement(self.page,
                                                "input[placeholder='Add Rate Rule']")
        # Custom Rules
        self.config_custom_rules = PageElement(
            self.page,
            "div[aria-label='Managed rule exceptions'] button:has-text('Custom Rule')")
        self.prod_custom_rule_input = PageElement(self.page, "input[name='rulesProdId']")
        self.action_custom_rule_input = PageElement(self.page,
                                                    "input[name='rulesProdAction.enfType']")
        self.audit_custom_rule_input = PageElement(self.page, "input[name='rulesAuditId']")
        # Managed Rules
        self.config_managed_rules = PageElement(
            self.page,
            "div[aria-label='Managed rule exceptions'] button:has-text('Managed Rule')")
        self.prod_managed_rule_input = PageElement(self.page, "input[name='rulesProdId']")
        self.action_managed_rule_input = PageElement(self.page, "input[name='rulesProdAction.enfType']")
        self.audit_managed_rule_input = PageElement(self.page, "input[name='rulesAuditId']")
        # Bot Rules
        self.config_bot_rules = PageElement(
            self.page,
            "div[aria-label='Managed rule exceptions'] button:has-text('Bot Rule')")
        self.prod_bot_rule_input = PageElement(self.page, "input[name='botsProdId']")
        self.action_bot_rule_input = PageElement(self.page,
                                                 "input[name='botsProdAction.enfType']")
        self.status_bot_rule_input = PageElement(self.page,
                                                 "input[name='botsProdAction.status']")
        self.valid_bot_rule_input = PageElement(self.page,
                                                "input[name='botsProdAction.validForSec']")

        # ================= Access Rules ==========

        self.add_access_rule = PageElement(self.page, "button :text('Add Access Rule')")
        # Access Control
        self.access_control_input = PageElement(self.page,
                                                "input[name='access-control-dropdown']")
        self.whitelist = PageElement(self.page, "button :text('whitelist')")
        self.blacklist = PageElement(self.page, "button :text('blacklist')")
        self.accesslist = PageElement(self.page, "button :text('accesslist')")
        # Create Access Control inputs for dropdown list
        for type_title, list_ in product(ACCESS_CONTROL_TYPE,
                                   ('whitelist', 'blacklist', 'accesslist')):
            type_id = ACCESS_CONTROL_TYPE[type_title]
            # Inputs
            setattr(self,
                    f'{type_id.lower()}_{list_}_input',
                    PageElement(self.page, f"input[name='{type_id}.{list_}']"))
            # Buttons
            setattr(self,
                    f'{type_id.lower()}_{list_}',
                    PageElement(self.page, f"//p[span='{type_title}']/../../../..//p[span='{list_}']"))
            # Saved input values
            setattr(self,
                    f'{type_id.lower()}_{list_}_values',
                    ListElement(self.page, f"//p[span='{type_title}']/../../../..//div[@role='button']/span"))

        # Allowed HTTP Methods
        for method in HTTP_METHODS:
            setattr(self,
                    f'method_{method.lower()}',
                    PageElement(self.page, f"input[value='{method}']"))

        self.other_methods = PageElement(self.page, "input[name='other http methods']")
        self.other_methods_buttons = ListElement(
            self.page, 'div[placeholder="Add..."] div[role="button"]')

        self.response_header_name = PageElement(self.page,
                                                "input[name='responseHeaderName']")
        self.upload_limit = PageElement(self.page, "input[name='maxFileSize']")
        self.request_content_type = PageElement(self.page,
                                                "input[name='allowedRequestContentTypes']")
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
                                               "input[name='disallowedExtensions']")
        self.extension_blacklist_buttons = ListElement(
            self.page, "//label[text()='Extension Blacklist']/..//div[@role='button']")
        self.extension_blacklist_clear = ListElement(
            self.page,
            "//label[text()='Extension Blacklist']/..//button[@title='Clear']")
        self.header_blacklist = PageElement(self.page, "input[name='disallowedHeaders']")
        self.header_blacklist_buttons = ListElement(
            self.page,
            "//label[text()='Header Blacklist']/..//div[@role='button']")
        self.header_blacklist_clear = ListElement(
            self.page,
            "//label[text()='Header Blacklist']/..//button[@title='Clear']")

        # =========== Bot Rules =============

        self.add_bot_rule = PageElement(self.page, "button :text('Add Bot Rule')")
        self.rule_type_input = DynamicPageElement(
            self.page, 'input[name="directive[{directive}].include"]')
        self.bot_rule_name_input = DynamicPageElement(
            self.page, 'input[name="directive[{directive}].name"]')
        self.bot_rule_msg = DynamicPageElement(
            self.page, 'input[name="directive[{directive}].actionMsg"]')

        self.bot_condition_variable = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].variable[0].type"]')
        self.bot_condition_count = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].variable[0].isCount"]')
        self.bot_condition_operator = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].operatorType"]')
        self.add_match = PageElement(self.page, "button :text('Add Match')")
        self.bot_condition_match = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].operatorValue"]')
        self.bot_condition_match_name = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].variable[0].match[{match}].value"]')

        # =========== Custom Rules =============

        self.add_custom_rule = PageElement(self.page, "button :text('Add Custom Rule')")

        self.custom_rule_name = DynamicPageElement(
            self.page, 'input[name="directive[{directive}].name"]')
        self.custom_rule_id = DynamicPageElement(
            self.page, 'input[name="directive[{directive}].actionId"]')
        self.custom_rule_msg = DynamicPageElement(
            self.page, 'input[name="directive[{directive}].actionMsg"]')
        self.custom_variable_count = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].variable[{variable}].isCount"]')
        self.custom_variable = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].variable[{variable}].type"]')
        self.custom_condition_operator = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].operatorType"]')
        self.custom_condition_operator_value = DynamicPageElement(
            self.page,
            'input[name="directive[{directive}].conditions[{condition}].operatorValue"]')

        # ==================== Dashboard & Event Logs ==============

        self.time_frame_input = PageElement(self.page, "input[name='time']")
        self.view_input = PageElement(self.page, "input[name='view']")
        self.refresh_input = PageElement(self.page, "input[name='refresh']")

        self.threats_button = PageElement(self.page, "button :text('Threats')")
        self.browser_challenges_button = PageElement(self.page,
                                                     "button :text('Browser Challenges')")
        self.rates_button = PageElement(self.page, "button :text('Rates')")
        self.rate_enforcement_button = PageElement(self.page,
                                                   "button :text('Rate Enforcement')")
        # Advanced filters
        self.field_input = PageElement(self.page, "input[name='field']")
        self.value_input = PageElement(self.page, "input[name='value']")

        self.add_filter_button = PageElement(self.page, "button :text('Add Filter')")
        self.filter_names = ListElement(self.page,
                                        "//div[p[contains(., 'Filters:')]]//div//p")
        self.filter_remove = ListElement(self.page,
                                         "//div[p[contains(., 'Filters:')]]//button")
        self.current_time = PageElement(self.page, "//h3/span")
