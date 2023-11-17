from ltf2.console_app.magic.constants import ORIGINS_COUNTRIES
import pytest

@pytest.mark.regression
def test_metric_selector_main_chart(traffic_page):
    """Traffic - By Country, verifying all drop-downs options are clickable, summary is correct

        Preconditions:
        --------------
        1. Navigate to Traffic --> By Country tab

        Steps:
        ------
        1. Verify response origins-countries request status is 200
        2. Verify all filter options are clickable in the main chart
        3. Verify percentile filter options are clickable

        Expected Results:
        -----------------
        1. response is 200
        2. All filter options are clickable in the main chart
        3. percentile filter options are clickable

        """
    metric_selector_values = [
        'Bytes Transferred',
        'Requests',
        'Errors',
        'Origin TTFB',
        'Response Time',
        'Cache Hit Rate'
    ]

    traffic_page.country_tab.click()

    with traffic_page.expect_response(ORIGINS_COUNTRIES) as response_value:
        response = response_value.value
        assert response.status == 200

    for value in metric_selector_values:
        traffic_page.country_metric_selector.click()
        traffic_page.select_by_name(name=value).click()
        assert traffic_page.country_metric_selector.get_attribute('value') == value
