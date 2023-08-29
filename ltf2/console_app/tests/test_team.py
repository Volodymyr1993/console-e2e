import time
from collections import namedtuple

import pytest

from ltf2.console_app.magic.helpers import random_str
from ltf2.console_app.magic.pages.pages import OrgPage


def test_create_org(org_page: OrgPage, orgs_to_delete: list):
    """ Organization - Create organization

    Precondition:
    -------------
    1. Navigate to Organization switcher

    Steps:
    ------

    1. Click 'Create an Organization'
    2. Fill in new org name
    3. Click 'Create an Organization'

    Expected Results:
    -----------------
    3. New org should be available in organization switcher
    """
    org_name = f'testname-{time.time()}'
    org_page.org_switcher_button.click()
    assert org_page.org_switcher_list.li[-1].text_content() == 'Create an Organization'
    # Create new org
    org_page.org_switcher_list.li[-1].click()
    org_page.input_name.fill(org_name)
    org_page.button_create_org_dialog.click()
    orgs_to_delete.append((org_page, org_name))
    # Org name is a current organization
    org_page.locator('p', has_text=org_name).wait_for(timeout=5000)
    # Get text of org_switcher_list elements
    org_page.org_switcher_button.click()
    texts = org_page.org_switcher_list.li.all_text_contents()
    # Organization name is in org switcher list
    assert org_name in texts
    # last element is `Create an Organization`
    assert texts[-1] == 'Create an Organization'


@pytest.mark.parametrize("role",
                         ['Read only', 'Purger', 'Member', 'Admin', 'Super Admin'])
def test_org_add_nonexistent_user_(org_page: OrgPage, create_org: str, role: str):
    """ Organization - Add organization member - User is not exist

    Precondition:
    -------------
    1. Create new Organization
    2. Make sure new organization is selected

    Steps:
    ------
    1. Click 'Organization Members'
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
    org_page.members.click()
    org_page.add_member_button.click()
    # Enter user email
    org_page.email.fill(email)
    # Choose Role
    org_page.role_select_input.click()
    for item in org_page.role_select.li:
        if item.text_content() == role:
            item.click()
            break
    org_page.invite_member_button.click()
    # Wait dialog to disappear
    org_page.visible_page_content.wait_for(timeout=5000)
    # Find row in the table with new member
    row = None
    for tr in org_page.members_table.tbody.tr:
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
def test_add_existent_user_(org_page: OrgPage,
                            create_org: str,
                            credentials: namedtuple,
                            role: str):
    """ Organization - Add organization member - User exists

    Precondition:
    -------------
    1. Create new Organization
    2. Make sure new organization is selected

    Steps:
    ------
    1. Click 'Organization Members'
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
    org_page.members.click()
    org_page.add_member_button.click()
    # Enter user email
    org_page.email.fill(email)
    # Choose Role
    org_page.role_select_input.click()
    for item in org_page.role_select.li:
        if item.text_content() == role:
            item.click()
            break
    org_page.invite_member_button.click()
    # Wait dialog to disappear
    org_page.visible_page_content.wait_for(timeout=5000)
    # Find row in the table with new member
    row = None
    for tr in org_page.members_table.tbody.tr:
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
