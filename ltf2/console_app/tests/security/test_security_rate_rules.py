import time
from datetime import datetime, timezone

import pytest
from playwright.sync_api import Page

from ltf2.console_app.magic.helpers import random_str


def fill_in_rule_name(page: Page) -> str:
    name = f'ltf-{random_str(10)}'
    rate = '1000'
    # Add rule
    page.add_rate_rule.click()
    page.input_name.fill(name)
    page.input_num.fill(rate)
    return name


def test_rate_rules_add_delete_rule_without_condition_group(rate_rules_page: Page,
                                                            delete_rate_rules: list):
    """ Rate Rules - Add and delete Managed rule

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Rate Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Rate Rules'
    2. Fill in the name and rate limit of the rule
    3. Click 'Save' button
    4. Click 'Delete' button
    5. Click 'Confirm' button

    Expected Results:
    -----------------
    3. 'Rate rule created' should appear on the snackbar
    5.1. 'Successfully deleted' should appear on the snackbar
    5.2. Rule should be not present in the 'Rate Rule table'
    """
    # Add rule
    name = f'ltf-{random_str(10)}'
    rate = '1000'
    # Add rule
    rate_rules_page.add_rate_rule.click()
    rate_rules_page.input_name.fill(name)
    rate_rules_page.input_num.fill(rate)
    ######
    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))
    assert rate_rules_page.client_snackbar.text_content() == "Rate rule created"
    # Delete rule
    rate_rules_page.delete_button.click()
    rate_rules_page.confirm_button.click()
    # Wait message on the snackbar to change
    rate_rules_page.client_snackbar.get_by_text('Successfully deleted').wait_for()
    # Make sure every dialog is closed - refresh page
    rate_rules_page.goto()
    rate_rules_page.security.click()
    rate_rules_page.rate_rules.click()

    for row in rate_rules_page.table.tbody.tr:
        if row[0].text_content() == name:
            raise AssertionError("Rule was not deleted")
    # If rule was successfully deleted - remove it from list
    delete_rate_rules.pop()


@pytest.mark.parametrize('param',
                         ['ASN', 'Country', 'File_extension', 'IP_address',
                          'Request_header', 'Request_method', 'Request_URL_path'])
def test_rate_rules_add_delete_rule_with_condition_group(rate_rules_page: Page,
                                                         delete_rate_rules: list,
                                                         param: str):
    """ Rate Rules - Add WAF rate rule with condition group and one {match_param} condition

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Rate Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Rate Rules'
    2. Fill in the name and rate limit of the rule
    3. Click 'New Condition Group' button
    4. In 'Matched By' dropdown select {match_param}
    5. Add 'Value'
    6. Click 'Save' button
    7. Click 'Delete' button
    8. Click 'Confirm' button

    Expected Results:
    -----------------
    6. 'Rate rule created' should appear on the snackbar
    8.1. 'Successfully deleted' should appear on the snackbar
    8.2. Rule should be not present in the 'Rate Rule table'
    """
    match_param = param.replace('_', ' ')
    value = {'ASN': '12345',
             'Country': 'UA',
             'File extension': '.mov',
             'IP address': '192.168.0.1',
             'Request header': 'test.com',
             'Request method': 'HEAD',
             'Request URL path': '/this/is/the/way/'}
    # Add rule
    name = fill_in_rule_name(rate_rules_page)
    rate_rules_page.rate_new_condition_group.click()
    rate_rules_page.rate_new_condition_group.click()
    rate_rules_page.match_condition_input(group=0, condition=0).click()
    rate_rules_page.select_by_name(name=match_param).click()
    # Request header has additional drop-down
    if match_param == 'Request header':
        rate_rules_page.match_req_header_input.click()
        rate_rules_page.select.li[0].click()
    rate_rules_page.rate_add_condition_value.fill(value[match_param])
    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))
    assert rate_rules_page.client_snackbar.text_content() == "Rate rule created"
    # Delete rule
    rate_rules_page.delete_button.click()
    rate_rules_page.confirm_button.click()
    # Wait message on the snackbar to change
    rate_rules_page.client_snackbar.get_by_text('Successfully deleted').wait_for()
    # Make sure every dialog is closed - refresh page
    rate_rules_page.goto()
    rate_rules_page.security.click()
    rate_rules_page.rate_rules.click()

    for row in rate_rules_page.table.tbody.tr:
        if row[0].text_content() == name:
            raise AssertionError("Rule was not deleted")
    # If rule was successfully deleted - remove it from list
    delete_rate_rules.pop()


