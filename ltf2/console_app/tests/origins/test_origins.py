import pytest
from ltf2.console_app.magic.helpers import random_str
import random
from ltf2.console_app.magic.helpers import deploy_changes


def generate_random_domain():
    tlds = ['.com', '.net', '.org', '.io', '.xyz']
    sub_domain = ['dev.', 'stage.', 'prod.', 'test.']
    random_tld = random.choice(tlds)
    random_sub_domain = random.choice(sub_domain)
    random_domain = 'www.' + random_sub_domain + random_str(20) + random_tld
    return random_domain


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
    deploy_changes(origins_page)
    assert origins_page.origin_name_field(origin=0).input_value() == random_name, "Name field is not as expected"
    assert origins_page.origin_override_host_headers(origin=0).input_value() == override_host_header, \
        "Origin Host Header field is not as expected"
    assert origins_page.origin_use_the_following_sni_field(origin=0).input_value() == override_host_header, \
        "Use the following SNI hint and enforce origin SAN/CN checking field is not as expected"
    assert origins_page.origin_scheme(origin=0, row=0).input_value() == 'match', "Scheme drop-down is not as expected"


@pytest.mark.regression
def test_add_two_origins(origins_page):
    """Origins - Add 2 different Origins

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields for the first one
        2. Fulfill all required fields for the second one
        3. Deploy created origins

      Expected results:
      -----------------
        1. Origins deployed successfully
    """
    # 1st
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    origin_hostname = generate_random_domain()
    # 2nd
    random_name2 = random_str(25)
    override_host_header2 = generate_random_domain()
    origin_hostname2 = generate_random_domain()

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)
    origins_page.add_origin(name=random_name2,
                            override_host_header=override_host_header2,
                            origin_hostname=origin_hostname2,
                            origins_number=1)
    # Deploy changes
    deploy_changes(origins_page)
    assert origins_page.origin_name_field(origin=1).input_value() == random_name2, "Name field is not as expected"
    assert origins_page.origin_override_host_headers(origin=1).input_value() == override_host_header2, \
        "Origin Host Header field is not as expected"
    assert origins_page.origin_use_the_following_sni_field(origin=1).input_value() == override_host_header2, \
        "Use the following SNI hint and enforce origin SAN/CN checking field is not as expected"
    assert origins_page.origin_scheme(origin=1, row=0).input_value() == 'match', "Scheme drop-down is not as expected"


