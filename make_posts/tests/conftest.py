import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.yield_fixture(scope='session')
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
