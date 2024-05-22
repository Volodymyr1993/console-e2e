import pytest
from ltf2.console_app.magic.helpers import random_str


@pytest.mark.regression
def test_environment_variable_add(env_variable_page):
    """Environment Variables - Add variable

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Add Environment Variable button
        2. Fill key field
        3. Fill value field
        3. Click Add variable button
    Expected results:
    -------------
        1. Experiment is created
        2. Experiment is present in the list
        3. Deploy button is present
    """
    random_key = random_str(15)
    random_value = f"{random_str(15)}\n{random_str(10)}\n{random_str(20)}"

    env_variable_page.add_env_variable_button.click()
    env_variable_page.the_key_field.fill(random_key)
    env_variable_page.the_value_field.fill(random_value)
    env_variable_page.add_variable_button.click()
    assert env_variable_page.deploy_changes_button.is_visible()
    assert env_variable_page.table.tbody.tr.td[0] == random_key, "Key does not match"
    assert env_variable_page.table.tbody.tr.td[1] == random_value, "Value does not match"

    