@pytest.mark.parametrize("scheme, port, ip_version",
                         [
                             pytest.param('match', None, 'IPv4 Preferred', id="variant 1"),
                             pytest.param('http', '80', 'IPv6 Preferred', id="variant 2"),
                             pytest.param('https', '443', 'IPv4 Only', id="variant 3"),
                             pytest.param('https', '443', 'IPv6 Only', id="variant 4")
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
    deploy_changes(origins_page)
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
    origin_hostname_second = generate_random_domain()
    origin_hostname_third = generate_random_domain()
    protocols = ['http', 'https']
    ports = ['80', '443']
    ip_versions = ['IPv4 Preferred', 'IPv4 Only']

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)
    # Add 1st extra hostname to the 1st origin
    origins_page.origin_add_host.click()
    origins_page.origin_hostname(origin=0, row=1).fill(origin_hostname_third)
    origins_page.origin_scheme(origin=0, row=1).click()
    origins_page.select_by_name(name=protocols[0]).click()
    origins_page.origin_port(origin=0, row=1).fill(ports[0])
    origins_page.origin_ip_version_preference(origin=0, row=1).click()
    origins_page.select_by_name(name=ip_versions[0]).click()
    # Add 2nd extra hostname to the 1st origin
    origins_page.origin_add_host.click()
    origins_page.origin_hostname(origin=0, row=2).fill(origin_hostname_second)
    origins_page.origin_scheme(origin=0, row=2).click()
    origins_page.select_by_name(name=protocols[1]).click()
    origins_page.origin_port(origin=0, row=2).fill(ports[1])
    origins_page.origin_ip_version_preference(origin=0, row=2).click()
    origins_page.select_by_name(name=ip_versions[1]).click()
    # Deploy changes
    deploy_changes(origins_page)
    # Verify 1st row
    assert origins_page.origin_hostname(origin=0, row=1).input_value() == origin_hostname_third, "Origin Hostname is not as expected"
    assert origins_page.origin_scheme(origin=0, row=1).input_value() == protocols[0], "Scheme is not as expected"
    assert origins_page.origin_port(origin=0, row=1).input_value() == ports[0], "Port is not as expected"
    assert origins_page.origin_ip_version_preference(origin=0, row=1).input_value() == ip_versions[0], "IP Version is not as expected"
    # Verify 2nd row
    assert origins_page.origin_hostname(origin=0, row=2).input_value() == origin_hostname_second, "Origin Hostname is not as expected"
    assert origins_page.origin_scheme(origin=0, row=2).input_value() == protocols[1], "Scheme is not as expected"
    assert origins_page.origin_port(origin=0, row=2).input_value() == ports[1], "Port is not as expected"
    assert origins_page.origin_ip_version_preference(origin=0, row=2).input_value() == ip_versions[1], "IP Version is not as expected"


@pytest.mark.regression
def test_balancer_types(origins_page):
    f"""Origins - Verify Balancer Types

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Add 2 hostnames with all required options
        3. Deploy changes

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. Selected Balancer Type deployed successfully
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    origin_hostname = generate_random_domain()
    origin_hostname_second = generate_random_domain()
    balancer_type = ['Primary / Failover', 'Round Robin']

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=origin_hostname,
                            origins_number=0)
    # Add 1st extra hostname to the 1st origin
    origins_page.origin_add_host.click()
    origins_page.origin_hostname(origin=0, row=1).fill(origin_hostname_second)
    origins_page.balancer_type(origin=0).click()
    origins_page.keyboard.press("Enter")
    # Deploy changes
    deploy_changes(origins_page)
    assert origins_page.balancer_type(origin=0).input_value() == balancer_type[0], "selected Balancer Type is not as expected"
    origins_page.balancer_type(origin=0).click()
    origins_page.keyboard.press("ArrowDown")
    origins_page.keyboard.press("Enter")
    # Deploy changes
    deploy_changes(origins_page)
    assert origins_page.balancer_type(origin=0).input_value() == balancer_type[1], "selected Balancer Type is not as expected"


def test_origin_tls_settings(origins_page):
    f"""Origins - Verify Origin TLS Settings

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Fulfill all Origin TLS Settings fields
        3. Deploy changes

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. Fields fulfilled correctly
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    random_data = generate_random_domain()
    use_sni = origins_page.origin_use_sni
    allow_sert = origins_page.allow_self_signed_certs

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=random_data,
                            origins_number=0)
    use_sni.click()
    allow_sert.click()
    origins_page.origin_use_the_following_sni_field(origin=0).fill(random_data)
    # Deploy Changes
    deploy_changes(origins_page)
    assert use_sni.is_checked() is False
    assert allow_sert.is_checked() is True
    assert origins_page.origin_use_the_following_sni_field(origin=0).input_value() == random_data, "value does not match"


