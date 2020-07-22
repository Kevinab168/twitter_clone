import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.yield_fixture(scope="session")
def driver():
    if os.environ.get('CI'):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(chrome_options=options)
    else:
        driver = webdriver.Remote(command_executor="127.0.0.1:9515")
    with driver:
        yield driver


@pytest.fixture
def login_user(driver, client, live_server):
    def action(user, password='test'):
        user.set_password(password)
        user.save()
        client.login(username=user.username, password=password)
        cookie = client.cookies['sessionid']
        driver.get(live_server.url)
        driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    return action
