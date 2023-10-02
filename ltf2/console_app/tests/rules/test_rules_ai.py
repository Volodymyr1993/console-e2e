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


def test_rules_ai_allow_only_post_requests(property_page):
    """Rules - AI rule - Allow only requests with method: POST

    Preconditions:
    --------------
    1. Navigate to Rule tab

    Steps:
    ------
    1. Click 'Add Rules Rule Using AI...'
    2. Fill in the rule 'Allow only requests with method: POST'
    3. Click 'Generate Rule'
    4. Click on created Condition
    5. Click on created Feature

    Expected Results:
    -----------------
    3. New Rule should be created
    4.1 Variable should be 'Method
    4.2 Operator should be 'does not equal'
    4.3 Value should be 'POST'
    5.1 Feature name should be 'Deny Access'
    5.2 Deny Access checkbox should be selected
    """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('Allow only requests with method: POST')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Method', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'does not equal', 'Wrong Operator'
    assert property_page.match_value_input.input_value() == 'POST', \
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
    # There are 2 ways how AI can create a valid rule
    if property_page.operator_input.input_value() == 'is one of':
        values_from_the_field = property_page.values_list.inner_text()
        make_list_from_string = list(values_from_the_field.split('\n')[:-1])
        for x in make_list_from_string:
            assert x in list_of_sanctioned_countries, 'Wrong Value'
        assert property_page.variable_input.input_value() == 'Country', 'Wrong Variable'
        property_page.close.click()
    else:
        property_page.close.click()
        for i in range(property_page.single_condition.count()):
            property_page.created_rule(num=-1).condition(num=i).click()
            assert property_page.operator_input.input_value() == 'equals', 'Wrong Operator'
            assert property_page.match_value_input.input_value() in list_of_sanctioned_countries
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


def test_rules_ai_generate_cache_rule_for_static_object(property_page):
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


def test_rules_ia_bypass_cache_with_strict_query_param(property_page):
    """Rules - AI rule - Disable caching when the "nc" query parameter is 1.

        Preconditions:
        --------------
        1. Navigate to Rule tab

        Steps:
        ------
        1. Click 'Add Rules Rule Using AI...'
        2. Fill in the rule 'disable caching when the "nc" query parameter is 1'
        3. Click 'Generate Rule'
        4. Click on created Condition
        5. Click on created Feature

        Expected Results:
        -----------------
        3. New Rule should be created
        4.1 Variable should be 'Query Parameter'
        4.2 Parameter Name should be 'nc'
        4.2 Operator should be 'equals'
        4.3 Value should be '1'
        5.1 Feature name should be 'Bypass Cache'
        5.2 Bypass the cache checkbox should be selected
        """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('disable caching when the "nc" query parameter is 1')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Query Parameter', 'Wrong Variable'
    assert property_page.parameter_name.text_content() == 'nc', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'equals', 'Wrong Operator'
    assert property_page.value_div.inner_text() == '1', 'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Bypass Cache', 'Wrong Feature'
    assert property_page.rule_checkbox.is_checked(), "Feature is not enabled"


def test_rules_ia_bypass_cache_with_matched_regex(property_page):
    """Rules - AI rule - set no-store for all urls containing /highsec/ path.

        Preconditions:
        --------------
        1. Navigate to Rule tab

        Steps:
        ------
        1. Click 'Add Rules Rule Using AI...'
        2. Fill in the rule 'set no-store for all urls containing /highsec/ path'
        3. Click 'Generate Rule'
        4. Click on created Condition
        5. Click on created Feature

        Expected Results:
        -----------------
        3. New Rule should be created
        4.1 Variable should be 'Path'
        4.2 Operator should be 'matches reqular expression'
        4.3 Match Value should be '\/highsec\/'
        5.1 Feature name should be 'Bypass Cache'
        5.2 Bypass the cache checkbox should be selected
        """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('set no-store for all urls containing /highsec/ path')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Path', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'matches regular expression', 'Wrong Operator'
    assert property_page.match_value_regex.inner_text() == r'\/highsec\/', 'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Bypass Cache', 'Wrong Feature'
    assert property_page.rule_checkbox.is_checked(), "Feature is not enabled"


def test_rules_ia_redirect_host_header(property_page):
    """Rules - AI rule - redirect example.com to www.example.com.

        Preconditions:
        --------------
        1. Navigate to Rule tab

        Steps:
        ------
        1. Click 'Add Rules Rule Using AI...'
        2. Fill in the rule 'redirect example.com to www.example.com'
        3. Click 'Generate Rule'
        4. Click on created Condition
        5. Click on created Feature

        Expected Results:
        -----------------
        3. New Rule should be created
        4.1 Variable should be 'Request Header'
        4.2 Header Name should be 'host'
        4.2 Operator should be 'equals'
        4.3 Value should be 'example.com'
        5.1 Feature name should be 'URL Redirect'
        5.2 Status Code should be 302
        5.3 Correct Source and Destination should be generated
        """
    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('redirect example.com to www.example.com')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Request Header', 'Wrong Variable'
    assert property_page.header_name.inner_text() == 'host', 'Wrong Header Name'
    assert property_page.operator_input.input_value() == 'equals', 'Wrong Operator'
    assert property_page.variable_value.inner_text() == 'example.com', 'Wrong Value'
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'URL Redirect', 'Wrong Feature'
    assert property_page.code_input.input_value() == '302', 'Wrong Status Code'
    assert property_page.source_input.text_content() == '(.*)', 'Wrong Source'
    assert property_page.destination_input.text_content() == 'https://www.example.com$1', 'Wrong Destination'
    assert not property_page.rule_checkbox.is_checked(), "Wrong 'ignore case'"


