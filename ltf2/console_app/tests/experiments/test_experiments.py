import time


def test_experiments_add(experiment_page):
    """Experimentation - Add experiment

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Click on Add experiment button
        2. Fill experiment name
        3. Click on Create button
      Expected results:
      -----------------
        1. Experiment is created
        2. Experiment is present in the list
        3. Deploy button is present
    """
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment_button.click()
    experiment_page.experiment_name_input(id=0).fill(exp_name)
    experiment_page.experiment_name_input(id=0).press("Enter")
    experiment_page.variant_name_input(exp_id=0, var_id=0).fill("test1")
    experiment_page.variant_name_input(exp_id=0, var_id=0).press("Enter")
    experiment_page.variant_name_input(exp_id=0, var_id=1).fill("test2")
    experiment_page.variant_name_input(exp_id=0, var_id=1).press("Enter")
    # wait for deploy button
    deploy_button = experiment_page.deploy_changes_button
    deploy_button.wait_for(timeout=10000)
    # check that experiment name is present
    assert experiment_page.experiment_name(name=exp_name)


def test_experiment_delete(experiment_page):
    """Experimentation - Delete experiment

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Click on Add experiment button
        2. Fill experiment name
        3. Click on Create button
        4. Click on Delete button
        5. Click on Delete confirmation button
      Expected results:
      -----------------
        1. Experiment is deleted
        2. Experiment is not present in the list
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # wait for deploy button
    deploy_button = experiment_page.deploy_changes_button
    deploy_button.wait_for(timeout=10000)
    # check that experiment name is present
    assert experiment_page.experiment_name(name=exp_name)
    # delete experiment
    experiment_page.delete_experiment_list.first.click()
    experiment_page.delete_experiment_confirm_button.click()
    # check that experiment name is not present
    assert not experiment_page.experiment_name(name=exp_name).is_visible()


def test_experiment_edit(experiment_page):
    """Experimentation - Edit experiment

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Click on Add experiment button
        2. Fill experiment name
        3. Click on Create button
        4. Click on Edit button
        5. Change experiment name
        6. Click on Save button
      Expected results:
      -----------------
        1. Experiment is edited
        2. Experiment is present in the list with new name
    """
    # add experiment
    new_exp_name = f"test{int(time.time())}new"
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # wait for deploy button
    deploy_button = experiment_page.deploy_changes_button
    deploy_button.wait_for(timeout=10000)
    # check that experiment name is present
    assert experiment_page.experiment_name(name=exp_name)
    # edit experiment
    experiment_page.experiment_name_input(id=0).fill(new_exp_name)
    experiment_page.experiment_name_input(id=0).press("Enter")
    # check that edited experiment name is present
    assert experiment_page.experiment_name(name=new_exp_name)


def test_experiment_add_variants(experiment_page):
    """Experimentation - Add variants

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Click on Add experiment button
        2. Fill experiment name
        3. Click on Create button
        4. Click on Edit button
        5. Add variants
        6. Click on Save button
      Expected results:
      -----------------
        1. Variants are added
        2. Deployment is successful
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # wait for deploy button
    deploy_button = experiment_page.deploy_changes_button
    deploy_button.wait_for(timeout=10000)
    # check that experiment name is present
    assert experiment_page.experiment_name(name=exp_name)
    # add variants
    experiment_page.add_variant_button.click()
    experiment_page.variant_name_input(exp_id=0, var_id=2).fill("variant3")
    experiment_page.variant_name_input(exp_id=0, var_id=2).press("Enter")
    experiment_page.add_variant_button.click()
    experiment_page.variant_name_input(exp_id=0, var_id=3).fill("variant4")
    experiment_page.variant_name_input(exp_id=0, var_id=3).press("Enter")
    # deploy changes
    experiment_page.deploy_changes()
    assert not experiment_page.deploy_changes_button.is_visible()


