import time
from urllib.parse import urljoin
import pytest
from ltf2.console_app.magic.helpers import random_str
from ltf2.console_app.tests.origins.test_origins import generate_random_domain
from datetime import date


@pytest.mark.regression
def test_org_level_activity_bat(org_activity):
    f""" Organization level, Activity - BAT

      Steps:
      ------
        1. Go to the Activity page
        2. Verify Activity header is visible

      Expected results:
      -----------------
        1. All elements are visible
    """
    assert org_activity.activity_header.inner_text() == "Organization Activity", 'Wrong header'
    assert org_activity.table.is_visible(), "The table is not visible"
    assert org_activity.add_filter_button.is_visible(), "The + Add Filter button is not visible"
    rows_count = org_activity.table.tbody.tr.count()
    if rows_count >= 11:
        assert org_activity.show_more_button.is_visible(), "The Show More button is not visible"


@pytest.mark.regression
def test_org_leve_add_all_action_types(org_activity):
    f""" Activity org level, add all action types

      Steps:
      ------
        1. Go to the Activity page
        2. Fulfill all filter fields
        3. add all action types

      Expected results:
      -----------------
        1. Fields are fulfilled correctly
        2. 200 ok responses
        3. filter cleared
    """
    today_date = date.today()
    date_format = today_date.strftime("%m/%d/%Y")
    random_data = random_str(25)
    action_types = ["Account created",
                    "Account removed",
                    "Alert created",
                    "Alert updated",
                    "Alert removed",
                    "Alert disabled",
                    "Alert unsubscribed",
                    "Attack Surfaces - Collection created",
                    "Attack Surfaces - Collection updated",
                    "Attack Surfaces - Collection deleted",
                    "Attack Surfaces - Entity created",
                    "Attack Surfaces - Entity updated",
                    "Attack Surfaces - Entity deleted",
                    "Attack Surfaces - Technology deleted",
                    "Branch created",
                    "Cache purged",
                    "Deployment completed",
                    "Deployment removed",
                    "Deployment failed",
                    "Deployment canceled",
                    "Deployment promoted",
                    "Deployment inactive removed",
                    "Deploy token created",
                    "Deploy token updated",
                    "Deploy token removed",
                    "Environment created",
                    "Environment updated",
                    "Environment removed",
                    "Environment set as production",
                    "Environment version created",
                    "Environment version updated",
                    "Environment version activated",
                    "Environment version draft removed",
                    "Environment variable created",
                    "Environment variable removed",
                    "Environment redirect created",
                    "Purging group created",
                    "Purging group updated",
                    "Purging group removed",
                    "Property created",
                    "Property removed",
                    "Property moved from",
                    "Property moved to",
                    "Property renamed",
                    "Organization created",
                    "Organization renamed",
                    "Organization removed",
                    "Organization member added",
                    "Organization member updated",
                    "Organization member removed"
                    ]

    org_activity.add_filter_button.click()
    org_activity.from_date_field.fill(date_format)
    org_activity.to_date_field.fill(date_format)
    org_activity.filter_search_field.fill(random_data)
    for item in action_types:
        org_activity.filter_action_type_field.click()
        org_activity.select_by_name_extra_level(name=item).click()
        with org_activity.expect_response('**/graphql') as response_value:
            response = response_value.value
            assert response.status == 200
        org_activity.filter_action_type_field.clear()
    org_activity.close.click()
    org_activity.clear_filters_button.click()
