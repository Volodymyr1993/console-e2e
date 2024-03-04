import pytest
from ltf2.console_app.magic.helpers import random_str
import random


def generate_random_domain():
    tlds = ['.com', '.net', '.org', '.io', '.xyz']
    sub_domain = ['dev.', 'stage.', 'prod.', 'test.']
    random_tld = random.choice(tlds)
    random_sub_domain = random.choice(sub_domain)
    random_domain = 'www.' + random_sub_domain + random_str(20) + random_tld
    return random_domain


@pytest.mark.regression
def test_origins_base_elements(origins_page):
    """Origins - base elements are visible

      Preconditions:
      -------------
        1. Open the Origins page
        2. Add simple origin
      Steps:
      ------
        1. Verify all elements are visible

      Expected results:
      -----------------
        1. All elements are visible
    """
    assert origins_page.instructions_link.is_visible(), 'The Instuctions link is not visible'
    origins_page.add_origin_button.click()
    assert origins_page.origin_name_field(origin=0).is_visible(), 'The Name field is not visible'
    assert origins_page.origin_override_host_headers(origin=0).is_visible(), 'The Override Host Header field is not visible'
    assert origins_page.origin_hostname(origin=0).is_visible(), 'The Origin Hostname field is not visible'
    assert origins_page.origin_scheme(origin=0, row=0).is_visible(), 'The Scheme field is not visible'
    assert origins_page.origin_port(origin=0, row=0).is_visible(), 'The Port field is not visible'
    assert origins_page.origin_ip_version_preference(origin=0, row=0).is_visible(), 'The IP Version Preference field is not visible'
    assert origins_page.origin_add_host.is_visible(), 'The Add Host field is not visible'
    assert origins_page.origin_use_sni.is_visible(), 'The Use SNI checkbox is not visible'
    assert origins_page.origin_use_the_following_sni_field(origin=0).is_visible(), 'The Use the following SNI field is not visible'
    #assert origins_page.allow_self_signed_certs_checkbox.is_visible(), 'The Allow Self Signed Certs checkbox is not visible'
    origins_page.add_pin_button.click()
    assert origins_page.pinned_certs(origin=0, row=0).is_visible(), 'The Pinned Cert(s) field is not visible'
    origins_page.shields_row.click()
    assert origins_page.shields_drop_down(origin=0)[0].is_visible(), 'The Shields APAC drop-down is is not visible'
    assert origins_page.shields_drop_down(origin=0)[1].is_visible(), 'The Shields EMEA drop-down is is not visible'
    assert origins_page.shields_drop_down(origin=0)[2].is_visible(), 'The Shields US East drop-down is is not visible'
    assert origins_page.shields_drop_down(origin=0)[3].is_visible(), 'The Shields US West drop-down is is not visible'
    assert origins_page.origin_json_editor.is_visible(), 'The JSON Editor is is not visible'
    origins_page.origin_json_editor.click()
    origins_page.json_field.wait_for(timeout=10000)
    assert origins_page.origin_editor.is_visible(), 'The Origin Editor is is not visible'
    origins_page.origin_editor.click()
    origins_page.add_origin_button.wait_for(timeout=10000)
    assert origins_page.add_origin_button.is_visible(), 'The Add Origin button is not visible'


@pytest.mark.regression
def test_add_origin_required_fields(origins_page):
    """Origins - Add Origin with all fields

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Scheme default is 'match'
        3. Deploy created origin

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. Default value is correct
        3. All required fields are fulfilled correctly
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    origin_hostname = generate_random_domain()

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)
    # Deploy changes
    origins_page.deploy_changes()

    assert origins_page.origin_name_field(origin=0).input_value() == random_name, "Name field is not as expected"
    assert origins_page.origin_override_host_headers(origin=0).input_value() == override_host_header, \
        "Origin Host Header field is not as expected"
    assert origins_page.origin_use_the_following_sni_field(origin=0).input_value() == override_host_header, \
        "Use the following SNI hint and enforce origin SAN/CN checking field is not as expected"
    assert origins_page.origin_scheme(origin=0, row=0).input_value() == 'match', "Scheme drop-down is not as expected"


@pytest.mark.parametrize("scheme, port, ip_version",
                         [
                             pytest.param('match', None, 'IPv4 Preferred', id="variant 1"),
                             pytest.param('http', '80', 'IPv6 Preferred', id="variant 2"),
                             pytest.param('https', '443', 'IPv4 Only', id="variant 3"),
                             pytest.param('https', '443', 'IPv6 Only', id="variant 4"),
                             pytest.param('match', None, None, id="variant 5")
                         ])
@pytest.mark.regression
def test_scheme_port_ip_version_combination(origins_page, scheme, port, ip_version):
    f"""Origins - Verify different combination with Scheme, Port, IP Version Preference fields

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Fulfill the Scheme field - {scheme}
        2. Fulfill the Port field - {port}
        2. Fulfill the IP Version Preference field - {ip_version}

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. All fields are fulfilled correctly
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    origin_hostname = generate_random_domain()

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)

    origins_page.origin_scheme(origin=0, row=0).click()
    origins_page.select_by_name(name=scheme).click()
    if scheme is not 'match':
        origins_page.origin_port(origin=0, row=0).fill(port)
    origins_page.origin_ip_version_preference(origin=0, row=0).click()
    origins_page.select_by_name(name=ip_version).click()
    # Deploy changes
    origins_page.deploy_changes()

    assert origins_page.origin_scheme(origin=0, row=0).input_value() == scheme, "Scheme is not as expected"
    if scheme is not 'match':
        assert origins_page.origin_port(origin=0, row=0).input_value() == port, "Port is not as expected"
    assert origins_page.origin_ip_version_preference(origin=0, row=0).input_value() == ip_version, \
        "IP Version Preference field is not as expected"