def test_experiment_modify_traffic_distribution(experiment_page):
    """Experimentation - Modify traffic distribution

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Add experiment
        2. Modify traffic distribution
        3. Check that wrong percentage message is present
        4. Modify traffic distribution back
        5. Check that wrong percentage message is not present
      Expected results:
      -----------------
        1. Traffic distribution is modifyable
        2. Wrong percentage message is present
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # modify traffic distribution
    experiment_page.variant_percentage_input(exp_id=0, var_id=0).fill("50")
    experiment_page.variant_percentage_input(exp_id=0, var_id=0).press("Enter")
    assert experiment_page.wrong_percentage_message
    # modify traffic distribution back
    experiment_page.variant_percentage_input(exp_id=0, var_id=0).fill("80")
    experiment_page.variant_percentage_input(exp_id=0, var_id=0).press("Enter")
    assert not experiment_page.wrong_percentage_message.is_visible()


def test_experiment_disabling(experiment_page):
    """Experimentation - Disabling experiment

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Add experiment
        2. Disable experiment
        3. Check that experiment is disabled
        4. Enable experiment
        5. Check that experiment is enabled
      Expected results:
      -----------------
        1. Experiment can be disabled/enabled
        2. Disabled/enable experiment can be deployed
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # deploy changes
    experiment_page.deploy_changes()
    # disable experiment
    experiment_page.is_active_checkbox_list.first.click()
    # deploy changes
    experiment_page.deploy_changes()
    # enable experiment
    experiment_page.is_active_checkbox_list.first.click()
    # deploy changes
    experiment_page.deploy_changes()
    assert not experiment_page.deploy_changes_button.is_visible()


def test_experiment_conditions_batch1(experiment_page):
    """Experimentation - Add criteria

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Add experiment
        2. Add criteria
        3. Deploy changes
      Expected results:
      -----------------
        1. Criteria are added
        2. Deployment is successful
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # add conditionts
    experiment_page.condition.add_asn(operator='equals', value='12345')
    experiment_page.condition.add_brand_name(operator='does not match regular expression', value='qwerty',
                                             ignore_case=True)

    experiment_page.condition.add_city(operator='is one of',
                                       value=['Lviv', 'Kyiv'],
                                       ignore_case=True)
    experiment_page.condition.add_cookie(operator='matches regular expression', name='ororo',
                                         value='qwerty')
    experiment_page.condition.add_client_ip(operator='equals', value='1.2.3.4')
    experiment_page.condition.add_continent(operator='is one of', value=['Europe',
                                                                         'North America'])
    experiment_page.condition.add_country(operator='is one of', value=['Ukraine',
                                                                       'United States'])
    experiment_page.condition.add_directory(operator='equals', value='qwerty')
    experiment_page.condition.add_dma_code(operator='equals', value='123',
                                           ignore_case=True)
    experiment_page.condition.add_filename(operator='matches regular expression', value='qwerty',
                                           ignore_case=True)
    experiment_page.condition.add_html_preferred_dtd(
        operator='equals', value='qwerty')
    experiment_page.condition.add_dual_orientation(value='no')
    experiment_page.condition.add_extension(operator='equals', value='qwerty')
    experiment_page.condition.add_image_inlining(value='yes')
    experiment_page.condition.add_is_android(value='no')
    experiment_page.condition.add_is_app(value='no')
    experiment_page.condition.add_is_ios(value='no')
    experiment_page.condition.add_is_robot(value='no')
    experiment_page.condition.add_is_smartphone(value='no')
    experiment_page.condition.add_is_smarttv(value='no')
    experiment_page.condition.add_is_tablet(value='no')
    experiment_page.condition.add_is_touchscreen(value='no')
    experiment_page.condition.add_is_windows_phone(value='no')
    experiment_page.condition.add_is_wireless_device(value='no')
    experiment_page.condition.add_latitude(
        operator='greater than or equal', value='100')
    experiment_page.condition.add_longitude(
        operator='greater than or equal', value='100')
    experiment_page.condition.add_marketing_name(operator='matches regular expression', value='qwerty',
                                                 ignore_case=True)
    experiment_page.condition.add_method(operator='equals', value='GET')
    experiment_page.condition.add_metro_code(operator='equals', value='123')
    experiment_page.condition.add_mobile_browser(
        operator='equals', value='qwerty')
    experiment_page.condition.add_model_name(operator='matches regular expression', value='qwerty',
                                             ignore_case=True)
    experiment_page.condition.add_origin_path(
        operator='matches regular expression', value='qwerty')
    experiment_page.condition.add_path(
        operator='matches regular expression', value='qwerty', ignore_case=True)
    # deploy changes
    experiment_page.deploy_changes()
    assert not experiment_page.deploy_changes_button.is_visible()


def test_experiment_conditions_batch2(experiment_page):
    """Experimentation - Add criteria

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Add experiment
        2. Add criteria
        3. Deploy changes
      Expected results:
      -----------------
        1. Criteria are added
        2. Deployment is successful
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # add conditionts
    experiment_page.condition.add_pop_code(operator='matches regular expression', value='aga',
                                           ignore_case=True)
    experiment_page.condition.add_postal_code(operator='matches regular expression', value='2323',
                                              ignore_case=True)
    experiment_page.condition.add_progressive_download(value='yes')
    experiment_page.condition.add_query(
        operator='matches regular expression', value='qwerty')
    experiment_page.condition.add_query_parameter(
        operator='matches regular expression', name='ororo', value='qwerty')
    experiment_page.condition.add_query_string(operator='matches regular expression', value='qwerty',
                                               ignore_case=True)
    experiment_page.condition.add_referring_domain(operator='matches regular expression', value='qwerty',
                                                   ignore_case=True)
    experiment_page.condition.add_region_code(operator='matches regular expression', value='435',
                                              ignore_case=True)
    experiment_page.condition.add_release_date(
        operator='equals', value='qwerty')
    experiment_page.condition.add_request_header(operator='equals', name='ororo',
                                                 value='qwerty')
    experiment_page.condition.add_resolution_height(
        operator='less than', value=600)
    experiment_page.condition.add_resolution_width(
        operator='less than', value=600)
    experiment_page.condition.add_response_status_code(
        operator='equals', value='200')
    experiment_page.condition.add_scheme(operator='equals', value='HTTP')
    # deploy changes
    experiment_page.deploy_changes()
    assert not experiment_page.deploy_changes_button.is_visible()


