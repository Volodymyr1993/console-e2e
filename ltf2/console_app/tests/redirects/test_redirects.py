import random
import time
import pytest
from ltf2.console_app.magic.helpers import random_str, random_bool, random_int

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
    redirect_page.first_checkbox_from_the_table.wait_for(timeout=5000)
    assert redirect_page.add_a_redirect_button.is_visible(), 'Add a redirect button is not visible'
    assert not redirect_page.remove_selected_redirect.is_visible(), 'Button is visible'
    assert redirect_page.default_status_dropdown.is_visible(), 'Default Status drop-down is not visible'
    assert redirect_page.import_button.is_visible(), 'Import button is not visible'
    assert redirect_page.export_button.is_visible(), 'Export button is not visible'
    assert redirect_page.table.is_visible(), 'Table with rows is not visible'
    assert redirect_page.delete_all_checkbox.is_visible(), 'Delete all checkbox is not visible'
    assert redirect_page.first_checkbox_from_the_table.is_visible(), 'First checkbox from the list is not visible'
    assert redirect_page.table_value_to_field(row=1).is_visible(), 'FROM field is not visible'
    assert redirect_page.table_value_status_field(row=1).is_visible(), 'Status field is not visible'
    assert redirect_page.table_value_to_field(row=1).is_visible(), 'TO field is not visible'
    assert redirect_page.table_value_query_field(row=1).is_visible(), 'Query string is not visible'
    assert redirect_page.search_field.is_visible(), 'Search field is not visible'
    redirect_page.add_a_redirect_button.click()
    redirect_page.redirect_from.wait_for(timeout=5000)
    assert redirect_page.redirect_from.is_visible(), 'FROM field is visible is not visible'
    assert redirect_page.redirect_to.is_visible(), 'TO field is not visible'
    assert redirect_page.response_status.is_visible(), 'Response Status is not visible'
    assert redirect_page.forward_query_string.is_visible(), 'Forward query string checkbox is not visible'
    assert redirect_page.cancel_button.is_visible(), 'Cansel button is not visible'
    assert redirect_page.save_redirect_button.is_visible(), 'Add a redirect button is not visible'
    redirect_page.cancel_button.click()
    redirect_page.import_button.click()
    redirect_page.import_browse_button.wait_for(timeout=5000)
    assert redirect_page.import_browse_button.is_visible(), 'Browse button is not visible'
    assert redirect_page.import_override_existing.is_visible(), 'Override button is not visible'
    assert redirect_page.import_append_file.is_visible(), 'Override button is not visible'
    assert redirect_page.upload_redirect_button.is_visible(), 'Override button is not visible'
    assert redirect_page.cancel_button.is_visible(), 'Cancel button is not visible'


@pytest.mark.regression
@pytest.mark.parametrize("from_, to, status, forward_query_string",
                         [
                            pytest.param('/' + random_str(10), '/' + random_str(10), "301 - Moved Permanently", True, id="random string"),
                            pytest.param('/' + random_int(10), '/' + random_int(10), "302 - Found", True, id="random int"),
                            pytest.param('/$-_.+!*\'()?', '/$-_.+!*\'()?', "307 - Temporary Redirect", False, id="allowed symbols"),
                            pytest.param('/' + random_str(10), '/' + random_str(10), "308 - Permanent Redirect", False, id="Permanent Redirect")
                         ])
def test_redirect_add(redirect_page, from_, to, status, forward_query_string):
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
    redirect_page.add_a_redirect_button.click()
    redirect_page.redirect_from.fill(from_)
    redirect_page.redirect_to.fill(to)
    redirect_page.response_status.click()
    redirect_page.select_by_name(name=status).click()
    redirect_page.forward_query_string.set_checked(forward_query_string)
    redirect_page.save_redirect_button.click()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.table_value_from_field(row=1).inner_text() == from_
    assert redirect_page.table_value_to_field(row=1).inner_text() == to
    assert redirect_page.table_value_status_field(row=1).inner_text() == status[0:3]
    assert redirect_page.table_value_query_field(row=1).inner_text() == str(forward_query_string)


