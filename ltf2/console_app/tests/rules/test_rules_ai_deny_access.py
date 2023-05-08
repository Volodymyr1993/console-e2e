def test_rules_ai_deny_access(property_page):
    """Rules - AI rule - Deny Access

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule
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
    assert property_page.value_div.text_content() == 'RU', 'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Deny Access', 'Wrong Feature'
    assert property_page.rule_checkbox.is_checked(), 'Feature is not enabled'
