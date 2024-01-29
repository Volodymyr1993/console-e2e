import time
import pytest
from ltf2.console_app.magic.helpers import random_str, random_bool

@pytest.mark.regression
def test_base_elements(redirect_page):
    """Redirects - base elements are visible

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Verify all elements are visible
      Expected results:
      -----------------
        1. All elements are visible
    """
    random_data = f"test{int(time.time())}"
    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)

    assert redirect_page.add_a_redirect_button.is_visible(), 'Add a redirect button is not visible'
    assert not redirect_page.remove_selected_redirect.is_visible(), 'Button is visible'
    assert redirect_page.default_status_dropdown.is_visible(), 'Default Status drop-down is not visible'
    assert redirect_page.import_button.is_visible(), 'Import button is not visible'
    assert redirect_page.export_button.is_visible(), 'Export button is not visible'
    assert redirect_page.table.is_visible(), 'Table with rows is not visible'
    assert redirect_page.delete_all_checkbox.is_visible(), 'Delete all checkbox is not visible'
    assert redirect_page.first_checkbox_from_the_table.is_visible(), 'First checkbox from the list is not visible'
    assert redirect_page.table_value_to_field.is_visible(), 'FROM field is not visible'
    assert redirect_page.table_value_status_field.is_visible(), 'Status field is not visible'
    assert redirect_page.table_value_to_field.is_visible(), 'TO field is not visible'
    assert redirect_page.table_value_query_field.is_visible(), 'Query string is not visible'
    assert redirect_page.search_field.is_visible(), 'Search field is not visible'
    redirect_page.add_a_redirect_button.click()
    assert redirect_page.redirect_from.is_visible(), 'FROM field is visible is not visible'
    assert redirect_page.redirect_to.is_visible(), 'TO field is not visible'
    assert redirect_page.response_status.is_visible(), 'Response Status is not visible'
    assert redirect_page.forward_query_string.is_visible(), 'Forward query string checkbox is not visible'
    assert redirect_page.cancel_button.is_visible(), 'Cansel button is not visible'
    assert redirect_page.save_redirect_button.is_visible(), 'Add a redirect button is not visible'
    redirect_page.cancel_button.click()
    redirect_page.import_button.click()
    assert redirect_page.import_browse_button.is_visible(), 'Browse button is not visible'
    assert redirect_page.import_override_existing.is_visible(), 'Override button is not visible'
    assert redirect_page.import_append_file.is_visible(), 'Override button is not visible'
    assert redirect_page.upload_redirect_button.is_visible(), 'Override button is not visible'
    assert redirect_page.cancel_button.is_visible(), 'Cancel button is not visible'


@pytest.mark.regression
def test_redirect_add(redirect_page):
    """Redirects - Add redirect

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Click on 'Add a redirect' button
        2. Fill all the fields with random data
        3. Click on 'Add a redirect' button
      Expected results:
      -----------------
        1. Redirect is created
        2. Redirect is present in the list, all fields match imputed values
    """
    redirect_from_value = '/' + random_str(20)
    redirect_to_value = '/' + random_str(20)
    status_value = '302 - Found'

    redirect_page.add_a_redirect_button.click()
    redirect_page.redirect_from.fill(redirect_from_value)
    redirect_page.redirect_to.fill(redirect_to_value)
    redirect_page.response_status.click()
    redirect_page.select_by_name(name=status_value).click()
    redirect_page.forward_query_string.click()
    redirect_page.forward_query_string.set_checked(True)
    redirect_page.save_redirect_button.click()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    assert redirect_page.table_value_from_field.inner_text() == redirect_from_value
    assert redirect_page.table_value_to_field.inner_text() == redirect_to_value
    assert redirect_page.table_value_status_field.inner_text() == '302'
    assert redirect_page.table_value_query_field.inner_text() == 'True'


@pytest.mark.regression
def test_redirect_delete(redirect_page):
    """Redirects - Delete redirect

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Click on 'Add a redirect' button
        2. Fill all the fields with random data
        3. Click on 'Add a redirect' button
        4. Select redirect which are going to delete
        5. Confirm deletion
        6. Verify redirect is deleted
      Expected results:
      -----------------
        1. Redirect is deleted
    """
    random_data = f"test{int(time.time())}"
    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.first_checkbox_from_the_table.set_checked(True)
    redirect_page.remove_selected_redirect.click()
    redirect_page.confirm_remove_redirect.click()
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    assert redirect_page.empty_list_message.is_visible(), 'empty list message is not visible'


