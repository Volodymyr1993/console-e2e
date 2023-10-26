from ltf2.console_app.magic.constants import TRAFFIC_ROUTES, ORIGINS_OVERTIME


def test_metric_selector_main_chart(traffic_page):
    """Traffic - Overview, verifying all filter options are clickable, summary is correct, all buttons are clickable

        Preconditions:
        --------------
        1. Navigate to Traffic --> Overview tab

        Steps:
        ------
        1. Verify all filter options are clickable in the main chart
        2. Verify summary for each option is correct
        3. Verify the chart setting filter buttons are clickable


        Expected Results:
        -----------------
        1. All filter options are clickable in the main chart
        2. summary for each option is correct
        3. the chart setting filter buttons are clickable

        """
    metric_selector_values = {
        'Data Transferred Out': 'Total:',
        'Data Transferred In' : 'Total:',
        'Throughput Out': 'Average:',
        'Throughput In': 'Average:',
        'Requests Rate Edge': 'Average:',
        'Requests Rate Origin': 'Average:'

    }

    traffic_page.traffic_metric_selector.click()
    for key, value in metric_selector_values.items():
        traffic_page.select_by_name(name=key).click()
        traffic_page.traffic_metric_selector.click()
        assert  traffic_page.traffic_main_chart_summary.inner_text().split()[0] == value, "Wrong summary"

    traffic_page.chart_filter_button[0].click()
    assert traffic_page.chart_filter_button_deployments[0].is_checked() is True
    assert traffic_page.chart_filter_button_full_cache_flushes[0].is_checked() is True


def test_rules_grid_buttons_check(traffic_page):
    """Traffic - Overview, Rules grig filters, buttons

        Preconditions:
        --------------
        1. Navigate to Traffic --> Overview tab

        Steps:
        ------
        1. Verify all main filter options are clickable in the Rules chart
        2. Verify all percentile filter options are clickable in the Rules chart
        3. Verify 'Show request count' button is clickable
        4. Verify 'Show as percentage of total requests' button is clickable
        5. Verify response status code is 200 after clicking buttons


        Expected Results:
        -----------------
        1. all main filter options are clickable in the Rules chart
        2. all percentile filter options are clickable in the Rules chart
        3. 'Show request count' button is clickable
        4. 'Show as percentage of total requests' button is clickable
        5. response status code is 200 after clicking buttons

        """
    rules_metrics_selector = ['TTFB', 'Response Time']
    traffic_page.traffic_rules_metric_selector.click()
    for value in rules_metrics_selector:
        with traffic_page.expect_response(TRAFFIC_ROUTES) as response_info:
            traffic_page.select_by_name(name=value).click()
        response = response_info.value
        assert response.status == 200
        assert traffic_page.traffic_rules_metric_selector.get_attribute('value') == value
        traffic_page.traffic_rules_metric_selector.click()

    # Default selected percentile is p75
    assert traffic_page.traffic_rules_percentile_selector.get_attribute('value') == 'p75'

    rules_percentiles_selector = ['p95', 'p99']
    traffic_page.traffic_rules_percentile_selector.click()
    for value in rules_percentiles_selector:
        with traffic_page.expect_response(TRAFFIC_ROUTES) as response_percentile:
            traffic_page.select_by_name(name=value).click()
        response = response_percentile.value
        assert response.status == 200
        assert traffic_page.traffic_rules_percentile_selector.get_attribute('value') == value
        traffic_page.traffic_rules_percentile_selector.click()

    traffic_page.show_as_percentage_of_total_requests_button.click()
    traffic_page.show_request_count_button.click()


def test_origin_latency_over_tyme_grid_buttons_check(traffic_page):
    """Traffic - Overview, Rules grig filters, buttons

        Preconditions:
        --------------
        1. Navigate to Traffic --> Overview tab

        Steps:
        ------
        1. Verify all main filter options are clickable in the Rules chart
        2. Verify all percentile filter options are clickable in the Rules chart
        3. Verify 'Show request count' button is clickable
        4. Verify 'Show as percentage of total requests' button is clickable
        5. Verify response status code is 200 after clicking buttons


        Expected Results:
        -----------------
        1. all main filter options are clickable in the Rules chart
        2. all percentile filter options are clickable in the Rules chart
        3. 'Show request count' button is clickable
        4. 'Show as percentage of total requests' button is clickable
        5. response status code is 200 after clicking buttons

        """
    # default percentile is 75
    assert traffic_page.traffic_origin_latency_percentile_selector.get_attribute('value') == 'p75'
    # Verify that response is 200 while first entering hte page
    with traffic_page.expect_response(ORIGINS_OVERTIME) as response_info_origin:
        response = response_info_origin.value
        assert response.status == 200

    rules_percentiles_selector = ['p95', 'p99']
    traffic_page.traffic_origin_latency_percentile_selector.click()
    for value in rules_percentiles_selector:
        with traffic_page.expect_response(ORIGINS_OVERTIME) as response_percentile:
            traffic_page.select_by_name(name=value).click()
        response = response_percentile.value
        assert response.status == 200
        assert traffic_page.traffic_origin_latency_percentile_selector.get_attribute('value') == value
        traffic_page.traffic_origin_latency_percentile_selector.click()

    # default latency metrick is TTFB
    assert traffic_page.traffic_origin_latency_metrics_selector.get_attribute('value') == 'TTFB'

    rules_metrics_selector = ['Response Time']
    traffic_page.traffic_origin_latency_metrics_selector.click()
    for value in rules_metrics_selector:
        with traffic_page.expect_response(ORIGINS_OVERTIME) as response_metric:
            traffic_page.select_by_name(name=value).click()
        response = response_metric.value
        assert response.status == 200
        assert traffic_page.traffic_origin_latency_metrics_selector.get_attribute('value') == value
        traffic_page.traffic_origin_latency_metrics_selector.click()

    rules_filter_by_selector = ['Show Origin Hostname']
    traffic_page.traffic_origin_latency_drop_down_filter.click()
    for value in rules_filter_by_selector:
        with traffic_page.expect_response(ORIGINS_OVERTIME) as response_info:
            traffic_page.select_by_name(name=value).click()
        response = response_info.value
        assert response.status == 200
        assert traffic_page.traffic_origin_latency_drop_down_filter.get_attribute('value') == value
        traffic_page.traffic_origin_latency_drop_down_filter.click()