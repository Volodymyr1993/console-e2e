import time
from datetime import datetime, timezone

import pytest
from playwright.sync_api import TimeoutError

from ltf2.console_app.magic.helpers import random_str, open_rule_editor
from ltf2.console_app.magic.pages.pages import SecurityPage
from ltf2.console_app.magic.constants import ACCESS_CONTROL_TYPE, HTTP_METHODS


open_access_rule = lambda page, rule: open_rule_editor(page, 'access_rules', rule)
LIST_NAMES = ('blacklist', 'whitelist', 'accesslist')


def fill_in_rule_name(page: SecurityPage) -> str:
    name = f'ltf-{random_str(10)}'
    # Add rule
    page.add_access_rule.click()
    page.input_name.fill(name)
    return name


@pytest.mark.regression
@pytest.mark.parametrize('parameter',
                         ('ASN', 'Cookie', 'Country', 'Country Subdivision (ISO3166-2)',
                          'IP', 'Referrer', 'URL', 'User-Agent'),
                         ids=('asn', 'cookie', 'country', 'country_subdivision',
                              'ip', 'referrer', 'url', 'user_gent'))
def test_access_rule_access_control(access_rules_page: SecurityPage,
                                    delete_access_rules: list,
                                    parameter: str):
    """ Access Rules - Add rule - Access Control - {parameter}

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Access Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Access Rules' button
    2. Fill in the name of rule
    3. Select {parameter} from 'Add Access Control' dropdown
    4. Click on 'whitelist', 'blacklist', 'accesslist'
    5. Fill correct value in the input field
    6. Click 'Save' button

    Expected Results
    -----------------
    6.1 'Access rule created' should appear on the snackbar
    6.2 Find and click rule in the table
    6.3 Rule should contain filled in values on 5 step
    """
    valid_input_values = {
        'ASN': '1',
        'Cookie': 'string',
        'Country': 'UA',
        'Country Subdivision (ISO3166-2)': 'UA-46',
        'IP': '10.10.10.1',
        'Referrer': 'string',
        'URL': 'string',
        'User-Agent': 'string'
    }
    type_id = ACCESS_CONTROL_TYPE[parameter].lower()

    rule_name = fill_in_rule_name(access_rules_page)
    access_rules_page.access_control_input.click()

    access_rules_page.select_by_name(name=parameter).click()

    # Get page element using access control type name
    for list_name in LIST_NAMES:
        # e.g. access_rules_page.asn_blacklist, access_rules_page.ip_blacklist
        button = getattr(access_rules_page, f'{type_id}_{list_name}')
        button.click()
        text_field = getattr(access_rules_page, f'{type_id}_{list_name}_input')
        text_field.fill(valid_input_values[parameter])
    # Save rule
    access_rules_page.save.click()
    assert access_rules_page.client_snackbar.text_content() == "Access rule created"
    delete_access_rules.append((access_rules_page, rule_name))

    open_access_rule(access_rules_page, rule_name)
    # Check created rule
    for list_name in LIST_NAMES:
        text_field = getattr(access_rules_page, f'{type_id}_{list_name}_input')
        assert text_field.text_content() == valid_input_values[parameter], \
            f'Wrong value for {parameter} {list_name}'


@pytest.mark.regression
def test_access_rule_advanced_settings_http_methods(access_rules_page: SecurityPage,
                                                    delete_access_rules: list):
    """ Access Rules - Add rule - Advanced Settings - HTTP methods

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Access Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Access Rules' button
    2. Fill in the name of rule
    3. Click on every HTTP Method's checkbox
    4. Click 'Save' button

    Expected Results
    -----------------
    6.1 'Access rule created' should appear on the snackbar
    6.2 HTTP Methods checkboxes should be checked as on step 3
    """
    rule_name = fill_in_rule_name(access_rules_page)
    expected = {}
    for method in HTTP_METHODS:
        checkbox = getattr(access_rules_page, f'method_{method.lower()}')
        expected[method] = not checkbox.is_checked()
        checkbox.click()

    # Save rule
    access_rules_page.save.click()
    assert access_rules_page.client_snackbar.text_content() == "Access rule created"
    delete_access_rules.append((access_rules_page, rule_name))

    open_access_rule(access_rules_page, rule_name)

    for method in HTTP_METHODS:
        checkbox = getattr(access_rules_page, f'method_{method.lower()}')
        assert expected[method] == checkbox.is_checked()


