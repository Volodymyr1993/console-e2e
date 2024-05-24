import pytest
from ltf2.console_app.magic.helpers import random_str


@pytest.mark.regression
def test_add_environment_variable(env_variable_page):
    """Environment Variables - Add variable

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Add Environment Variable button
        2. Fill key field
        3. Fill value field
        4. Click Add variable button
    Expected results:
    -------------
        1. Environment Variable is created
        2. Environment Variable is present in the list
        3. Deploy button is present
    """
    random_key = random_str(15)
    random_value = f"{random_str(15)},{random_str(10)},{random_str(20)}"

    env_variable_page.add_env_variable(random_key, random_value, False)
    env_variable_page.wait_for_timeout(timeout=1500)
    assert env_variable_page.redeploy_button.is_visible()
    assert env_variable_page.row_key(row=1).inner_text() == random_key, "Key does not match"
    assert env_variable_page.row_value(row=1).inner_text() == random_value, "Value does not match"


@pytest.mark.regression
def test_add_env_var_with_secret_value(env_variable_page):
    """Environment Variables - Add variable with secret value

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Add Environment Variable button
        2. Fill key field
        3. Fill value field
        4. Set Keep this value a secret TRUE
        3. Click Add variable button
    Expected results:
    -------------
        1. Environment Variable is created
        2. Environment Variable is present in the list
        3. Data is secret
    """
    random_key = random_str(15)
    random_value = random_str(15)

    env_variable_page.add_env_variable(random_key, random_value, True)
    env_variable_page.add_variable_button.click()
    env_variable_page.wait_for_timeout(timeout=1500)
    assert env_variable_page.row_key(row=1).inner_text() == random_key, "Key does not match"
    assert env_variable_page.row_value(row=1).inner_text() == "****" + random_value[12:15], "Value does not match"
    

@pytest.mark.regression
def test_import_env_var(env_variable_page):
    """Environment Variables - Import variable

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Import Environment Variable button
        2. Fill the key/value field
        3. Click Add variable button
    Expected results:
    -------------
        1. Environment Variable is created
        2. Environment Variable is present in the list
    """
    random_key = random_str(15)
    random_value = f"{random_str(15)}"
    random_data = f"{random_key}=" + random_value

    env_variable_page.import_env_variable(random_data, False)
    env_variable_page.wait_for_timeout(timeout=1500)
    assert env_variable_page.redeploy_button.is_visible()
    assert env_variable_page.row_key(row=1).inner_text() == random_key, "Key does not match"
    assert env_variable_page.row_value(row=1).inner_text() == random_value, "Value does not match"


@pytest.mark.regression
def test_import_env_var_secret(env_variable_page):
    """Environment Variables - Import variable with secret

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Import Environment Variable button
        2. Fill the key/value field
        3. Click the 'Keep values secret' checkbox
        4. Click Add variable button
    Expected results:
    -------------
        1. Environment Variable is created
        2. Environment Variable is present in the list
        3. Data is secret
    """
    random_key = random_str(15)
    random_value = f"{random_str(15)}"
    random_data = f"{random_key}=" + random_value

    env_variable_page.import_env_variable(random_data, True)
    env_variable_page.wait_for_timeout(timeout=1500)
    assert env_variable_page.row_key(row=1).inner_text() == random_key, "Key does not match"
    assert env_variable_page.row_value(row=1).inner_text() == "****" + random_value[12:15], "Value does not match"


@pytest.mark.regression
def test_env_var_deploy_now(env_variable_page):
    """Environment Variables - Deploy Environment Variable

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Add Environment Variable button
        2. Fill key field
        3. Fill value field
        4. Click Add variable button
        5. Click the 'Deploy Now' button
    Expected results:
    -------------
        1. Environment Variable is created
        2. Environment Variable is present in the list
        3. Deploy successfully
    """
    random_key = random_str(15)
    random_value = f"{random_str(15)},{random_str(10)},{random_str(20)}"

    env_variable_page.add_env_variable(random_key, random_value, False)
    env_variable_page.redeploy_button.wait_for(timeout=2000)
    env_variable_page.redeploy_button.click()
    env_variable_page.deploy_confirmation.click()
    # wait for deployment finish
    env_variable_page.online_status.wait_for(timeout=60000)
    env_variable_page.env_page.click()
    env_variable_page.add_env_variable_button.wait_for(timeout=30000)
    env_variable_page.wait_for_timeout(timeout=1500)
    assert not env_variable_page.redeploy_button.is_visible()
    assert env_variable_page.row_key(row=1).inner_text() == random_key, "Key does not match"
    assert env_variable_page.row_value(row=1).inner_text() == random_value, "Value does not match"


@pytest.mark.regression
def test_import_env_var_deploy_secret(env_variable_page):
    """Environment Variables - Deploy Environment Variable

    Preconditions:
    -------------
        1. Open the Environment Variables page
      Steps:
    -------------
        1. Click Add Environment Variable button
        2. Fill key field
        3. Fill value field
        4. Click the 'Keep values secret' checkbox
        5. Click the 'Deploy Now' button
    Expected results:
    -------------
        1. Environment Variable is created
        2. Environment Variable is present in the list
        3. Data is secret
    """
    random_key = random_str(15)
    random_value = random_str(15)

    env_variable_page.add_env_variable(random_key, random_value, True)
    env_variable_page.add_variable_button.click()
    env_variable_page.redeploy_button.wait_for(timeout=2000)
    env_variable_page.redeploy_button.click()
    env_variable_page.deploy_confirmation.click()
    # wait for deployment finish
    env_variable_page.online_status.wait_for(timeout=60000)
    env_variable_page.env_page.click()
    env_variable_page.add_env_variable_button.wait_for(timeout=30000)
    env_variable_page.wait_for_timeout(timeout=1500)
    assert not env_variable_page.redeploy_button.is_visible()
    assert env_variable_page.row_key(row=1).inner_text() == random_key, "Key does not match"
    assert env_variable_page.row_value(row=1).inner_text() == "****" + random_value[12:15], "Value does not match"