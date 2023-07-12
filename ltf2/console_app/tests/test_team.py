import time
from collections import namedtuple

import pytest

from ltf2.console_app.magic.helpers import random_str
from ltf2.console_app.magic.pages.pages import TeamPage


def test_create_team(team_page: TeamPage, teams_to_delete: list):
    """ Team - Create team

    Precondition:
    -------------
    1. Navigate to Team switcher

    Steps:
    ------
    1. Click 'Create a Team'
    2. Fill in new team name
    3. Click 'Create a Team'

    Expected Results:
    -----------------
    3. New team should be available in team switcher
    """
    team_name = f'testname-{time.time()}'
    team_page.team_switcher_button.click()
    assert team_page.team_switcher_list.li[-1].text_content() == 'Create a Team'
    # Create new team
    team_page.team_switcher_list.li[-1].click()
    team_page.input_name.fill(team_name)
    team_page.button_create_team_dialog.click()
    teams_to_delete.append((team_page, team_name))
    # Team name is a current team
    team_page.locator('p', has_text=team_name).wait_for(timeout=5000)
    # Get text of team_switcher_list elements
    team_page.team_switcher_button.click()
    texts = team_page.team_switcher_list.li.all_text_contents()
    # Team name is in team switcher list
    assert team_name in texts
    # last element is `Create a team`
    assert texts[-1] == 'Create a Team'


@pytest.mark.parametrize("role",
                         ['Read only', 'Purger', 'Member', 'Admin', 'Super Admin'])
def test_team_add_nonexistent_user_(team_page: TeamPage, create_team: str, role: str):
    """ Team - Add team member - User is not exist

    Precondition:
    -------------
    1. Create new Team
    2. Make sure new team is selected

    Steps:
    ------
    1. Click 'Team Members'
    2. Click 'Add Members'
    3. Fill in random email that is not registered in the system
    4. Choose {role} role from dropdown list
    5. Click 'Invite Members'

    Expected Results:
    -----------------
    5. Row with new member should appear in the table with following cells:
        1) Checkbox
        2) '<email> (pending)' text and 'Resend Email' button
        3) Member name from email (<name>@<something>.com)
        4) Member role selected  on step 5
        5) Delete member button
    """
    name = f'{random_str(9)}-{time.time()}'
    email = f'{name}@{random_str(5)}.com'
    team_page.members.click()
    team_page.add_member_button.click()
    # Enter user email
    team_page.email.fill(email)
    # Choose Role
    team_page.role_select_input.click()
    for item in team_page.role_select.li:
        if item.text_content() == role:
            item.click()
            break
    team_page.invite_member_button.click()
    # Wait dialog to disappear
    team_page.visible_page_content.wait_for(timeout=5000)
    # Find row in the table with new member
    row = None
    for tr in team_page.members_table.tbody.tr:
        if tr.username.text_content() == name:
            row = tr
            break
    assert row, 'Cannot find row with new member'
    # Verify row
    assert not row.member_checkbox.is_checked()
    row.resend_email_button.wait_for(timeout=5000)
    assert row[1].text_content() == f'{email} (pending) Resend Email'
    assert row.username.text_content() == name
    assert row.role_input.input_value() == role
    row.delete_member_button.wait_for(timeout=500)


@pytest.mark.parametrize("role",
                        ['Read only', 'Purger', 'Member', 'Admin', 'Super Admin'])
def test_add_existent_user_(team_page: TeamPage,
                            create_team: str,
                            credentials: namedtuple,
                            role: str):
    """ Team - Add team member - User exists

    Precondition:
    -------------
    1. Create new Team
    2. Make sure new team is selected

    Steps:
    ------
    1. Click 'Team Members'
    2. Click 'Add Members'
    3. Fill in email of existed user
    4. Choose {role} role from dropdown list
    5. Click 'Invite Members'

    Expected Results:
    -----------------
    5. Row with new member should appear in the table with following cells:
        1) Checkbox
        2) Email
        3) Member name from email (<name>@<something>.com)
        4) Member role selected  on step 5
        5) Delete member button
    """
    try:
        email = credentials.users[1]
    except IndexError:
        raise AssertionError("At least two users should be specified in .ltfrc")

    name = email.split('@')[0]
    team_page.members.click()
    team_page.add_member_button.click()
    # Enter user email
    team_page.email.fill(email)
    # Choose Role
    team_page.role_select_input.click()
    for item in team_page.role_select.li:
        if item.text_content() == role:
            item.click()
            break
    team_page.invite_member_button.click()
    # Wait dialog to disappear
    team_page.visible_page_content.wait_for(timeout=5000)
    # Find row in the table with new member
    row = None
    for tr in team_page.members_table.tbody.tr:
        if tr.username.text_content() == name:
            row = tr
            break
    assert row, 'Cannot find row with new member'
    # Verify row
    assert not row.member_checkbox.is_checked()
    assert row[1].text_content() == email
    assert row.username.text_content() == name
    assert row.role_input.input_value() == role
    row.delete_member_button.wait_for(timeout=500)
