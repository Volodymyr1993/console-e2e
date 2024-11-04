import pytest
import time

from playwright.sync_api import expect


@pytest.fixture()
def reset_rules_to_default(rules_page):
    rules_page.rules_reset_to_defaults_btn.click()
    rules_page.rules_reset_dlg_reset_btn.click()
    rules_page.wait_for_load_state('networkidle')


@pytest.mark.regression
def test_bat(reset_rules_to_default, collections_page, cleanup, ltfrc_console_app, open_port):
    """Attack Surfaces - BAT 1"""
    target_ip = ltfrc_console_app['exposure_service_ip']
    opened_port = 5900
    open_port(p_type='http', port=opened_port)

    coll_name = f'coll-{time.time()}'
    collections_page.create_collection(coll_name)
    cleanup.append(coll_name)
    new_coll = collections_page.get_collections(name_filter=coll_name)
    assert new_coll['name'] == coll_name

    collections_page.open_collection(coll_name)
    collections_page.add_seed(seed_type='IP Address', seed=target_ip)

    collections_page.coll_scan_now_btn.click()
    # expect(collections_page.coll_scan_now_btn._locator, 'Scan was not complete').to_be_enabled(timeout=120*1000)
    collections_page.collections.click()
    collections_page.open_collection(coll_name)
    collections_page.wait_for_scans_completed(timeout=120)

    collections_page.open_scan(0)
    scan_tasks = collections_page.get_scan_tasks()
    collections_page.log.debug(scan_tasks)
    assert all(x['status'].lower() == 'completed' for x in scan_tasks)
    scan_exposures = collections_page.get_scan_exposures()
    collections_page.log.debug(scan_exposures)
    assert f'Open port {opened_port} on {target_ip}' in scan_exposures


# @pytest.mark.regression
# def test_bat_attack_surfaces_dash(dashboard_page):
#     """Attack Surfaces - BAT, Dashboard, verifying elements are visible"""
#     dashboard_page.wait_for_error()
#     assert dashboard_page.dash_header.is_visible(), 'The page header is not visible'  # remove after other asserts are present
#
#
# @pytest.mark.regression
# def test_bat_attack_surfaces_collections(collections_page):
#     """Attack Surfaces - BAT, Collections, verifying elements are visible"""
#     collections_page.wait_for_error()
#     assert collections_page.collections_header.is_visible(), 'The page header is not visible'  # remove after other asserts are present
#
#
# @pytest.mark.regression
# def test_bat_attack_surfaces_assets(entities_page):
#     """Attack Surfaces - BAT, Assets, verifying elements are visible"""
#     entities_page.wait_for_error()
#     assert entities_page.assets_header.is_visible(), 'The page header is not visible'  # remove after other asserts are present
#
#
# @pytest.mark.regression
# def test_bat_attack_surfaces_exposures(exposures_page):
#     """Attack Surfaces - BAT, Exposures, verifying elements are visible"""
#     exposures_page.wait_for_error()
#     assert exposures_page.exposures_header.is_visible(), 'The page header is not visible'
#
#
# @pytest.mark.regression
# def test_bat_attack_surfaces_technologies(technologies_page):
#     """Attack Surfaces - BAT, Technologies, verifying elements are visible"""
#     technologies_page.wait_for_error()
#     assert technologies_page.technologies_header.is_visible(), 'The page header is not visible'  # remove after other asserts are present
#
#
# @pytest.mark.regression
# def test_bat_attack_surfaces(rules_page):
#     """Attack Surfaces - BAT, Rules, verifying elements are visible"""
#     rules_page.wait_for_error()
#     assert rules_page.rules_header.is_visible(), 'The page header is not visible'  # remove after other asserts are present
