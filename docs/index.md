# edgio-console-app



## Requirements

- Python 3.8+
- pip.conf [configured](https://gitlab.com/groups/limelight-networks/qa/ltf/-/wikis/home#pypi-pip)

## Installation

### 1. Create .ltfrc config file

Example of config in `${HOME}/.ltfrc`:
```ini
[edgio-console-app]
url = https://edgio-stage.app
team = ltf2-e2e
property = component-ui-test
# Can be specified as EDGIO_USER env var
users = <email>
# Can be specified as EDGIO_PASSWORD env var
password = <password>
# Optional. If set, browser will be started in headed mode
headed = True
```

### 2. Create virtualenv and update pip/setuptools

```shell
$ python3 -m venv ~/console/
$ source ~/console/bin/activate
$ pip install -U pip setuptools
```

### 3. Clone edgio-console-app repo into this folder:
```shell
$ git clone git@gitlab.com:limelight-networks/qa/ltf/ltf-projects/edgio-console-app.git
```

### 4. Install LTF edgio-console-app
```shell
$ cd edgio-console-app
$ pip install -e .
```
### 5. Install browsers
```shell
$ playwright install
```

## Running tests
```shell
$ pytest test_team.py
```
### Headed mode
```shell
$ pytest test_team.py --headed
```
or set `headed = True` in `${HOME}/.ltfrc`.

For more details on  usage, CLI arguments and fixtures of `pytest-playwright` go [here](https://playwright.dev/python/docs/test-runners) 