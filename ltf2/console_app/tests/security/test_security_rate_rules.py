import time
from datetime import datetime, timezone

import pytest
from playwright.sync_api import Page

from ltf2.console_app.magic.helpers import random_str, random_int, open_rule_editor


open_rate_rule = lambda page, rule: open_rule_editor(page, 'rate_rules', rule)


def fill_in_rule_name(page: Page) -> str:
    name = f'ltf-{random_str(10)}'
    rate = '1000'
    # Add rule
    page.add_rate_rule.click()
    page.input_name.fill(name)
    page.input_num.fill(rate)
    return name


def test_rate_rules_add_rule_without_condition_group(rate_rules_page: Page,
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

    Expected Results:
    -----------------
    3. 'Rate rule created' should appear on the snackbar
    """
    # Add rule
    name = f'ltf-{random_str(10)}'
    rate = random_int(4)
    # Add rule
    rate_rules_page.add_rate_rule.click()
    rate_rules_page.input_name.fill(name)
    rate_rules_page.input_num.fill(rate)

    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))
    assert rate_rules_page.client_snackbar.text_content() == "Rate rule created"
    open_rate_rule(rate_rules_page, name)
    assert rate_rules_page.input_name.input_value() == name
    assert rate_rules_page.input_num.input_value() == rate


@pytest.mark.parametrize('param',
                         ['ASN','Country', 'File_extension', 'IP_address',
                          'Request_header', 'Request_method', 'Request_URL_path'])
def test_rate_rules_add_rule_with_condition_group(rate_rules_page: Page,
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

    Expected Results:
    -----------------
    6.1 'Rate rule created' should appear on the snackbar
    6.2 Condition group should be present
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
    rate_rules_page.rate_condition_match_by(group=0, condition=0).click()
    rate_rules_page.select_by_name(name=match_param).click()
    # Request header has additional drop-down
    if match_param == 'Request header':
        rate_rules_page.match_req_header_input.click()
        rate_rules_page.select.li[0].click()
    rate_rules_page.rate_condition_value_input.fill(value[match_param])
    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))
    assert rate_rules_page.client_snackbar.text_content() == "Rate rule created"

    open_rate_rule(rate_rules_page, name)
    # Verification
    rate_rules_page.rate_condition_match_by(group=0, condition=0).wait_for()
    assert rate_rules_page.rate_condition_match_by(
        group=0, condition=0).input_value() == match_param
    assert rate_rules_page.rate_condition_values.text_content() == value[match_param]



def test_rate_rules_add_rule_with_five_conditions(rate_rules_page: Page,
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

    Expected Results:
    -----------------
    7.1 'Rate rule created' should appear on the snackbar
    7.2 Created conditions should be present in the rule
    """
    # Add rule
    name = fill_in_rule_name(rate_rules_page)
    rate_rules_page.rate_new_condition_group.click()
    rate_rules_page.rate_new_condition_group.click()
    for i in range(5):
        if i >= 1:
            rate_rules_page.rate_new_condition.click()
            rate_rules_page.rate_conditions(group=0, condition=i).click()
        rate_rules_page.rate_condition_match_by(group=0, condition=i).click()
        rate_rules_page.select_by_name(name='IP address').click()
        rate_rules_page.rate_condition_value_input.fill(f'10.10.10.{i}')
    rate_rules_page.save.click()
    # Verify if created
    delete_rate_rules.append((rate_rules_page, name))
    assert rate_rules_page.client_snackbar.text_content() == "Rate rule created"

    open_rate_rule(rate_rules_page, name)
    # Validate conditions
    for i in range(5):
        rate_rules_page.rate_conditions(group=0, condition=i).click()
        rate_rules_page.rate_condition_match_by(group=0, condition=i).click()
        rate_rules_page.select_by_name(name='IP address').click()
        assert rate_rules_page.rate_condition_values.text_content() == f'10.10.10.{i}'


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
    rate_rules_page.rate_condition_value_input.fill('')
    rate_rules_page.save.click()
    delete_rate_rules.append((rate_rules_page, name))

    # for item, err in ((rate_rules_page.rate_condition_value_input,
    #                    'Type desired value and ENTER to apply.'),):
    #     assert item.locator('../../p').text_content() == f'Required', \
    #         f'{item.selector} should contain error'
    # Refresh page
    rate_rules_page.goto()
    rate_rules_page.security.click()
    rate_rules_page.rules_manager.click()
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
    security_logged.rules_manager.click()
    security_logged.rate_rules.click()
    security_logged.table.wait_for(timeout=5000)
    time.sleep(1)
    assert security_logged.add_rate_rule.is_disabled(), \
        "Add Rate Rule button should be disabled"

    expected_msg = "You can only add up to 99 rules"
    assert security_logged.get_by_title(expected_msg).is_visible(), \
        f"`{expected_msg}` message should be visible"