@pytest.mark.regression
def test_redirect_update(redirect_page):
    """Redirects - update redirect

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Click on 'Add a redirect' button
        2. Fill all the fields with random data
        3. Click on 'Add a redirect' button
        4. click redirect which are going to update
        5. change fields data
        6. Verify redirect is updated
      Expected results:
      -----------------
        1. Redirect is updated
    """
    status_value = '307 - Temporary Redirect'
    random_data = f"test{int(time.time())}"

    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.table_value_to_field.click()
    new_random_data = f"/test{int(time.time())}"
    redirect_page.redirect_from.clear()
    redirect_page.redirect_to.clear()
    redirect_page.redirect_from.fill(new_random_data)
    redirect_page.redirect_to.fill(new_random_data)
    redirect_page.response_status.click()
    redirect_page.select_by_name(name=status_value).click()
    redirect_page.forward_query_string.click()
    redirect_page.forward_query_string.set_checked(True)
    redirect_page.save_redirect_button.click()
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    assert redirect_page.table_value_from_field.inner_text() == new_random_data
    assert redirect_page.table_value_to_field.inner_text() == new_random_data
    assert redirect_page.table_value_status_field.inner_text() == '307'
    assert redirect_page.table_value_query_field.inner_text() == 'True'


@pytest.mark.regression
def test_redirect_deploy(redirect_page):
    """Redirects - deploy redirect

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Click on 'Add a redirect' button
        2. Fill all the fields with random data
        3. Click on 'Add a redirect' button
        4. click 'Deploy' button
        5. Wait for successful deployment

      Expected results:
      -----------------
        1. Redirect is deployed
        2. Yellow banner disappeared
    """
    random_data = f"test{int(time.time())}"

    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.redeploy_button.click()
    redirect_page.redeploy_confirmation.click()
    # wait for deployment finish
    redirect_page.online_status.wait_for(timeout=15000)
    redirect_page.redirects_page.click()
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    assert not redirect_page.redeploy_button.is_visible(), 'Redeploy button is still visible'
    assert redirect_page.add_a_redirect_button.is_visible()


@pytest.mark.regression
def test_redirect_import_override_option(redirect_page):
    """Redirects - import, override existing redirects

      Preconditions:
      -------------
        1. Open the Redirects page
        2. Add new redirect
      Steps:
      ------
        1. Click on 'Import' button
        2. Choose the 'Override existing list with file content'
        3. Upload valid CSV with redirects
        4. click 'Upload redirects' button
        5. Verify results

      Expected results:
      -----------------
        1. Redirects uploaded successfully
        2. Previous redirects are overroded by new one
    """
    csv_file_name = 'import_test.csv'
    random_data = f"test{int(time.time())}"
    data_to_import = [
        ["/" + random_str(15), "/" + random_str(15), '302', random_bool()]
    ]

    redirect_page.csv_for_import(csv_file_name, data_to_import)
    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.upload_csv_file(csv_file_name)
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    assert redirect_page.table_value_from_field.inner_text() == data_to_import[0][0]
    assert redirect_page.table_value_to_field.inner_text() == data_to_import[0][1]
    assert redirect_page.table_value_status_field.inner_text() == data_to_import[0][2]
    assert redirect_page.table_value_query_field.inner_text() == data_to_import[0][3]


