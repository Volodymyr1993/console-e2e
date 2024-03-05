import time

import pytest
from playwright.sync_api import TimeoutError

from ltf2.console_app.magic.constants import SECURITY_RULE_NAME_PREFIX
from ltf2.console_app.magic.helpers import random_str
from ltf2.console_app.magic.pages.pages import SecurityPage


def create_app_name(page: SecurityPage) -> str:
    name = f'{SECURITY_RULE_NAME_PREFIX}{random_str(10)}'
    # Add rule
    page.new_seccurity_application.click()
    page.input_name.fill(name)
    return name


def open_secapp_editor(page: SecurityPage, rule_name: str) -> None:
    page.goto()
    page.security.click()
    page.security_application.click()
    page.secapp_by_name(name=rule_name).click()


@pytest.mark.regression
def test_security_application_add_rule(security_app_page: SecurityPage, delete_sec_app: list):
    """ Security Application - Add rule

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Security Application' on the left sidebar

    Steps:
    ------
    1. Click 'Add New' button
    2. Fill in the name of rule
    3. Fill correct value in the input field
    4. Click 'Save' button
    5. Click 'Access All Changes'

    Expected Results
    -----------------
    5.1 'Security application updated' should appear on the snackbar
    5.2 Find and click rule in the table
    5.3 Rule should contain filled in values on 3rd step
    """
    rule_name = create_app_name(security_app_page)
    value = random_str(8)
    # Select last hostname
    security_app_page.host_input.click()
    host_match = security_app_page.select.li[-1].text_content()
    security_app_page.select.li[-1].click()
    security_app_page.host_values_input.fill(value)
    # Select last url path
    security_app_page.url_path_input.click()
    url_match = security_app_page.select.li[-1].text_content()
    security_app_page.select.li[-1].click()
    security_app_page.url_values_input.fill(value)
    # Click Access Rule
    security_app_page.config_access_rules.click()
    # Select all fields
    security_app_page.prod_access_rule_input.click()
    access_rule = security_app_page.select.li[0].text_content()
    security_app_page.select.li[0].click()

    security_app_page.action_access_rule_input.click()
    action_type = security_app_page.select.li[0].text_content()
    security_app_page.select.li[0].click()

    security_app_page.audit_access_rule_input.click()
    audit = security_app_page.select.li[0].text_content()
    security_app_page.select.li[0].click()

    # Save Rule
    delete_sec_app.append(rule_name)
    security_app_page.save.click()
    security_app_page.save_secapp.click()
    assert security_app_page.client_snackbar.text_content() == \
           "Security application updated"

    # Find created app
    open_secapp_editor(security_app_page, rule_name)

    # Check host
    assert security_app_page.host_input.input_value() == host_match, \
        'Wrong Hostname dropdown item'
    assert security_app_page.host_values_buttons.text_content() == value, \
        'Wrong Hostname value'
    # Check url
    assert security_app_page.url_path_input.input_value() == url_match, \
        'Wrong Url dropdown item'
    assert security_app_page.url_values_buttons.text_content() == value, \
        'Wrong Url value'

    # Check Access Rules
    assert security_app_page.prod_access_rule_input.input_value() == access_rule, \
        'Wrong Production Access Rule'
    assert security_app_page.action_access_rule_input.input_value() == action_type, \
        'Wrong Action Type'
    assert security_app_page.audit_access_rule_input.input_value() == audit, \
        'Wrong Audit Access Rule'