def test_rules_ia_compress_content(property_page):
    """Rules - AI rule - compress JavaScript and CSS files

        Preconditions:
        --------------
        1. Navigate to Rule tab

        Steps:
        ------
        1. Click 'Add Rules Rule Using AI...'
        2. Fill in the rule 'compress images'
        3. Click 'Generate Rule'
        4. Click on created Condition
        5. Click on created Feature

        Expected Results:
        -----------------
        3. New Rule should be created
        4.1 Variable should be 'Extension'
        4.2 Operator should be 'is one of'
        4.3 Values should be 'png, jpg, jpeg, gif, svg'
        5.1 Feature name should be 'Compress Content Types'
        5.2 Compress Content Types should be 'image/png, image/jpeg, image/gif, image/svg, image/jpg'
        """
    extention_to_compare = ['png', 'jpg', 'jpeg', 'gif', 'svg']
    compress_content_to_compare = ['image/png', 'image/jpeg', 'image/gif', 'image/svg+xml']

    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('compress images')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    assert property_page.variable_input.input_value() == 'Extension', 'Wrong Variable'
    assert property_page.operator_input.input_value() == 'is one of', 'Wrong Operator'
    values_from_the_condifion_field = property_page.match_tags_inputs.inner_text()
    make_list_from_string = list(values_from_the_condifion_field.split('\n')[:-1])
    assert make_list_from_string == extention_to_compare
    property_page.close.click()
    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Compress Content Types', 'Wrong Feature'
    values_from_the_feature_field = property_page.match_compress_content_type_inputs.inner_text()
    make_list_from_string = list(values_from_the_feature_field.split('\n')[:-1])
    assert make_list_from_string == compress_content_to_compare, 'Wrong Source'


def test_rules_ia_cache_key_query_string_include_option(property_page):
    """Rules - AI rule - include only id and type query parameters in the cache key

        Preconditions:
        --------------
        1. Navigate to Rule tab

        Steps:
        ------
        1. Click 'Add Rules Rule Using AI...'
        2. Fill in the rule 'include only id and type query parameters in the cache key'
        3. Click 'Generate Rule'
        4. Click on created Feature

        Expected Results:
        -----------------
        3. New Rule should be created
        4.1 Feature name should be 'Cache Key Query String'
        4.2 Option should be 'Include'
        4.3 Value should be 'Id, Type'
        """
    values_to_compare = ['id', 'type']

    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('include only id and type query parameters in the cache key')
    property_page.generate_rule.click()

    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Cache Key Query String', 'Wrong Feature'
    assert property_page.option_input.input_value() == 'Include', 'Wrong Status Code'
    values_from_the_field = property_page.match_tags_inputs.inner_text()
    make_list_from_string = list(values_from_the_field.split('\n')[:-1])
    assert make_list_from_string == values_to_compare, 'Wrong Source'


def test_rules_ia_remove_all_except_one_cache_key_query(property_page):
    """Rules - AI rule - remove the uid query parameter from the cache key

        Preconditions:
        --------------
        1. Navigate to Rule tab

        Steps:
        ------
        1. Click 'Add Rules Rule Using AI...'
        2. Fill in the rule 'remove the uid query parameter from the cache key'
        3. Click 'Generate Rule'
        4. Click on created Condition
        5. Click on created Feature

        Expected Results:
        -----------------
        3. New Rule should be created
        4.1 Variable should be 'Extension'
        4.2 Operator should be 'equals'
        4.3 Values should be 'uid'
        5.1 Feature name should be 'Cache Key Query String'
        5.1 Feature Option should be 'Include All Except'
        5.2 Value should be 'uid'
        """
    value_to_compare_with = ['uid']

    property_page.add_rule_using_ai.click()
    property_page.add_rule_using_ai_input.fill('remove the uid query parameter from the cache key')
    property_page.generate_rule.click()

    # Validate Condition
    property_page.created_rule(num=-1).condition(num=0).click()
    # There are 2 ways how AI can create a valid rule
    if property_page.variable_input.input_value() == 'Extension':
        assert property_page.operator_input.input_value() == 'equals', 'Wrong Operator'
        assert property_page.value_div.inner_text() == 'uid', 'Wrong Value'
        property_page.close.click()
    else:
        assert property_page.variable_input.input_value() == 'Path', 'Wrong Variable'
        assert property_page.operator_input.input_value() == 'matches (simple)', 'Wrong Operator'
        assert property_page.match_value_regex.inner_text() == '/.*', 'Wrong Value'
        property_page.close.click()

    # Validate Feature
    property_page.created_rule(num=-1).feature(num=0).click()
    assert property_page.feature_input.input_value() == 'Cache Key Query String', 'Wrong Feature'
    assert property_page.option_input.input_value() == 'Include All Except', 'Wrong Feature'
    values_from_the_feature_field = property_page.match_tags_inputs.inner_text()
    make_list_from_string = list(values_from_the_feature_field.split('\n')[:-1])
    assert make_list_from_string == value_to_compare_with, 'Wrong Source'