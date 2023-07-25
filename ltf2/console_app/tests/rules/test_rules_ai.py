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

def test_rules_ai_deny_all_except_one(property_page):
    """Rules - AI rule - Deny all requests except from one country

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule 'deny request to all but Ukraine'
    3. Click 'Generate Rule'
    4. Click on created Condition
    5. Click on created Feature

    Expected Results:
    -----------------
    3. New Rule should be created
    4.1 Variable should be 'Country
    4.2 Operator should be 'does not equal'
    4.3 Value should be 'Ukraine'
    5.1 Feature name should be 'Deny Access'
    5.2 Deny Access checkbox should be selected
    """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('deny request to all but Ukraine')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Country', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'does not equal', 'Wrong Operator'
    assert property_page.match_value_input.input_value() == 'Ukraine', \
        'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Deny Access', 'Wrong Feature'
    assert property_page.rule_checkbox.is_checked(), 'Feature is not enabled'

def test_rules_ai_deny_all_sanctioned_countries(property_page):
    """Rules - AI rule - Deny access for all sanctioned countries

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule 'deny access for all countries under sanctions'
    3. Click 'Generate Rule'
    4. Click on created Condition
    5. Click on created Feature

    Expected Results:
    -----------------
    3. New Rule should be created
    4.1 Variable should be 'Country
    4.2 Operator should be 'is one of'
    4.3 Value should be 'Iran, Syrian, North Korea, Cuba, Sudan'
    5.1 Feature name should be 'Deny Access'
    5.2 Deny Access checkbox should be selected
    """
    list_of_sanctioned_countries = [
        'Iran, Islamic Republic of',
        'Syrian Arab Republic',
        'Korea, Democratic People’s Republic of',
        'Cuba',
        'Sudan'
    ]

    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('deny access for all countries under sanctions')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Country', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'is one of', 'Wrong Operator'

    values_from_the_field = property_page.values_list.inner_text()
    make_list_from_string = list(values_from_the_field.split('\n')[:-1])

    assert make_list_from_string == list_of_sanctioned_countries, \
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

def test_rules_ai_generate_cache_rule_for_statis_object(property_page):
    """Rules - AI rule - Generate cache rule for static objects.

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule 'generate cache rule for static objects.'
    3. Click 'Generate Rule'
    4. Click on created Condition
    5. Click on created Feature

    Expected Results:
    -----------------
    3. New Rule should be created
    4.1 Variable should be 'Path
    4.2 Operator should be 'matches (simple)'
    4.3 Value should be '/static/:path*'
    5.1 Feature name should be 'Set Max Age'
    5.2 Response Status 200, Max Age 1 year
    """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('generate cache rule for static objects.')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Path', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'matches (simple)', 'Wrong Operator'
    assert property_page.value_div.inner_text() == '/static/:path*', \
        'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Set Max Age', 'Wrong Feature'
    assert property_page.response_status_code.input_value() == '200'
    assert property_page.max_age_value.input_value() == '1'
    assert property_page.max_age_unit.input_value() == 'year'