def test_rate_rules_add_delete_rule_with_five_conditions(rate_rules_page: Page,
                                                         delete_rate_rules: list):
    """ Rate Rules - Add WAF rate rule with 5 conditions

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Rate Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Rate Rules'
    2. Fill in the name and rate limit of the rule
    3. Click 'New Condition Group' button
    4. In 'Matched By' dropdown select IP address
    5. Add 'Value'
    6. Add 4 more conditions
    7. Click 'Save' button
    8. Click 'Delete' button
    9. Click 'Confirm' button

    Expected Results:
    -----------------
    7. 'Rate rule created' should appear on the snackbar
    9.1. 'Successfully deleted' should appear on the snackbar
    9.2. Rule should be not present in the 'Rate Rule table'
    """
    # Add rule
    name = fill_in_rule_name(rate_rules_page)
    rate_rules_page.rate_new_condition_group.click()
    rate_rules_page.rate_new_condition_group.click()
    for i in range(0, 5):
        if i >= 1:
            rate_rules_page.rate_new_condition.click()
        rate_rules_page.match_condition_input(group=0, condition=i).click()
        rate_rules_page.select_by_name(name='IP address').click()
        # for item in rate_rules_page.select.li:
        #     if item.text_content() == 'IP address':
        #         item.click()
        #         break
        rate_rules_page.rate_add_condition_value.fill(f'10.10.10.{i}')
    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))
    assert rate_rules_page.client_snackbar.text_content() == "Rate rule created"
    # Delete rule
    rate_rules_page.delete_button.click()
    rate_rules_page.confirm_button.click()
    # Wait message on the snackbar to change
    rate_rules_page.client_snackbar.get_by_text('Successfully deleted').wait_for()
    # Make sure every dialog is closed - refresh page
    rate_rules_page.goto()
    rate_rules_page.security.click()
    rate_rules_page.rate_rules.click()

    for row in rate_rules_page.table.tbody.tr:
        if row[0].text_content() == name:
            raise AssertionError("Rule was not deleted")
    # If rule was successfully deleted - remove it from list
    delete_rate_rules.pop()


def test_rate_rules_add_rule_with_empty_condition_value(rate_rules_page: Page,
                                                        delete_rate_rules: list):
    """ Rate Rules - Add Security rate rule with empty condition value

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Rate Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Rate Rules'
    2. Fill in the name and rate limit of rule
    3. Click 'New Condition Group' button
    4. In 'Matched By' dropdown select {match_param}
    5. Specify empty 'Value'
    6. Click 'Save' button
    7. Close window

    Expected Results:
    -----------------
    6. 'Required' should be shown under 'Value' field
    6.1. Rate Rule should not be created
    """
    # Add rule
    name = fill_in_rule_name(rate_rules_page)
    rate_rules_page.rate_new_condition_group.click()
    rate_rules_page.rate_new_condition_group.click()

    # Trying to save the rule
    rate_rules_page.rate_add_condition_value.fill('')
    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))

    for item, err in ((rate_rules_page.rate_add_condition_value,
                       'Type desired value and ENTER to apply.'),):
        assert item.locator('../../p').text_content() == f'Required', \
                        f'{item.selector} should contain error'

    # Refresh page
    rate_rules_page.goto()
    rate_rules_page.security.click()
    rate_rules_page.rate_rules.click()

    for row in rate_rules_page.table.tbody.tr:
        if row[0].text_content() == name:
            raise AssertionError("Rule was created")
    # If rule wasn't created - remove it from list
    delete_rate_rules.pop()


def test_rate_rules_request_limit(security_logged):
    """ Rate Rules - Max Rules count

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Mock response on /graphql with 99 rate rules

    Steps:
    ------
    1. Click 'Rate Rules' on the left sidebar

    Expected Results:
    -----------------
    1. 'Add Rate Rules' button should be disabled
    2. 'You can only add up to 99 rules' should appear near 'Add Rate Rules' button
    """
    mock_data = {'data': {'wafConfig': []}}
    last_modified = datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
    for i in range(99):
        item = {'id': str(i),
                'name': random_str(15),
                'lastModifiedDate': last_modified}
        mock_data['data']['wafConfig'].append(item)

    security_logged.mock.schedule(
        match={'variables': {"path": "/limit"}},
        body_json=mock_data)
    security_logged.rate_rules.click()
    security_logged.table.wait_for(timeout=5000)
    time.sleep(1)
    assert security_logged.add_rate_rule.is_disabled(), \
        "Add Rate Rule button should be disabled"

    expected_msg = "You can only add up to 99 rules"
    assert security_logged.get_by_title(expected_msg).is_visible(), \
        f"`{expected_msg}` message should be visible"