@pytest.mark.regression
def test_security_application_edit_rule(security_app_page: SecurityPage,
                                        delete_sec_app: list):
    """ Security Application - Edit rule

    Steps:
    ------
    1. Click 'Add New' button
    2. Fill in the name of rule
    3. Fill correct value in the input field
    4. Click 'Save' button
    5. Click 'Access All Changes'
    6. Click on newly created rule
    7. Fill in some strings into input fields
    8. Click 'Save' button
    9. Click 'Access All Changes'

    Expected Results
    -----------------
    5. 'Security application updated' should appear on the snackbar
    6. Rule should contain filled in values on 3rd step
    9.1 'Security application updated' should appear on the snackbar
    9.2 Rule should contain filled in values on 6th step
    """
    rule_name = create_app_name(security_app_page)
    value = 'Value'
    security_app_page.host_input.click()
    security_app_page.select.li[-1].click()
    security_app_page.host_values_input.fill(value)
    security_app_page.url_path_input.click()
    security_app_page.select.li[-1].click()
    security_app_page.url_values_input.fill(value)
    security_app_page.config_access_rules.click()
    # Save Rule
    delete_sec_app.append(rule_name)
    security_app_page.save.click()
    security_app_page.save_secapp.click()
    assert security_app_page.client_snackbar.text_content() == \
           "Security application updated"

    # Find created app
    open_secapp_editor(security_app_page, rule_name)

    # Edit
    # Select last hostname
    security_app_page.host_input.click()
    host_match = security_app_page.select.li[-1].text_content()
    security_app_page.select.li[-1].click()
    host_value = random_str(10)
    security_app_page.host_values_input.fill(host_value)
    # Select last url path
    security_app_page.url_path_input.click()
    url_match = security_app_page.select.li[-1].text_content()
    security_app_page.select.li[-1].click()
    url_value = random_str(10)
    security_app_page.url_values_input.fill(url_value)
    # Click Access Rule
    security_app_page.config_access_rules.click()
    # Select all fields
    security_app_page.prod_access_rule_input.click()
    access_rule = security_app_page.select.li[0].text_content()
    security_app_page.select.li[0].click()

    security_app_page.action_access_rule_input.click()
    action_type = security_app_page.select.li[0].text_content()
    security_app_page.select.li[0].click()

    security_app_page.audit_access_rule_input.click()
    audit = security_app_page.select.li[0].text_content()
    security_app_page.select.li[0].click()

    # Save Rule
    security_app_page.save.click()
    security_app_page.save_secapp.click()
    assert security_app_page.client_snackbar.text_content() == \
           "Security application updated"

    # Find created app
    open_secapp_editor(security_app_page, rule_name)

    # Check host
    assert security_app_page.host_input.input_value() == host_match, \
        'Wrong Hostname dropdown item'
    assert security_app_page.host_values_buttons.last.text_content() == host_value, \
        'Wrong Hostname value'
    # Check url
    assert security_app_page.url_path_input.input_value() == url_match, \
        'Wrong Url dropdown item'
    assert security_app_page.url_values_buttons.last.text_content() == url_value, \
        'Wrong Url value'

    # Check Access Rules
    assert security_app_page.prod_access_rule_input.input_value() == access_rule, \
        'Wrong Production Access Rule'
    assert security_app_page.action_access_rule_input.input_value() == action_type, \
        'Wrong Action Type'
    assert security_app_page.audit_access_rule_input.input_value() == audit, \
        'Wrong Audit Access Rule'


@pytest.mark.regression
def test_security_application_delete_rule(security_app_page: SecurityPage, delete_sec_app: list):
    """ Security Application - Delete rule

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Security Application' on the left sidebar

    Steps:
    ------
    1. Click 'Add New' button
    2. Fill in the name of rule
    3. Fill correct value in the input field
    4. Click 'Save' button
    5. Click 'Access All Changes'
    6. Click on newly created rule
    7. Click 'Delete' button

    Expected Results
    -----------------
    5. 'Security application updated' should appear on the snackbar
    7.1 'Security application updated' should appear on the snackbar
    7.2 Rule shouldn't be present in Security Application table
    """
    rule_name = create_app_name(security_app_page)

    security_app_page.save.click()
    security_app_page.save_secapp.click()
    delete_sec_app.append(rule_name)
    assert security_app_page.client_snackbar.text_content() == 'Security application updated'

    # Find created app
    open_secapp_editor(security_app_page, rule_name)

    security_app_page.delete_button.click()
    security_app_page.confirm_button.click()
    security_app_page.save_secapp.click()
    # Wait message on snackbar to change
    assert security_app_page.client_snackbar.text_content() == 'Security application updated'

    try:
        security_app_page.secapp_by_name(name=rule_name).wait_for(timeout=3000)
        raise AssertionError(f'Rule {rule_name} was not deleted')
    except TimeoutError:
        delete_sec_app.pop()


@pytest.mark.regression
def test_security_application_rules_limit(security_logged):
    """ Security Application - Max Rules count

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Mock response on /graphql with 99 security applications

    Steps:
    ------
    1. Click 'Security Application' on the left sidebar

    Expected Results:
    -----------------
    1. 'Add New' button should be disabled
    2. 'You can only add up to 99 security applications' should appear near 'Add New' button
    """
    mock_data = {'data': {'wafConfig': {'scopes': []}}}

    for i in range(99):
        item = {'id': str(i),
                'name': random_str(15),
                'aclAuditAction': None,
                'aclAuditId': None,
                'aclProdAction': None,
                'aclProdId': None,
                'botsProdAction': None,
                'botsProdId': None,
                'profileAuditAction ': None,
                'profileAuditId': None,
                'profileProdAction': None,
                'profileProdId': None,
                'rulesAuditAction': None,
                'rulesAuditId': None,
                'rulesProdAction': None,
                'rulesProdId': None,
                'host': {'type': 'GLOB',
                         'value': '*'},
                'path': {'type': 'GLOB',
                         'value': '*'}}
        mock_data['data']['wafConfig']['scopes'].append(item)

    security_logged.mock.schedule(
        match={'variables': {'path': '/scopes'}},
        body_json=mock_data)
    security_logged.security_application.click()
    security_logged.new_seccurity_application.wait_for(timeout=3000)
    time.sleep(1)
    assert security_logged.new_seccurity_application.is_disabled(), \
        "'Add New' button should be disabled"
    expected_msg = "You can only add up to 99 security applications"
    assert security_logged.get_by_title(expected_msg).is_visible(), \
        f"`{expected_msg}` message should be visible"
