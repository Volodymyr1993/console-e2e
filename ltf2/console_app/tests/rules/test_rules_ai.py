def test_rules_ai_deny_access(property_page):
    """Rules - AI rule - Deny Access

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule 'Reject all requests from Russia'
    3. Click 'Generate Rule'
    4. Click on created Condition
    5. Click on created Feature

    Expected Results:
    -----------------
    3. New Rule should be created
    4.1 Variable should be 'Country
    4.2 Operator should be 'equals'
    4.3 Value should be 'RU'
    5.1 Feature name should be 'Deny Access'
    5.2 Deny Access checkbox should be selected
    """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('Reject all requests from Russia')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Country', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'equals', 'Wrong Operator'
    assert property_page.match_value_input.input_value() == 'Russian Federation', \
        'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Deny Access', 'Wrong Feature'
    assert property_page.rule_checkbox.is_checked(), 'Feature is not enabled'


def test_rules_ai_url_redirect(property_page):
    """Rules - AI rule - URL redirect

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule 'Redirect http traffic to https'
    3. Click 'Generate Rule'
    4. Click on created Condition
    5. Click on created Feature

    Expected Results:
    -----------------
    3. New Rule should be created
    4.1 Variable should be 'Scheme
    4.2 Operator should be 'equals'
    4.3 Value should be 'HTTP'
    5.1 Feature name should be 'URL Redirect'
    5.2 Status Code should be 302
    5.3 Correct Source and Destination should be generated
    """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('Redirect http traffic to https')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Scheme', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'equals', 'Wrong Operator'
    assert property_page.match_value_input.input_value() == 'HTTP', 'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'URL Redirect', 'Wrong Feature'
    assert property_page.code_input.input_value() == '302', 'Wrong Status Code'
    assert property_page.source_input.text_content() == '(.*)', 'Wrong Source'
    assert property_page.destination_input.text_content() == 'https://%{host}$1', \
        'Wrong Destination'
    assert not property_page.rule_checkbox.is_checked(), "Wrong 'ignore case'"