@pytest.mark.regression
def test_redirect_max_allowed(redirect_page):
    """Redirects - Add redirect

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Click on 'Add a redirect' button
        2. Fill all the fields with max allowed data
        3. Click on 'Add a redirect' button
      Expected results:
      -----------------
        1. Redirect is created
        2. Redirect is present in the list, value contains first 20 symbols
    """
    max_allowed_value = '/' + random_str(1)*255
    expected = max_allowed_value[0:20] + "..."
    redirect_page.add_a_redirect_button.click()
    redirect_page.redirect_from.fill(max_allowed_value)
    redirect_page.redirect_to.fill(max_allowed_value)
    redirect_page.save_redirect_button.click()
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.table_value_from_field(row=1).inner_text() == expected
    assert redirect_page.table_value_to_field(row=1).inner_text() == expected


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
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.wait_for_timeout(timeout=2000)

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
    redirect_page.table_value_to_field(row=1).click()
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
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.table_value_from_field(row=1).inner_text() == new_random_data
    assert redirect_page.table_value_to_field(row=1).inner_text() == new_random_data
    assert redirect_page.table_value_status_field(row=1).inner_text() == '307'
    assert redirect_page.table_value_query_field(row=1).inner_text() == 'True'


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
    redirect_page.online_status.wait_for(timeout=60000)
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
    random_data = f"test{int(time.time())}"
    data_to_import = [
        ["/" + random_str(15), "/" + random_str(15), '302', random_bool()]
    ]
    csv_file = redirect_page.csv_for_import(data_to_import)
    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.upload_csv_file(csv_file, True)
    redirect_page.wait_for_timeout(timeout=2500)
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    assert redirect_page.table_value_from_field(row=1).inner_text() == data_to_import[0][0]
    assert redirect_page.table_value_to_field(row=1).inner_text() == data_to_import[0][1]
    assert redirect_page.table_value_status_field(row=1).inner_text() == data_to_import[0][2]
    assert redirect_page.table_value_query_field(row=1).inner_text() == str(data_to_import[0][3])


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
    random_data = f"test{int(time.time())}"
    data_to_import = [
        ["/123", "/321", '302', random_bool()]
    ]
    csv_file = redirect_page.csv_for_import(data_to_import)
    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.wait_for_timeout(timeout=2500)
    count_rows_before_import = redirect_page.table.tbody.tr.count()
    redirect_page.upload_csv_file(csv_file, False)
    redirect_page.wait_for_timeout(timeout=2500)
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    count_after_append_redirects = redirect_page.table.tbody.tr.count()
    assert count_rows_before_import + len(data_to_import) == count_after_append_redirects
    assert redirect_page.table_value_from_field(row=1).first.inner_text() == data_to_import[0][0]
    assert redirect_page.table_value_to_field(row=1).first.inner_text() == data_to_import[0][1]
    assert redirect_page.table_value_status_field(row=1).first.inner_text() == data_to_import[0][2]
    assert redirect_page.table_value_query_field(row=1).first.inner_text() == str(data_to_import[0][3])


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
    data_to_import = [
        ["/" + random_str(5), "/" + random_str(5), '302', 'True'],
        ["/" + random_str(10), "/" + random_str(10), '301', 'False'],
        ["/" + random_str(15), "/" + random_str(15), '307', 'True'],
        ["/" + random_str(15), "/" + random_str(15), '308', 'False']
    ]
    expected_content = [
        ["from", "to", "status", "forwardQueryString"],
        data_to_import
    ]
    csv_file = redirect_page.csv_for_import(data_to_import)
    redirect_page.upload_csv_file(csv_file, True)
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.wait_for_timeout(timeout=1500)
    with redirect_page.expect_download() as download_info:
        redirect_page.export_button.click()
    download = download_info.value
    download.save_as("" + download.suggested_filename)
    redirect_page.verify_exported_csv(download.suggested_filename, expected_content)


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
    csv_file = redirect_page.csv_for_import(data_to_import)
    redirect_page.upload_csv_file(csv_file, True)
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.search_field.click()
    redirect_page.search_field.fill(random_from)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.table_value_from_field(row=1).inner_text() == random_from, \
        'The search result does not match the expected'
    assert len(redirect_page.table.tbody.tr) == 1, "More rows are present than expected"
    redirect_page.search_field.clear()
    redirect_page.search_field.fill(random_to)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.table_value_to_field(row=1).inner_text() == random_to, \
        'The search result does not match the expected'
    assert len(redirect_page.table.tbody.tr) == 1, "More rows are present than expected"
    redirect_page.search_field.clear()
    redirect_page.search_field.fill(random_str(10))
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.no_redirects_matching.is_visible(), "Empty field text is not visible"