@pytest.mark.regression
def test_redirect_import_append_option(redirect_page):
    """Redirects - import, append file content redirects

      Preconditions:
      -------------
        1. Open the Redirects page
        2. Add new redirect
      Steps:
      ------
        1. Click on 'Import' button
        2. Choose the 'Append file content to existing redirects list'
        3. Upload valid CSV with redirects
        4. click 'Upload redirects' button
        5. Verify results

      Expected results:
      -----------------
        1. Redirects uploaded successfully
        2. Previous redirects are present, new one is in the end of the list
    """
    csv_file_name = 'import_test.csv'
    random_data = f"test{int(time.time())}"
    data_to_import = [
        ["/123", "/321", '302', random_bool()]
    ]

    redirect_page.csv_for_import(csv_file_name, data_to_import)
    redirect_page.add_redirect(from_=random_data, to=random_data)
    count_rows_before_import = redirect_page.table_rows.count()

    redirect_page.upload_csv_file(csv_file_name, False)
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    count_after_append_redirects = redirect_page.table_rows.count()

    assert count_rows_before_import + len(data_to_import) == count_after_append_redirects
    assert redirect_page.table_value_from_field.first.inner_text() == data_to_import[0][0]
    assert redirect_page.table_value_to_field.first.inner_text() == data_to_import[0][1]
    assert redirect_page.table_value_status_field.first.inner_text() == data_to_import[0][2]
    assert redirect_page.table_value_query_field.first.inner_text() == data_to_import[0][3]


@pytest.mark.regression
def test_redirect_export_option(redirect_page):
    """Redirects - Verify Export button

      Preconditions:
      -------------
        1. Open the Redirects page
        2. Import new redirect
      Steps:
      ------
        1. Click on 'Export' button
        2. Verify downloaded CSV values are the same as on UI

      Expected results:
      -----------------
        1. Redirects downloaded successfully
        2. Data is correct
    """
    csv_file_name = 'import_test.csv'
    data_to_import = [
        ["/" + random_str(5), "/" + random_str(5), '302', random_bool()],
        ["/" + random_str(10), "/" + random_str(10), '301', random_bool()],
        ["/" + random_str(15), "/" + random_str(15), '307', random_bool()]
    ]
    expected_content = [
        ["from", "to", "status", "forwardQueryString"],
        [data_to_import]
    ]
    redirect_page.csv_for_import(csv_file_name, data_to_import)
    redirect_page.upload_csv_file(csv_file_name, True)
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    with redirect_page.expect_download() as download_info:
        redirect_page.export_button.click()
    download = download_info.value
    download.save_as("" + download.suggested_filename)
    assert redirect_page.verify_exported_csv(download.suggested_filename, expected_content) == True


@pytest.mark.regression
def test_redirect_search(redirect_page):
    """Redirects - search field

      Preconditions:
      -------------
        1. Open the Redirects page
        2. Import new redirects
      Steps:
      ------
        1. Click on 'Search' field
        2. Type existing value

      Expected results:
      -----------------
        1. Redirects was found successfully
    """
    csv_file_name = 'import_test.csv'
    random_from = '/' + random_str(5)
    random_to = '/' + random_str(5)
    data_to_import = [
        ["/" + random_str(5), "/" + random_str(5), '302', random_bool()],
        ["/" + random_str(5), "/" + random_str(5), '301', random_bool()],
        ["/" + random_str(5), "/" + random_str(5), '301', random_bool()],
        ["/" + random_str(5), "/" + random_str(5), '301', random_bool()],
        ["/" + random_str(5), "/" + random_str(5), '301', random_bool()],
        [random_from, "/" + random_str(5), '301', random_bool()],
        ["/" + random_str(5), random_to, '301', random_bool()],
        ["/" + random_str(5), "/" + random_str(5), '307', random_bool()]
        ]
    redirect_page.csv_for_import(csv_file_name, data_to_import)
    redirect_page.upload_csv_file(csv_file_name, True)
    redirect_page.reload()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)

    redirect_page.search_field.click()
    redirect_page.search_field.fill(random_from)
    time.sleep(2)
    assert redirect_page.table_value_from_field.inner_text() == random_from, \
        'The search result does not match the expected'
    assert len(redirect_page.table_rows) == 1, "More rows are present than expected"

    redirect_page.search_field.clear()
    redirect_page.search_field.fill(random_to)
    time.sleep(2)
    assert redirect_page.table_value_to_field.inner_text() == random_to, \
        'The search result does not match the expected'
    assert len(redirect_page.table_rows) == 1, "More rows are present than expected"

    redirect_page.search_field.clear()
    redirect_page.search_field.fill(random_str(10))
    time.sleep(2)
    assert redirect_page.no_redirects_matching.is_visible(), "Empty field text is not visible"