@pytest.mark.regression
def test_multiple_hostnames(origins_page):
    f"""Origins - Verify adding multiple hostnames 

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Add 2 hostnames with all options
        3. Deploy changes

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. All fields are fulfilled correctly
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    origin_hostname = generate_random_domain()
    protocols = ['http', 'https']
    ports = [80, 443]
    ip_versions = ['IPv4 Preferred', 'IPv4 Only']

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)
    # Add 1st extra hostname to the 1st origin
    origins_page.origin_add_host.click()
    origins_page.origin_hostname(origin=0, row=1).fill(origin_hostname)
    origins_page.origin_scheme(origin=0, row=1).click()
    origins_page.select_by_name(name=protocols[0]).click()
    origins_page.origin_port(origin=0, row=1).fill(ports[0])
    origins_page.origin_ip_version_preference(origin=0, row=1).click()
    origins_page.select_by_name(name=ip_versions[0]).click()
    # Add 2nd extra hostname to the 1st origin
    origins_page.origin_add_host.click()
    origins_page.origin_hostname(origin=0, row=2).fill(origin_hostname)
    origins_page.origin_scheme(origin=0, row=2)
    origins_page.select_by_name(name=protocols[1]).click()
    origins_page.origin_port(origin=0, row=2).fill(ports[1])
    origins_page.origin_ip_version_preference(origin=0, row=2).click()
    origins_page.select_by_name(name=ip_versions[1]).click()
    # Deploy changes
    origins_page.deploy_changes()
    # Verify 1st Origins row
    assert origins_page.origin_hostname(origin=0, row=1).input_value() == origin_hostname, "Origin Hostname is not as expected"
    assert origins_page.origin_scheme(origin=0, row=1).input_value() == protocols[0], "Scheme is not as expected"
    assert origins_page.origin_port(origin=0, row=1).input_value() == ports[0], "Port is not as expected"
    assert origins_page.origin_ip_version_preference(origin=0, row=1).input_value() == ip_versions[0], "IP Version is not as expected"
    # Verify 2nd Origins row
    assert origins_page.origin_hostname(origin=0, row=2).input_value() == origin_hostname, "Origin Hostname is not as expected"
    assert origins_page.origin_scheme(origin=0, row=2).input_value() == protocols[1], "Scheme is not as expected"
    assert origins_page.origin_port(origin=0, row=2).input_value() == ports[1], "Port is not as expected"
    assert origins_page.origin_ip_version_preference(origin=0, row=2).input_value() == ip_versions[1], "IP Version is not as expected"

@pytest.mark.parametrize("balancer_type",
                         [
                             pytest.param('Primary / Failover', id="variant 1"),
                             pytest.param('Round Robin', id="variant 2")
                         ])
@pytest.mark.regression
def test_balancer_types(origins_page, balancer_type):
    f"""Origins - Verify Balancer Types

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Add 2 hostnames with all required options
        3. Select - {balancer_type}
        3. Deploy changes

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. {balancer_type} deployed successfully
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    origin_hostname = generate_random_domain()
    protocols = ['http', 'https']
    ports = [80, 443]
    ip_versions = ['IPv4 Preferred', 'IPv4 Only']

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)
    # if use_sni is False:
    #     assert check_box_status is False, 'Use SNI is not turned off'
    # else:
    #     assert check_box_status is True, 'By default should be turned ON'
    # allow_certs_checkbox = origins_page.allow_self_signed_certs_checkbox.last.is_checked()
    # if allow_self_signed_cert is True:
    #     assert allow_certs_checkbox is True, 'Allow Self Signed Certs is not as expected'
    # else:
    #     assert allow_certs_checkbox is False, 'By default should be turned off'



    # if use_sni is False:
    #     turn_off = origins_page.origin_use_sni.first
    #     turn_off.click()
    # if allow_self_signed_cert is True:
    #     turn_on = origins_page.allow_self_signed_certs_checkbox.last
    #     turn_on.click()
    #check_box_status = origins_page.origin_use_sni.first.is_checked()
    # origins_page.deploy_changes()


