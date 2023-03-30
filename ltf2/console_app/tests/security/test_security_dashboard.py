from datetime import datetime, timedelta


def test_event_logs_current_time_range(security_logged):
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
    security_logged.time_frame_input.click()
    for li in security_logged.select.li:
        # Get Time Frame name, e.g. Last 15 minutes
        item_name = li.text_content()
        _, *time_range = item_name.split()
        # Select Time Frame
        li.click()
        try:
            number, period = time_range
        except ValueError:
            number, period = 1, f'{time_range[0]}s'

        now = datetime.utcnow()
        # Format UTC 12/12 13:27 - 12/12 13:42
        expected = (f'UTC '
                    f'{(now - timedelta(**{period: int(number)})).strftime("%m/%d %H:%M")}'
                    f' - {now.strftime("%m/%d %H:%M")}')
        assert expected == security_logged.current_time.text_content(), \
            f'Wrong current time for `{item_name}`'
        security_logged.time_frame_input.click()


def test_dashboard_add_filter_and_change_tab(security_logged):
    """ Dashboard - Add Filter and change tab

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Dashboard page should be open

    Steps:
    ------
    1. Select field in Advanced Filters
    2. Fill in 'Exact Value' field
    3. Click 'Add filter' button
    4. Click 'Rate Enforcement' tab

    Expected Results:
    -----------------
    3. Filter should be added near chart in format '<Filter name>: <Filter value>'
    4. Filter should not be applied after switching a tab
    """
    filter_value = 'qwerty'
    security_logged.field_input.click()
    filter_name = security_logged.select.li[-1].text_content()
    security_logged.select.li[-1].click()

    security_logged.value_input.fill(filter_value)
    security_logged.add_filter_button.click()
    f_name = security_logged.filter_names[0].text_content()
    assert f_name == f'{filter_name}:  {filter_value}', \
        "Wrong filter name or value before changing a tab"

    security_logged.rate_enforcement_button.click()

    assert not security_logged.filter_names.is_visible(), \
        "Unexpected filter is applied for another tab"