def test_experiment_features_batch(experiment_page):
    """Experimentation - Add action

      Preconditions:
      -------------
        1. Open experimentation page
      Steps:
      ------
        1. Add experiment
        2. Add actions
        3. Deploy changes
      Expected results:
      -----------------
        1. Actions are added
        2. Deployment is successful
    """
    # add experiment
    exp_name = f"test{int(time.time())}"
    experiment_page.add_experiment(name=exp_name, variants=[
                                   "variant1", "variant2"])
    # wait for deploy button
    deploy_button = experiment_page.deploy_changes_button
    deploy_button.wait_for(timeout=10000)
    # add actions
    # caching
    experiment_page.feature.add_refresh_zero_byte_cache_files(enable=True)
    experiment_page.feature.add_revalidate_after_origin_unavaliable(
        response_status_code=200, value=100, unit='minutes')
    experiment_page.feature.add_revalidate_while_stale_timer(value=100)
    experiment_page.feature.add_rewrite_cache_key(
        source='source', destination='destination', ignore_case=True)
    experiment_page.feature.add_partial_cache_sharing_min_hit_size(value=200)
    experiment_page.feature.add_set_client_max_age(value=10, unit='minutes')
    experiment_page.feature.add_set_max_age(
        response_status_code=300, value=1, unit='minute')
    experiment_page.feature.add_stale_on_error(enable=True)
    experiment_page.feature.add_stale_while_revalidate(
        value=100, unit='minutes')
    experiment_page.feature.add_expires_header_treatment(
        expires_header_treatment='If missing')
    experiment_page.feature.add_set_service_worker_max_age(
        value=2, unit='hours')
    experiment_page.feature.add_set_client_ip_custom_header(
        header_name='Header')
    experiment_page.feature.add_set_origin(value='origin')
    experiment_page.feature.add_token_auth_ignore_url_case(enable=False)
    # headers
    experiment_page.feature.add_add_response_headers(
        header_name='name', header_value='value')
    experiment_page.feature.add_debug_header(enable=False)
    experiment_page.feature.add_remove_origin_response_headers(
        header_name='name')
    experiment_page.feature.add_remove_response_headers(header_name='name')
    experiment_page.feature.add_set_request_headers(
        header_name='name', header_value='value')
    experiment_page.feature.add_set_response_headers(
        header_name='name', header_value='value')
    # logs
    experiment_page.feature.add_custom_log_field(custom_log_field='log field')
    experiment_page.feature.add_log_query_string(enable=False)
    experiment_page.feature.add_mask_client_subnet(enable=False)
    # origins
    experiment_page.feature.add_max_keep_alive_requests(value=200)
    # response
    experiment_page.feature.add_allow_prefetching_of_uncached_content(
        enable=False)
    experiment_page.feature.add_set_done(enable=False)
    experiment_page.feature.add_set_response_body(body='first\nsecond\nthird')
    experiment_page.feature.add_set_status_code(code=200)
    # set variables
    experiment_page.feature.add_set_variables(name='Name', value='Value')
    # URL
    experiment_page.feature.add_follow_redirects(enable=False)
    experiment_page.feature.add_url_redirect(
        code=300, source='source', destination='destination', ignore_case=True)
    experiment_page.feature.add_rewrite_url(
        source='source', destination='destination', ignore_case=True)
    # deploy changes
    experiment_page.deploy_changes()
    assert not experiment_page.deploy_changes_button.is_visible()
