import time
from collections import namedtuple

import pytest

from ltf2.console_app.magic.helpers import random_str
from ltf2.console_app.magic.pages.pages import OrgPage


@pytest.mark.regression
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
    orgs_to_delete.append(org_name)
    # Org name is a current organization
    org_page.locator('p', has_text=org_name).wait_for(timeout=5000)
    # Get text of org_switcher_list elements
    org_page.org_switcher_button.click()
    texts = org_page.org_switcher_list.li.all_text_contents()
    # Organization name is in org switcher list
    assert org_name in texts
    # last element is `Create an Organization`
    assert texts[-1] == 'Create an Organization'


@pytest.mark.regression
@pytest.mark.parametrize("role",
                         ['Viewer', 'Security Manager', 'Editor', 'Maintainer', 'Admin'])
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
    4. Choose {role} role
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
    name = f'{random_str(9)}-{int(time.time()*1000)}'
    email = f'{name}@{random_str(5)}.com'
    org_page.members.click()
    org_page.members_table.wait_for(timeout=2000)
    members_count = org_page.members_table.tbody.tr.count()
    org_page.add_member_button.click()
    # Enter user email
    org_page.email.fill(email)
    # Select a Role
    org_page.member_permission(role=role).click()
    org_page.invite_member_button.click()
    # Wait for member to appear in the table
    for _ in range(10):
        if org_page.members_table.tbody.tr.count() > members_count:
            break
        time.sleep(0.5)
    else:
        raise AssertionError("New member was not added")
    # Find a row in the table with the new member
    row = None
    for tr in org_page.members_table.tbody.tr:
        if tr.username.text_content().lower() == name:
            row = tr
            break
    else:
        raise AssertionError("Cannot find a row with the new member")
    # Verify row
    assert not row.member_checkbox.is_checked()
    row.resend_email_button.wait_for(timeout=5000)
    assert row[2].text_content() == f'{email}Resend Email'
    assert row.role.text_content() == f'Organization Role: {role}'


@pytest.mark.regression
@pytest.mark.parametrize("role",
                         ['Viewer', 'Security Manager', 'Editor', 'Maintainer', 'Admin'])
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
    org_page.members_table.wait_for(timeout=2000)
    members_count = org_page.members_table.tbody.tr.count()
    org_page.add_member_button.click()
    # Enter user email
    org_page.email.fill(email)
    # Select a Role
    org_page.member_permission(role=role).click()
    org_page.invite_member_button.click()
    # Wait for member to appear in the table
    for _ in range(10):
        if org_page.members_table.tbody.tr.count() > members_count:
            break
        time.sleep(0.5)
    else:
        raise AssertionError("New member was not added")
    # Find row in the table with new member
    row = None
    for tr in org_page.members_table.tbody.tr:
        if tr.username.text_content().lower() == name:
            row = tr
            break
    else:
        raise AssertionError("Cannot find a row with the new member")
    # Verify row
    assert not row.member_checkbox.is_checked()
    assert row[2].text_content() == email
    assert row.role.text_content() == f'Organization Role: {role}'