def test_pinned_certs(origins_page):
    f"""Origins - Verify Pinned Certs

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Add few Pinned Certs
        3. Deploy changes

      Expected results:
      -----------------
        1. Origin deployed successfully
        2. Pinned Certs deployed successfully
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    random_data = generate_random_domain()
    random_sha = 'ba7816bf8f01cfea414140de5dae2223b00361aa'
    random_sha2 = 'bb7816bf8f01cfea414140de5dae2223b00361bb'

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=random_data,
                            origins_number=0)
    origins_page.add_pin_button.click()
    origins_page.pinned_certs(origin=0, row=0).fill(random_sha)
    origins_page.add_pin_button.click()
    origins_page.pinned_certs(origin=0, row=1).fill(random_sha2)
    # Deploy Changes
    deploy_changes(origins_page)
    assert origins_page.pinned_certs(origin=0, row=0).input_value() == random_sha, 'SHA is not as expected'
    assert origins_page.pinned_certs(origin=0, row=1).input_value() == random_sha2, 'SHA is not as expected'


@pytest.mark.parametrize("apac, emea, us_east, us_west",
 [
     pytest.param('Bypass', 'Bypass', 'Bypass', 'Bypass', id="variant 1"),
     pytest.param('BLR - Bangalore, India', 'FRB - Frankfurt', 'DCD - Ashburn - PCI', 'DAC - Dallas - PCI', id="variant 2"),
     pytest.param('TIR - Chennai, India', 'FRC - Frankfurt - PCI', 'DCE - Ashburn - PCI', 'DAD - Dallas - PCI', id="variant 3"),
     pytest.param('NDL - Delhi, India', 'HYV - Helsinki', 'AGB - Atlanta', 'DNA - Denver', id="variant 4"),
     pytest.param('FOR - Fortaleza', 'JNB - Johannesburg, South Africa - PCI', 'AGA - Atlanta', 'LAA - Los Angeles', id="variant 5"),
     pytest.param('HKC - Hong Kong', 'LHC - London - PCI', 'AGC - Atlanta - PCI', 'LAC - Los Angeles - PCI', id="variant 6"),
     pytest.param('KHH - Kaohsiung', 'LHD - London - PCI', 'BSB - Boston', 'SAC - San Jose - PCI', id="variant 7"),
     pytest.param('MBW - Melbourne', 'MDR - Madrid - PCI', 'CHA - Chicago', 'SED - Seattle - PCI', id="variant 8"),
     pytest.param('MTY - Monterrey, Mexico - PCI', 'LPL - Manchester - PCI', 'CHD - Chicago - PCI', 'Bypass', id="variant 9"),
     pytest.param('OSA - Osaka - PCI', 'MIL - Milan', 'MIB - Miami', 'Bypass', id="variant 10"),
     pytest.param('RIB - Rio de Janeiro - PCI', 'PAB - Paris', 'MIC - Miami', 'Bypass', id="variant 11"),
     pytest.param('SPB - Sao Paulo, Brazil - PCI', 'PAA - Paris - PCI', 'MID - Miami - PCI', 'Bypass', id="variant 12"),
     pytest.param('SGC - Singapore - PCI', 'RIX - Riga, Latvia', 'NYD - New York - PCI', 'Bypass', id="variant 13"),
     pytest.param('NWA - Sydney - PCI', 'STO - Stockholm', 'PHD - Philadelphia', 'Bypass', id="variant 14"),
     pytest.param('TKB - Tokyo', 'SKA - Stockholm', 'Bypass', 'Bypass', id="variant 15"),
     pytest.param('TKA - Tokyo', 'VIA - Vienna - PCI', 'Bypass', 'Bypass', id="variant 16"),
     pytest.param('TKC - Tokyo - PCI', 'WMI - Warsaw', 'Bypass', 'Bypass', id="variant 17"),
     pytest.param('Bypass', 'AMB - Amsterdam - PCI', 'Bypass', 'Bypass', id="variant 18")
 ])
def test_shields(origins_page, apac, emea, us_east, us_west):
    f"""Origins - Verify Shields

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Fulfill all required fields
        2. Select shield for each region
        3. Deploy changes

      Expected results:
      -----------------
        1. Origin deployed successfully
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    random_hostname = generate_random_domain()

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=random_hostname,
                            origins_number=0)
    # expand the row
    origins_page.shields_row.click()
    # APAC
    origins_page.shields_drop_down(origin=0).first.click()
    origins_page.select_by_name(name=apac).click()
    # EMEA
    origins_page.shields_drop_down(origin=0).nth(1).click()
    origins_page.select_by_name(name=emea).click()
    # US East
    origins_page.shields_drop_down(origin=0).nth(2).click()
    origins_page.select_by_name(name=us_east).click()
    # US WEST
    origins_page.shields_drop_down(origin=0).last.click()
    origins_page.select_by_name(name=us_west).click()
    # Deploy changes
    deploy_changes(origins_page)
    assert origins_page.shields_drop_down(origin=0).first.input_value() == apac, "APAC shield does not match"
    assert origins_page.shields_drop_down(origin=0).nth(1).input_value() == emea, "APAC shield does not match"
    assert origins_page.shields_drop_down(origin=0).nth(2).input_value() == us_east, "US East shield does not match"
    assert origins_page.shields_drop_down(origin=0).last.input_value() == us_west, "US West shield does not match"


def test_json_editor(origins_page):
    f"""Origins - Verify JSON Editor

      Preconditions:
      -------------
        1. Open the Origins page
      Steps:
      ------
        1. Click JSON Editor button
        2. Verify JSON field is visible
        3. Click the Origins Editor

      Expected results:
      -----------------
        1. UI is switching between the JSON and user friendly UI
    """
    random_name = random_str(25)
    override_host_header = generate_random_domain()
    random_hostname = generate_random_domain()

    origins_page.add_origin(name=random_name,
                            override_host_header=override_host_header,
                            origin_hostname=random_hostname,
                            origins_number=0)
    origins_page.origin_json_editor.click()
    origins_page.json_field.wait_for(timeout=20000)
    assert origins_page.json_field.is_visible(), "JSON field is not visible"
    origins_page.origin_editor.click()
    origins_page.origin_add_host.wait_for(timeout=20000)
    assert origins_page.origin_add_host.is_visible(), "Origins Name field is not visible"