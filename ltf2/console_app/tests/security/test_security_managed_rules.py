import time
from datetime import datetime, timezone

import pytest

from ltf2.console_app.magic.helpers import random_str, random_int, open_rule_editor
from ltf2.console_app.magic.pages.pages import SecurityPage


open_managed_rule = lambda page, rule: open_rule_editor(page, 'managed_rules', rule)


def fill_in_rule_name(page: SecurityPage) -> str:
    name = f'ltf-{random_str(10)}'
    # Add rule
    page.add_managed_rule.click()
    page.input_name.fill(name)
    return name


def test_managed_rules_add(managed_rules_page: SecurityPage,
                           delete_managed_rules: list):
    """ Managed Rules - Add and delete Managed rule

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Click 'Save' button

    Expected Results:
    -----------------
    2. 'Managed rule created' should appear on the snackbar
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    managed_rules_page.save.click()
    # Verify if created
    delete_managed_rules.append((managed_rules_page, name))
    assert managed_rules_page.client_snackbar.text_content() == "Managed rule created"
    open_managed_rule(managed_rules_page, name)
    assert managed_rules_page.input_name.input_value() == name


def test_managed_rules_add_rule_with_header_and_ignore_list(managed_rules_page: SecurityPage,
                                                            delete_managed_rules: list):
    """ Managed Rules - Add rule - Optional fields

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Fill in 'Ignore Cookies' field
    4. Fill in 'Ignore Header' field
    5. Fill in 'Ignore Query Arguments' field
    6. Click 'Save' button

    Expected Results:
    -----------------
    6.1 'Managed rule created' should appear on the snackbar
    6.2 Find rule in the table. It should contain filled in values on 2-5 steps
    """
    header = f'X-LTF-{random_str(5)}'
    header_ignore = f'X-LTF-{random_str(5)}'
    cookie = f'ltf-cookie-{random_str(5)}'
    query_args = f'ltf-query-{random_str(5)}'

    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    # Fill in Ignore List fields
    managed_rules_page.header_name_input.fill(header)
    managed_rules_page.ignore_cookies_input.fill(cookie)
    managed_rules_page.ignore_header_input.fill(header_ignore)
    managed_rules_page.ignore_query_args_input.fill(query_args)

    managed_rules_page.save.click()
    # Verify if created
    delete_managed_rules.append((managed_rules_page, name))
    assert managed_rules_page.client_snackbar.text_content() == "Managed rule created"

    open_managed_rule(managed_rules_page, name)
    # Verify fields
    assert managed_rules_page.header_name_input.input_value() == header
    assert managed_rules_page.ignore_cookies_buttons[0].text_content() == cookie
    assert managed_rules_page.ignore_header_buttons[0].text_content() == header_ignore
    assert managed_rules_page.ignore_query_args_buttons[0].text_content() == query_args


def test_managed_rules_add_rule_more_details(managed_rules_page: SecurityPage,
                                             delete_managed_rules: list):
    """ Managed Rules - Add rule - More Details

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Fill in all numeric fields
    4. Uncheck 'Json Inspection'
    5. Click 'Save' button

    Expected Results:
    -----------------
    5.1 'Managed rule created' should appear on the snackbar
    5.2 Find rule in the table. It should contain filled in values on 2,3 steps
    """
    max_args_reqs = random_int(3)
    single_arg_length = random_int(4)
    arg_name_length = random_int(4)
    total_arg_length = random_int(5)
    file_size = random_int(6)

    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    # Fill in More Details fields
    managed_rules_page.more_details.click()
    managed_rules_page.max_args_reqs_input.fill(max_args_reqs)
    managed_rules_page.single_arg_length_input.fill(single_arg_length)
    managed_rules_page.arg_name_length_input.fill(arg_name_length)
    managed_rules_page.total_arg_length_input.fill(total_arg_length)
    managed_rules_page.max_file_size_input.fill(file_size)
    managed_rules_page.json_parser_input.uncheck()

    managed_rules_page.save.click()
    # Verify if created
    delete_managed_rules.append((managed_rules_page, name))
    assert managed_rules_page.client_snackbar.text_content() == "Managed rule created"

    open_managed_rule(managed_rules_page, name)
    # Verify fields
    managed_rules_page.more_details.click()
    assert managed_rules_page.max_args_reqs_input.input_value() == max_args_reqs
    assert managed_rules_page.single_arg_length_input.input_value() == single_arg_length
    assert managed_rules_page.arg_name_length_input.input_value() == arg_name_length
    assert managed_rules_page.total_arg_length_input.input_value() == total_arg_length
    assert managed_rules_page.max_file_size_input.input_value() == file_size
    assert not managed_rules_page.json_parser_input.is_checked()


def test_managed_rules_add_rule_with_more_details_negative_value(managed_rules_page: SecurityPage):
    """ Managed Rules - Add rule - Negative - More Details - Negative values

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Fill in "-1" in every field in More Details
    4. Click 'Save' button

    Expected Results:
    -----------------
    3. 'Positive value required' error message should appear near every field in
        More Details
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)

    # Fill in More Details fields
    managed_rules_page.more_details.click()
    managed_rules_page.max_args_reqs_input.fill("-1")
    managed_rules_page.single_arg_length_input.fill("-1")
    managed_rules_page.arg_name_length_input.fill("-1")
    managed_rules_page.total_arg_length_input.fill("-1")
    managed_rules_page.max_file_size_input.fill("-1")
    managed_rules_page.save.click()
    # Check if every element has error message
    for item in (managed_rules_page.max_args_reqs_input,
                 managed_rules_page.single_arg_length_input,
                 managed_rules_page.arg_name_length_input,
                 managed_rules_page.total_arg_length_input,
                 managed_rules_page.max_file_size_input):

        assert item.locator('../../p').text_content() == 'Positive value required', \
            f'{item.selector} should contain error'


