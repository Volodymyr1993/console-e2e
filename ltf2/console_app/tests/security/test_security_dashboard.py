from datetime import datetime, timedelta

import pytest


def get_utc_time_range(time_period):
    """
    Generate a time range strings (-1m, now, +1m) based on a specified time period.

    Parameters:
    - time_period (str): A string representing the time period, e.g., 'Last 10 minutes', 'Last 7 days'.

    Returns:
    - str: A formatted string representing the time range in UTC.
           Format: 'Monday, February 28, 2024 at 10:30 AM - Monday, February 28, 2024 at 10:40 AM'.
    """
    now_utc = datetime.now()

    assert 'Last' in time_period, "Wrong time_period format"

    period = time_period.split()[1:]
    if len(period) == 2:
        num, unit = period
        num = int(num)
    elif len(period) == 1:
        # Last hour, Last day
        unit = time_period.split()[1:]
        num = 1
    else:
        raise ValueError("Invalid time_period")

    if 'minute' in unit:
        start_time_utc = now_utc - timedelta(minutes=num)
    elif 'hour' in unit:
        start_time_utc = now_utc - timedelta(hours=num)
    elif 'day' in unit:
        start_time_utc = now_utc - timedelta(days=num)
    else:
        raise ValueError("Invalid time period")
    start_tuple = (start_time_utc - timedelta(minutes=1),
                   start_time_utc,
                   start_time_utc + timedelta(minutes=1))

    end_tuple = (now_utc - timedelta(minutes=1),
                 now_utc,
                 now_utc + timedelta(minutes=1))

    time_ranges = []

    for start, end in zip(start_tuple, end_tuple):
        start_time_str = start.strftime('%A, %B %-d, %Y at %-I:%M %P')
        end_time_str = end.strftime('%A, %B %-d, %Y at %-I:%M %P')
        time_ranges.append(f"{start_time_str} - {end_time_str}")

    return time_ranges

@pytest.mark.regression
def test_dashboard_logs_current_time_range(dashboard_page):
    """ Dashboard - Current time range

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Dashboard page should be open

    Steps:
    ------
    1. Select 'Time Frame'

    Expected Results:
    -----------------
    1. Proper 'Current Time Range' should appear
    """
    dashboard_page.dashboard_time_frame_input.click()
    for li in dashboard_page.select.li:
        # Get Time Frame name, e.g. Last 15 minutes
        time_range = li.text_content()
        # Skip Custom Time Range
        if time_range == 'Custom time range':
            continue
        # Select Time Frame
        li.click()
        actual = dashboard_page.dashboard_current_time.text_content()
        expected = get_utc_time_range(time_range)
        assert actual in expected, f'Wrong current time for `{time_range}`'
        dashboard_page.dashboard_time_frame_input.click()


@pytest.mark.regression
def test_dashboard_add_filter(dashboard_page):
    """ Dashboard - Add Filter

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Dashboard page should be open

    Steps:
    ------
    1. Select field in Advanced Filters
    2. Fill in 'Exact Value' field
    3. Click 'Add filter' button

    Expected Results:
    -----------------
    3. Filter should be added near chart in format '<Filter name>: <Filter value>'
    """
    filter_value = 'qwerty'

    dashboard_page.add_edit_filters.click()
    dashboard_page.add_filter.click()
    dashboard_page.field_input.click()

    filter_name = dashboard_page.select.li[-1].text_content()
    dashboard_page.select.li[-1].click()
    dashboard_page.value_input.fill(filter_value)
    dashboard_page.save.click()
    dashboard_page.apply.click()
    # Validation
    f_name = dashboard_page.filter_names[0].text_content()
    assert f_name == f'{filter_name}={filter_value}', \
        "Wrong filter name"