@pytest.mark.regression
def test_access_rule_advanced_settings_input_fields(access_rules_page: SecurityPage,
                                                    delete_access_rules: list):
    """ Access Rules - Add rule - Advanced Settings - Input fields

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Access Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Access Rules' button
    2. Fill in the name of rule
    3. Fill in some strings into input fields in "Advanced Settings"
    4. Click 'Save' button

    Expected Results
    -----------------
    4.1 'Access rule created' should appear on the snackbar
    4.2 Rule should contain filled in values on 3 step
     """
    rule_name = fill_in_rule_name(access_rules_page)
    string_value1, string_value2 = 'Value 1', 'Value 2'
    response_header = 'Header'
    upload_limit = '1024'

    # Other HTTP Methods
    access_rules_page.other_methods.fill(string_value1)
    access_rules_page.other_methods.press('Enter')
    access_rules_page.other_methods.fill(string_value2)
    access_rules_page.other_methods.press('Enter')
    # Response Header Name
    access_rules_page.response_header_name.fill(response_header)
    # Single File Upload Limit
    access_rules_page.file_upload_limit.fill(upload_limit)
    # Allowed Request Content Types
    #access_rules_page.request_content_type.hover()
    #access_rules_page.request_content_type_clear.click()
    access_rules_page.request_content_type.fill(string_value1)
    # Extension Blacklist
    #access_rules_page.extension_blacklist.hover()
    #access_rules_page.extension_blacklist_clear.click()
    access_rules_page.extension_blacklist.fill(string_value1)
    # Header Blacklist
    access_rules_page.header_blacklist.fill(string_value1)

    # Save rule
    access_rules_page.save.click()
    assert access_rules_page.client_snackbar.text_content() == "Access rule created"
    delete_access_rules.append((access_rules_page, rule_name))

    open_access_rule(access_rules_page, rule_name)

    # ==== Verifications ====
    # Other HTTP Methods
    assert access_rules_page.other_methods_buttons[0].text_content() == string_value1, \
        'Wrong other HTTP methods'
    assert access_rules_page.other_methods_buttons[1].text_content() == string_value2, \
        'Wrong other HTTP methods'
    # Response Header Name
    assert access_rules_page.response_header_name.input_value() == response_header, \
        "Wrong Response Header Name "
    # Single File Upload Limit
    assert access_rules_page.file_upload_limit.input_value() == upload_limit, \
        "Wrong Single File Upload Limit"
    # Allowed Request Content Types
    assert access_rules_page.request_content_type_buttons[0].text_content() == string_value1, \
        f"Cannot find `{string_value1}` in Allowed Request Content Types"
    # Extension Blacklist
    assert access_rules_page.extension_blacklist_buttons[0].text_content() == string_value1, \
        f"Cannot find `{string_value1}` in Extension Blacklist"
    # Header Blacklist
    assert access_rules_page.header_blacklist_buttons[0].text_content() == string_value1, \
        f"Cannot find `{string_value1}` in Header Blacklist"


