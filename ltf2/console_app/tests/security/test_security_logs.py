from datetime import datetime, timedelta

from ltf2.console_app.magic.pages.pages import SecurityPage


def test_logs_current_time_range(event_logs_page: SecurityPage):
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
    event_logs_page.time_frame_input.click()
    for li in event_logs_page.select.li:
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
        assert expected == event_logs_page.current_time.text_content(), \
            f'Wrong current time for `{item_name}`'
        event_logs_page.time_frame_input.click()


def test_logs_add_filter_and_change_tab(event_logs_page: SecurityPage):
    """ Event Logs - Add Filter and change tab

    Preconditions:
    --------------
    1. Navigate to Security tab
    2. Click 'Event Logs' on the left sidebar

    Steps:
    ------
    1. Select field in Advanced Filters
    2. Fill in 'Exact Value' field
    3. Click 'Add filter' button
    4. Click 'Rate Enforcement' tab

    Expected Results:
    -----------------
    3. Filter should be added near chart in format '<Filter name>: <Filter value>'
    4. Filter should not change
    """
    filter_value = 'qwerty'
    event_logs_page.field_input.click()
    filter_name = event_logs_page.select.li[-1].text_content()
    event_logs_page.select.li[-1].click()

    event_logs_page.value_input.fill(filter_value)
    event_logs_page.add_filter_button.click()
    f_name = event_logs_page.filter_names[0].text_content()
    assert f_name == f'{filter_name}:  {filter_value}', "Wrong filter name or value"

    event_logs_page.rate_enforcement_button.click()
    assert not event_logs_page.filter_names.is_visible(), \
        "Unexpected filter is applied for another tab"