@pytest.mark.regression
def test_redirect_changing_default_status(redirect_page):
    """Redirects - changing the default status

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Select the Default Status -> any
        2. Click the 'Add a redirect' button
        3. Add a few redirects with the default status
        4. Change the default status in the main drop-down

      Expected results:
      -----------------
        1. Default status was changed successfully for the redirects which were created from stem 3.
    """
    random_data = f"test{int(time.time())}"
    set_default = '301 - Moved Permanently'
    new_default = '308 - Permanent Redirect'
    redirect_page.default_status_dropdown.click()
    redirect_page.select_by_name(name=set_default).click()
    redirect_page.add_redirect(from_=random_data, to=random_data)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.table_value_status_field(row=1).inner_text() == 'Default (301)'
    redirect_page.default_status_dropdown.click()
    redirect_page.select_by_name(name=new_default).click()
    assert redirect_page.table_value_status_field(row=1).inner_text() == 'Default (308)'


@pytest.mark.regression
def test_redirect_import_duplicate_values(redirect_page):
    """Redirects - import duplicate values

      Preconditions:
      -------------
        1. Open the Redirects page
      Steps:
      ------
        1. Import file with valid redirects
        2. Import the same file one more time using append option

      Expected results:
      -----------------
        1. duplicate error occurs
    """
    data_to_import = [
        ["/123", "/321", '302', 'True']
    ]
    csv_file = redirect_page.csv_for_import(data_to_import)
    redirect_page.upload_csv_file(csv_file, True)
    csv_file.seek(0)
    redirect_page.upload_csv_file(csv_file, False)
    redirect_page.wait_for_timeout(timeout=1500)
    assert redirect_page.client_snackbar.text_content() == f"Redirect {data_to_import[0][0]} is already defined on this environment."


@pytest.mark.regression
def test_redirect_import_mapping(redirect_page):
    """Redirects - Verify imported values match UI

      Preconditions:
      -------------
        1. Open the Redirects page
        2. Import redirects
      Steps:
      ------
        1. Import CSV with all statuses and forward query strings combinations

      Expected results:
      -----------------
        1. Redirects uploaded successfully
        2. Mapping results match expectations
    """
    data_to_import = [
        ["/" + random_str(15), "/" + random_str(15), '301', "True"],
        ["/" + random_str(15), "/" + random_str(15), '302', "False"],
        ["/" + random_str(15), "/" + random_str(15), '307', "true"],
        ["/" + random_str(15), "/" + random_str(15), '308', "false"],
        ["/" + random_str(15), "/" + random_str(15), '308', True],
        ["/" + random_str(15), "/" + random_str(15), '308', False]
    ]
    csv_file = redirect_page.csv_for_import(data_to_import)
    redirect_page.upload_csv_file(csv_file)
    redirect_page.add_a_redirect_button.wait_for(timeout=30000)
    redirect_page.wait_for_timeout(timeout=1500)
    for row_number in range(1, len(redirect_page.table.tbody.tr) + 1):
        assert redirect_page.table_value_from_field(row=row_number).inner_text() == data_to_import[row_number - 1][0]
        assert redirect_page.table_value_to_field(row=row_number).inner_text() == data_to_import[row_number - 1][1]
        assert redirect_page.table_value_status_field(row=row_number).inner_text() == data_to_import[row_number - 1][2]
        assert redirect_page.table_value_query_field(row=row_number).inner_text() == str(data_to_import[row_number - 1][3]).capitalize()