@pytest.mark.regression
def test_access_rule_edit_rule(access_rules_page: SecurityPage,
                               delete_access_rules: list):
    """ Access Rules - Edit existent rule

     Preconditions:
     --------------
     1. Navigate to Security tab
     2. Click 'Access Rules' on the left sidebar

     Steps:
     ------
     1. Click 'Add Access Rules' button
     2. Fill in the name of rule
     3. Click 'Save' button
     4. Click on newly created rule
     5. Fill in some strings into input fields
     6. Click 'Save' button

     Expected Results
     -----------------
     3 'Access rule created' should appear on the snackbar
     6.1 'Access rule updated' should appear on the snackbar
     6.2 Rule should contain filled in values on 3 step
    """
    # Create Rule
    rule_name = fill_in_rule_name(access_rules_page)
    # Save rule
    access_rules_page.save.click()
    assert access_rules_page.client_snackbar.text_content() == "Access rule created"
    delete_access_rules.append((access_rules_page, rule_name))

    open_access_rule(access_rules_page, rule_name)
    # Edit Rule
    string_value1, string_value2 = 'Value 1', 'Value 2'
    response_header = 'Header'
    upload_limit = '1024'
    # Other HTTP Methods
    access_rules_page.other_methods.fill(string_value1)
    access_rules_page.other_methods.press('Enter')
    access_rules_page.other_methods.fill(string_value2)
    access_rules_page.other_methods.press('Enter')
    # Response Header Name
    access_rules_page.response_header_name.fill(response_header)
    # Multiple File Upload Limit
    #TODO
    access_rules_page.file_upload_limit.fill(upload_limit)
    # Single File Upload Limit
    access_rules_page.file_upload_limit.fill(upload_limit)
    # Header Blacklist
    access_rules_page.header_blacklist.fill(string_value1)

    # Save again rule
    access_rules_page.save.click()
    assert access_rules_page.client_snackbar.text_content() == "Access rule updated"

    open_access_rule(access_rules_page, rule_name)

    # Verification
    # Other HTTP Methods
    assert access_rules_page.other_methods_buttons[0].text_content() == string_value1, \
        'Wrong other HTTP methods'
    assert access_rules_page.other_methods_buttons[1].text_content() == string_value2, \
        'Wrong other HTTP methods'
    # Response Header Name
    assert access_rules_page.response_header_name.input_value() == response_header, \
        "Wrong Response Header Name "
    # Single File Upload Limit
    assert access_rules_page.file_upload_limit.input_value() == upload_limit, \
        "Wrong Single File Upload Limit"
    # Header Blacklist
    assert access_rules_page.header_blacklist_buttons[0].text_content() == string_value1, \
        f"Cannot find `{string_value1}` in Header Blacklist"


@pytest.mark.regression
def test_access_rule_delete_rule(access_rules_page: SecurityPage,
                                 delete_access_rules: list):
    """ Access Rules - Delete existent rule

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Access Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Access Rules' button
    2. Fill in the name of rule
    3. Click 'Save' button
    4. Click on newly created rule
    5. Click 'Delete' button

    Expected Results
    -----------------
    3 'Access rule created' should appear on the snackbar
    5.1 'Successfully deleted' should appear on the snackbar
    6.2 Rule shouldn't be present in Access Rules table
    """
    # Create Rule
    rule_name = fill_in_rule_name(access_rules_page)
    # Save rule
    access_rules_page.save.click()
    assert access_rules_page.client_snackbar.text_content() == "Access rule created"
    delete_access_rules.append((access_rules_page, rule_name))

    open_access_rule(access_rules_page, rule_name)

    # Delete rule
    access_rules_page.delete_button.click()
    access_rules_page.confirm_button.click()
    assert access_rules_page.client_snackbar.text_content() == "Successfully deleted"
    try:
        access_rules_page.table.wait_for(timeout=10000)  # ms
    except TimeoutError:
        # Check if there is no access rules
        access_rules_page.no_data_to_display.wait_for(timeout=500)  # ms
        delete_access_rules.pop()
        return
    for row in access_rules_page.table.tbody.tr:
        if row[0].text_content() == rule_name:
            row[0].click()
            raise AssertionError("Rule was not deleted")
    delete_access_rules.pop()


@pytest.mark.regression
def test_access_rules_request_limit(security_logged):
    """ Access Rules - Max Rules count

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Mock response on /graphql with 99 access rules

    Steps:
    ------
    1. Click 'Access Rules' on the left sidebar

    Expected Results:
    -----------------
    1. 'Add Access Rules' button should be disabled
    2. 'You can only add up to 99 rules' should appear near 'Add Access Rules' button
    """
    mock_data = {'data': {'wafConfig': []}}
    last_modified = datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
    for i in range(99):
        item = {'id': str(i),
                'name': random_str(15),
                'superCapacity': False,
                'lastModifiedDate':	last_modified}
        mock_data['data']['wafConfig'].append(item)

    security_logged.mock.schedule(
        match={'variables': {"path": "/acl"}},
        body_json=mock_data)
    security_logged.access_rules.click()
    security_logged.table.wait_for(timeout=5000)
    time.sleep(1)
    assert security_logged.add_access_rule.is_disabled(), \
        "Add Access Rule button should be dissabled"

    expected_msg = "You can only add up to 99 rules"
    assert security_logged.get_by_title(expected_msg).is_visible(), \
        f"`{expected_msg}` message should be visible"