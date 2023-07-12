from datetime import datetime, timedelta


def make_time_frame(time_range: str):
    """ Make expected time value with 1 minute difference (now - 1m, now, now + 1m)

    :param time_range: time range, e.g. '1 day', '6 hours', ...
    :return list of time frames [now - 1m, now, now + 1m] in the following format:
        'UTC 12/12 13:27 - 12/12 13:42'
    """
    try:
        number, period = time_range
    except ValueError:
        number, period = 1, f'{time_range[0]}s'
    now = datetime.utcnow()
    future = now + timedelta(minutes=1)
    past = now - timedelta(minutes=1)
    frames = []
    for t in (past, now, future):
        frames.append(
            f'UTC '
            f'{(t - timedelta(**{period: int(number)})).strftime("%m/%d %H:%M")}'
            f' - {t.strftime("%m/%d %H:%M")}')
    return frames


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
        item_name = li.text_content()
        _, *time_range = item_name.split()
        # Select Time Frame
        li.click()
        actual = dashboard_page.dashboard_current_time.text_content()
        expected = make_time_frame(time_range)
        assert actual in expected, f'Wrong current time for `{item_name}`'
        dashboard_page.dashboard_time_frame_input.click()


def test_dashboard_add_filter_and_change_tab(dashboard_page):
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
   # dashboard_page.apply_filters.click()
    dashboard_page.field_input.click()
    filter_name = dashboard_page.select.li[-1].text_content()
    dashboard_page.select.li[-1].click()
    dashboard_page.value_input.fill(filter_value)
    dashboard_page.value_input.press('Enter')
    f_name = dashboard_page.filter_names[0].text_content()
    assert f_name == f'{filter_name}:  {filter_value}', \
        "Wrong filter name or value before changing a tab"

    dashboard_page.rate_enforcement_button.click()

    assert not dashboard_page.filter_names.is_visible(), \
        "Unexpected filter is applied for another tab"


def test_event_logs_current_time_range(dashboard_page):
    """ Event Logs - Current time range

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Event Logs' on the left sidebar

    Steps:
    ------
    1. Select 'Time Frame'

    Expected Results:
    -----------------
    1. Proper 'Current Time Range' should appear
    """
    dashboard_page.event_log_time_frame_input.click()
    for li in dashboard_page.select.li:
        # Get Time Frame name, e.g. Last 15 minutes
        item_name = li.text_content()
        _, *time_range = item_name.split()
        # Select Time Frame
        li.click()
        actual = dashboard_page.event_log_current_time.text_content()
        expected = make_time_frame(time_range)
        assert actual in expected, f'Wrong current time for `{item_name}`'
        dashboard_page.event_log_time_frame_input.click()


# def test_event_logs_add_filter_and_change_tab(dashboard_page):
#     """ Event Logs - Add Filter and change tab
#
#     Preconditions:
#     --------------
#     1. Navigate to Security tab
#     2. Click 'Event Logs' on the left sidebar
#
#     Steps:
#     ------
#     1. Select field in Advanced Filters
#     2. Fill in 'Exact Value' field
#     3. Click 'Add filter' button
#     4. Click 'Rate Enforcement' tab
#
#     Expected Results:
#     -----------------
#     3. Filter should be added near chart in format '<Filter name>: <Filter value>'
#     4. Filter should not change
#     """
#     filter_value = 'qwerty'
#     dashboard_page.apply_filters.click()
#     dashboard_page.field_input.click()
#     filter_name = dashboard_page.select.li[-1].text_content()
#     dashboard_page.select.li[-1].click()
#
#     dashboard_page.value_input.fill(filter_value)
#     dashboard_page.value_input.press('Enter')
#     f_name = dashboard_page.filter_names[0].text_content()
#     assert f_name == f'{filter_name}:  {filter_value}', "Wrong filter name or value"
#
#     dashboard_page.rate_enforcement_button.click()
#     assert not dashboard_page.filter_names.is_visible(), \
#         "Unexpected filter is applied for another tab"
