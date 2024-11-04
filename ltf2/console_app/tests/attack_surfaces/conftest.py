from typing import Generator
from urllib.parse import urljoin

import pytest
import requests
from playwright.sync_api import TimeoutError
from playwright.sync_api import Page

from ltf2.console_app.magic.constants import PAGE_TIMEOUT
from ltf2.console_app.magic.pages.pages import AttackSurfacesPage


@pytest.fixture
def cleanup(collections_page, base_url, ltfrc_console_app):
    collections = []

    yield collections

    collections_page.goto(f'{urljoin(base_url, ltfrc_console_app["team"])}/security/asm/collections')
    collections_page.wait_for_load_state('networkidle')
    for c in collections:
        collections_page.remove_collection(c)


@pytest.fixture
def open_port(ltfrc_console_app):
    exposure_svc = f'http://{ltfrc_console_app["exposure_service_ip"]}:{ltfrc_console_app["exposure_service_port"]}'

    def _open_port(p_type: str, port: int, tls: str = ""):
        # p_type: nc, http
        # tls: any cert name of exposure/certs folder (without extension)
        r = requests.post(
            exposure_svc,
            json=[
                {"type": p_type, "port": port, "cert": tls},
            ],
        )
        r.raise_for_status()
    yield _open_port
    requests.get(f'{exposure_svc}/clear')


# =============== Pages ======================

@pytest.fixture
def attack_surfaces_logged(
        use_login_state: dict,
        page: Page,
        base_url: str,
        ltfrc_console_app) -> Generator[AttackSurfacesPage, None, None]:
    # Set global timeout
    page.set_default_timeout(PAGE_TIMEOUT)
    main_page = AttackSurfacesPage(page, url=urljoin(base_url, ltfrc_console_app['team']))
    main_page.goto()
    # main_page.attack_surfaces.click()
    # Close the status banner if present
    try:
        main_page.status_snackbar_close.click(timeout=1500)
    except TimeoutError:
        print('Status banner not found')
    yield main_page


@pytest.fixture
def dashboard_page(attack_surfaces_logged) -> Generator[AttackSurfacesPage, None, None]:
    # attack_surfaces_logged.dashboard.click()
    attack_surfaces_logged.goto(f'{attack_surfaces_logged.url}/security/asm/dashboard')
    attack_surfaces_logged.wait_for_load_state('networkidle')
    yield attack_surfaces_logged


@pytest.fixture
def collections_page(attack_surfaces_logged) -> Generator[AttackSurfacesPage, None, None]:
    # attack_surfaces_logged.collections.click()
    attack_surfaces_logged.goto(f'{attack_surfaces_logged.url}/security/asm/collections')
    attack_surfaces_logged.wait_for_load_state('networkidle')
    yield attack_surfaces_logged


@pytest.fixture
def entities_page(attack_surfaces_logged) -> Generator[AttackSurfacesPage, None, None]:
    # attack_surfaces_logged.entities.click()
    attack_surfaces_logged.goto(f'{attack_surfaces_logged.url}/security/asm/entities')
    attack_surfaces_logged.wait_for_load_state('networkidle')
    yield attack_surfaces_logged


@pytest.fixture
def exposures_page(attack_surfaces_logged) -> Generator[AttackSurfacesPage, None, None]:
    # attack_surfaces_logged.exposures.click()
    attack_surfaces_logged.goto(f'{attack_surfaces_logged.url}/security/asm/exposures')
    attack_surfaces_logged.wait_for_load_state('networkidle')
    yield attack_surfaces_logged


@pytest.fixture
def technologies_page(attack_surfaces_logged) -> Generator[AttackSurfacesPage, None, None]:
    # attack_surfaces_logged.technologies.click()
    attack_surfaces_logged.goto(f'{attack_surfaces_logged.url}/security/asm/technologies')
    attack_surfaces_logged.wait_for_load_state('networkidle')
    yield attack_surfaces_logged


@pytest.fixture
def rules_page(attack_surfaces_logged) -> Generator[AttackSurfacesPage, None, None]:
    # attack_surfaces_logged.rules.click()
    attack_surfaces_logged.goto(f'{attack_surfaces_logged.url}/security/asm/rules')
    attack_surfaces_logged.wait_for_load_state('networkidle')
    yield attack_surfaces_logged