def test_managed_rules_add_rule_with_more_details_empty_value(managed_rules_page: SecurityPage):
    """ Managed Rules - Add rule - Negative - More Details - Empty values

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Fill in empty string in every field in More Details

    Expected Results:
    -----------------
    3. 'Value required for' error message should appear near every field in
        More Details
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)

    # Fill in More Details fields
    managed_rules_page.more_details.click()

    managed_rules_page.max_args_reqs_input.fill("")
    managed_rules_page.single_arg_length_input.fill("")
    managed_rules_page.arg_name_length_input.fill("")
    managed_rules_page.total_arg_length_input.fill("")
    managed_rules_page.max_file_size_input.fill("")
    managed_rules_page.save.click()
    # Check if every element has error message
    for item, err in ((managed_rules_page.max_args_reqs_input, 'Max # of Arguments/Request'),
                      (managed_rules_page.single_arg_length_input, 'Single Argument Length'),
                      (managed_rules_page.arg_name_length_input, 'Argument Name Length'),
                      (managed_rules_page.total_arg_length_input, 'Total Argument Length'),
                      (managed_rules_page.max_file_size_input, 'Multiple File Upload Limit')):

        assert item.locator('../../p').text_content() == f'Value required for {err}', \
            f'{item.selector} should contain error'


def test_managed_rules_add_rule_with_policies(managed_rules_page: SecurityPage, delete_managed_rules: list):
    """ Managed Rules - Add rule - Policies

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Click 'Next' button
    4. Select some value from dropdown lists
    5. Check 'Automatically opt-in to the latest ECRS ruleset'
    6. Click 'Save' button

    Expected Results:
    -----------------
    5.1 'Managed rule created' should appear on the snackbar
    5.2 Find rule in the table. It should contain filled in values on 4 step
    6. 'Ruleset ECRS' field should be disabled
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    managed_rules_page.policies.click()

    # Select last one Ruleset ECRS
    managed_rules_page.ruleset_input.click()
    ruleset = managed_rules_page.ruleset_select.li[-1].text_content()
    managed_rules_page.ruleset_select.li[-1].click()

    # Select first one Threshold
    managed_rules_page.threshold_input.click()
    threshold = managed_rules_page.select.li[0].text_content()
    managed_rules_page.select.li[0].click()

    # Select last one Paranoia Level
    managed_rules_page.paranoia_level_input.click()
    paranoia_level = managed_rules_page.select.li[-1].text_content()
    managed_rules_page.select.li[-1].click()

    managed_rules_page.ruleset_switch.check()
    managed_rules_page.save.click()
    delete_managed_rules.append((managed_rules_page, name))

    # Verification
    open_managed_rule(managed_rules_page, name)
    managed_rules_page.policies.click()
    assert managed_rules_page.ruleset_input.is_disabled()
    assert managed_rules_page.ruleset_input.input_value() == ruleset
    assert managed_rules_page.threshold_input.input_value() == threshold
    assert managed_rules_page.paranoia_level_input.input_value() == paranoia_level
    assert managed_rules_page.ruleset_switch.is_checked()


