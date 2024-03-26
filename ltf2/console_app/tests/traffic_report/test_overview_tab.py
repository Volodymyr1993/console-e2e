import time
from datetime import date, timedelta, datetime

from ltf2.console_app.magic.constants import TRAFFIC_ROUTES, ORIGINS_OVERTIME, TRAFFIC_OVERTIME, ERRORS_OVERTIME, DATA_USAGE_OVERTIME
import pytest


@pytest.mark.regression
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
        'Data Transferred Edge': 'Total:',
        'Data Transferred Origin' : 'Total:',
        'Throughput Edge': 'Average:',
        'Throughput Origin': 'Average:',
        'Requests Rate Edge': 'Average:',
        'Requests Rate Origin': 'Average:'

    }

    traffic_page.traffic_metric_selector.click()
    for key, value in metric_selector_values.items():
        traffic_page.select_by_name(name=key).click()
        traffic_page.traffic_metric_selector.click()
        assert traffic_page.traffic_main_chart_summary.inner_text().split()[0] == value, "Wrong summary"

    traffic_page.chart_filter_button[0].click()
    assert traffic_page.chart_filter_button_deployments[0].is_checked() is True
    assert traffic_page.chart_filter_button_full_cache_flushes[0].is_checked() is True


@pytest.mark.regression
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


@pytest.mark.regression
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
    # Verify that response is 200 while first entering hte page
    with traffic_page.expect_response(ORIGINS_OVERTIME) as response_info_origin:
        response = response_info_origin.value
        assert response.status == 200

    # default percentile is 75
    assert traffic_page.traffic_origin_latency_percentile_selector.get_attribute('value') == 'p75'

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


@pytest.mark.regression
def test_date_picker_traffic_overview(traffic_page):
    """Traffic - Date Picker selector

        Preconditions:
        --------------
        1. Navigate to Traffic --> Overview tab

        Steps:
        ------
        1. Verify Today, Last 24 Hours, Last 7 Days, This Month, Last Month, Last 30 Days, Last 90 Day  from the date picker

        Expected Results:
        -----------------
        1. ranges are selected correctly
        """

    date_picker_options = {
        traffic_page.date_picker_today: 'Today',
        traffic_page.date_picker_last_24_hours: 'Last 24 Hours',
        traffic_page.date_picker_last_7_days: 'Last 7 Days',
        traffic_page.date_picker_this_month: 'This Month',
        traffic_page.date_picker_last_month: 'Last Month',
        traffic_page.date_picker_last_30_days: 'Last 30 Days',
        traffic_page.date_picker_last_90_days: 'Last 90 Days',
    }

    # default day is Last 30 Days
    assert traffic_page.date_picker.inner_text() == 'Last 30 Days'

    # Verify all values from the date picker are clickable
    for key, value in date_picker_options.items():
        traffic_page.reload()
        traffic_page.date_picker.click()
        with traffic_page.expect_response(TRAFFIC_OVERTIME) as response:
            key.click()
            response_info = response.value
        assert response_info.status == 200
        assert traffic_page.date_picker.inner_text() == value


@pytest.mark.regression
def test_date_picker_monthly(traffic_page):
    """Traffic - Daily and Monthly ranges

        Preconditions:
        --------------
        1. Navigate to Traffic --> Overview tab

        Steps:
        ------
        1. Verify Daily is range selected
        2. Verify Monthly range is selected

        Expected Results:
        -----------------
        1. Daily is range selected
        2. Monthly range is selected
        """

    today_date = date.today()

    custom_ranges = {
        traffic_page.date_picker_daily: '%d %b %Y',
        traffic_page.date_picker_monthly: '%b %Y'
    }

    for item, time_format in custom_ranges.items():
        traffic_page.date_picker.click()
        item.click()
        with traffic_page.expect_response(DATA_USAGE_OVERTIME) as response:
            traffic_page.date_picker_apply_button.click()
            response_info = response.value
        assert response_info.status == 200
        assert traffic_page.date_picker.inner_text() == today_date.strftime(time_format)


def test_date_picker_custom_date_range(traffic_page):
    """Traffic - Custom Date Range

        Preconditions:
        --------------
        1. Navigate to Traffic --> Overview tab

        Steps:
        ------
        1. Verify Custom Date Range

        Expected Results:
        -----------------
        1. Custom Date Range is range selected
    """

    today = datetime.now()
    thirty_days_ago = today - timedelta(days=29)
    date_range_format = f"{thirty_days_ago.strftime('%d %b %Y')} - {today.strftime('%d %b %Y')}"

    traffic_page.date_picker.click()
    traffic_page.date_picker_last_7_days.click()
    traffic_page.reload()
    traffic_page.date_picker.click()
    traffic_page.date_picker_custom_date_range.click()
    with traffic_page.expect_response(ERRORS_OVERTIME) as response:
        traffic_page.date_picker_apply_button.click()
        response_info = response.value
    assert response_info.status == 200
    assert traffic_page.date_picker.inner_text() == date_range_format