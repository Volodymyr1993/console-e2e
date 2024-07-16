import pytest
from ltf2.console_app.magic.helpers import random_str
from ltf2.console_app.tests.origins.test_origins import generate_random_domain
from urllib.parse import urljoin


@pytest.mark.regression
def test_web_properties_create_new_property(web_properties, ltfrc_console_app):
    f""" Web Property - Create new Property

      Preconditions:
      -------------
        1. 
      Steps:
      ------
        1. Click 'New Property'
        2. Fill all required fields
        3. Click 'Create Property' button

      Expected results:
      -----------------
        1. New Property created successfully
    """
    random_name = random_str(25)
    random_origin = generate_random_domain()
    random_origin_header = generate_random_domain()

    web_properties.add_property(property_name=random_name, origin_name=random_origin, origin_header=random_origin_header)
    assert web_properties.property_name(name=random_name).inner_text() == random_name, "Property Name does not match"
    # Delete property
    path_to_property = urljoin(ltfrc_console_app['url'], f"{ltfrc_console_app['team']}/{random_name}")
    web_properties.delete_property(path_to_property, random_name)


@pytest.mark.regression
def test_web_properties_search(web_properties):
    f""" Web Property - Search

      Preconditions:
      -------------
        1. Should be at least 1 property
      Steps:
      ------
        1. Find property using search

      Expected results:
      -----------------
        1. Property found successfully
    """

    property_name = web_properties.property_cards.nth(0).inner_text().split('\n')[0]
    web_properties.search_field.fill(property_name)
    web_properties.wait_for_timeout(timeout=2000)
    assert web_properties.property_cards.nth(0).inner_text().split('\n')[0] == property_name, "Property is not in the search result"
    assert web_properties.property_cards.count() == 1, 'Expected to see 1'

@pytest.mark.regression
def test_web_properties_order_by(web_properties):
    f""" Web Property - Order By

      Preconditions:
      -------------
        1. Should be at least 1 property
      Steps:
      ------
        1. Order by all types

      Expected results:
      -----------------
        1. Property ordered correctly
    """
    values = [
        'Name (A - Z)',
        'Name (Z - A)',
        'Last Updated (oldest first)',
        'Created (oldest first)',
        'Created (newest first)',
        'Last Updated (newest first)'
    ]

    for value in values:
        web_properties.sorting_drop_down.click()
        web_properties.select_by_name(name=value).click()
        assert web_properties.sorting_drop_down.get_attribute('value') == value