@pytest.mark.parametrize('parameter', ['Argument', 'Headers', 'Cookies'])
def test_managed_rules_add_rule_with_exception(managed_rules_page: SecurityPage, delete_managed_rules: list, parameter: str):
    """ Managed Rules - Add rule - Exceptions

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Click 'Exceptions' tab
    4. Select Parameter {parameter}
    5. Fill in 'Name' and 'Applied Rule ID\'s'
    6. Click 'Save' button

    Expected Results:
    -----------------
    6.1 'Managed rule created' should appear on the snackbar
    6.2 Find rule in the table. It should contain filled in values on 4 step
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    managed_rules_page.exceptions.click()
    managed_rules_page.add_condition.click()
    managed_rules_page.parameter_input.click()

    # Select parameter
    for li in managed_rules_page.select.li:
        if li.text_content() == parameter:
            li.click()
            break
    else:
        raise AssertionError(f'Missing {parameter} in Parameter dropdown list')

    # Fill in fields
    condition_name = random_str(5)
    managed_rules_page.condition_name.fill(condition_name)
    managed_rules_page.regex_switch.check()
    ids = random_str(5)
    managed_rules_page.rule_ids.fill(ids)
    managed_rules_page.save.click()
    delete_managed_rules.append((managed_rules_page, name))
    assert managed_rules_page.client_snackbar.text_content() == f"Managed rule created"
    # Verification
    open_managed_rule(managed_rules_page, name)
    managed_rules_page.exceptions.click()

    assert condition_name in managed_rules_page.conditions[0].text_content()
    assert managed_rules_page.parameter_input.input_value() == parameter
    assert managed_rules_page.condition_name.input_value() == condition_name
    assert managed_rules_page.rule_ids_buttons[0].text_content() == ids


# Error cases
def test_managed_rules_graphql_plaintext_error(managed_rules_page: SecurityPage,
                                               delete_managed_rules: list):
    """ Managed Rules - Plain text error

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Click 'Save' button
    4. Click 'Delete' button
    5. Mock /graphql response with string error message
    5. Click 'Confirm' button

    Expected Results:
    -----------------
    2. 'Managed rule created' should appear on the snackbar
    5.1 Mocked message should be displayed
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    managed_rules_page.save.click()
    # Verify if created
    delete_managed_rules.append((managed_rules_page, name))
    assert managed_rules_page.client_snackbar.text_content() == "Managed rule created"
    open_managed_rule(managed_rules_page, name)
    # Delete rule
    managed_rules_page.delete_button.click()
    managed_rules_page.mock.schedule(
        match={'variables': {'httpMethod': 'delete'}},
        body_json={"data":
                       {"mutateWafConfig":
                            {"userErrors":
                                 [{"message":"Error from mock","__typename":"UserError"}],
                             "response":None,
                             "__typename":"MutateWafConfigPayload"}}})
    managed_rules_page.confirm_button.click()

    # Wait message on the snackbar to change
    managed_rules_page.client_snackbar.get_by_text('Error from mock').wait_for()


def test_managed_rules_add_delete_graphql_jsonasstring_error(
        managed_rules_page: SecurityPage,
        delete_managed_rules: list):
    """ Managed Rules - JSON as string error

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Managed Rules' on the left sidebar

    Steps:
    ------
    1. Click 'Add Managed Rules'
    2. Fill in the name of rule
    3. Click 'Save' button
    4. Click 'Delete' button
    5. Mock /graphql response with JSON error msg
    5. Click 'Confirm' button

    Expected Results:
    -----------------
    2. 'Managed rule created' should appear on the snackbar
    5.1 Mocked message should be displayed
    """
    # Add rule
    name = fill_in_rule_name(managed_rules_page)
    managed_rules_page.save.click()
    # Verify if created
    delete_managed_rules.append((managed_rules_page, name))
    assert managed_rules_page.client_snackbar.text_content() == "Managed rule created"
    open_managed_rule(managed_rules_page, name)
    # Delete rule
    managed_rules_page.delete_button.click()
    managed_rules_page.mock.schedule(
        match={'variables': {'httpMethod': 'delete'}},
        body_json={"data":
                       {"mutateWafConfig":
                            {"userErrors":
                                 [{"message": "{\"errors\":[{\"code\":400,\"message\":\"Message inside JSON\"}],\"success\":false}","__typename":"UserError"}],
                             "response":None,
                             "__typename": "MutateWafConfigPayload"}}})
    managed_rules_page.confirm_button.click()

    # Wait message on the snackbar to change
    managed_rules_page.client_snackbar.get_by_text('Message inside JSON').wait_for()


def test_managed_rules_request_limit(security_logged):
    """ Managed Rules - Max Rules count

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Mock response on /graphql with 99 managed rules

    Steps:
    ------
    1. Click 'Managed Rules' on the left sidebar

    Expected Results:
    -----------------
    1. 'Add Managed Rules' button should be disabled
    2. 'You can only add up to 99 rules' should appear near 'Add Managed Rules' button
    """
    mock_data = {'data': {'wafConfig': []}}
    last_modified = datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + 'Z'
    for i in range(99):
        item = {'id': str(i),
                'name': random_str(15),
                'rulesetId': 'ERS',
                'rulesetVersion': '2022-11-04',
                'createdDate': '11/22/2022 01:09:23 PM',
                'lastModifiedDate': last_modified}
        mock_data['data']['wafConfig'].append(item)

    security_logged.mock.schedule(
        match={'variables': {"path": "/profile"}},
        body_json=mock_data)
    security_logged.rules_manager.click()
    security_logged.managed_rules.click()
    security_logged.table.wait_for(timeout=5000)
    time.sleep(1)
    assert security_logged.add_managed_rule.is_disabled(), \
        "Add Manage Rule button should be disabled"

    expected_msg = "You can only add up to 99 rules"
    assert security_logged.get_by_title(expected_msg).is_visible(), \
        f"`{expected_msg}` message should be visible"
