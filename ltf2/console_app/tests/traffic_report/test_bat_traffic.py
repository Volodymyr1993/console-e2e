import time


def test_bat_traffic_overview(traffic_page):
    """Traffic - Overview BAT, verifying elements are visible

    Preconditions:
    --------------
    1. Navigate to Traffic --> Overview tab

    Steps:
    ------
    1. Verify header is visible
    2. Verify range picker is visible
    3. Verify Data grid is visible
    4. Verify metric selector is visible
    5. Verify filter button from the Data grid is visible
    6. Verify Requests grid is visible
    7. Verify filter button from the Requests grid is visible
    8. Verify Errors grid is visible
    9. Verify filter button from the Errors grid is visible
    10. Verify Rules grid is visible
    11. Verify metric selector from the Rules grid is visible
    12. Verify percentile drop down from the Rules grid is visible
    13. Verify show request count button from the Rules grid is visible
    14. Verify show as percentage of total requests button from the Rules grid is visible

    Expected Results:
    -----------------
    1. header is visible
    2. range picker is visible
    3. Data grid is visible
    4. metric selector is visible
    5. filter button from the Data grid is visible
    6. Requests grid is visible
    7. filter button from the Requests grid is visible
    8. Errors grid is visible
    9. filter button from the Errors grid is visible
    10. Rules grid is visible
    11. metric selector from the Rules grid is visible
    12. percentile drop down from the Rules grid is visible
    13. show request count button from the Rules grid is visible
    14. show as percentage of total requests button from the Rules grid is visible
    """
    assert traffic_page.traffic_header.inner_text() == "Traffic", 'Wrong header'
    assert traffic_page.traffic_24_hours.is_visible(), 'ange selector button is not visible'
    assert traffic_page.traffic_7_days.is_visible(), 'ange selector button is not visible'
    assert traffic_page.traffic_28_days.is_visible(), 'range selector button is not visible'
    assert traffic_page.traffic_metric_selector.is_visible(), 'drop down is not visible'
    assert traffic_page.traffic_requests_grid_summary.inner_text() == "Requests", 'Wrong summary'
    assert traffic_page.traffic_errors_grid_summary.inner_text() == "Errors", 'Wrong summary'
    assert traffic_page.traffic_rules_grid_summary.inner_text() == "Rules", 'Wrong summary'
    assert traffic_page.show_as_percentage_of_total_requests_button.is_visible(), 'button is not visible'
    assert traffic_page.show_request_count_button.is_visible(), 'button is not visible'
    assert traffic_page.traffic_rules_metric_selector.is_visible(), 'button is not visible'
    assert traffic_page.traffic_rules_percentile_selector.is_visible(), 'drop down is not visible'
    assert traffic_page.show_request_count_button.is_visible(), 'button is not visible'
    assert traffic_page.show_as_percentage_of_total_requests_button.is_visible(), 'button is not visible'
    assert traffic_page.traffic_origin_latency_over_time_summary.is_visible(), 'Summary is not visible'


def test_bat_traffic_by_country(traffic_page):
    """Traffic - Geography BAT, verifying elements are visible

    Preconditions:
    --------------
    1. Navigate to Traffic --> By Country tab

    Steps:
    ------
    1. Verify map is visible
    2. Verify country metric selector is visible
    3. Verify percentile selector is visible
    4. Verify Origin Latency by Country grid is visible

    Expected Results:
    -----------------
    1. Map is visible
    2. country metric selector is visible
    3. percentile selector is visible
    4. Origin Latency by Country grid is visible


    """
    traffic_page.country_tab.click()
    time.sleep(1)
    assert traffic_page.country_map.is_visible(), "map is not visible"
    assert traffic_page.country_metric_selector.is_visible(), "selector is not visible"
    assert traffic_page.country_percentile_selector.is_visible(), "selector is not visible"
    assert traffic_page.country_tab_origin_latency_by_country_grid.is_visible(), "grid is not visible"
