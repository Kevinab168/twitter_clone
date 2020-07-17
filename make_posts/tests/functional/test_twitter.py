from pytest_factoryboy import register
from make_posts.tests.factories import UserFactory

register(UserFactory)


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert "welcome" in driver.page_source.lower()
    assert driver.find_element_by_css_selector('[data-test="log_in"]')


def test_login_page(driver, live_server, user_factory):
    # user = user_factory.create(password='hello')
    user = user_factory.create()
    user.set_password('test')
    user.save()
    driver.get(live_server.url + '/login')
    username_input = driver.find_element_by_css_selector('[data-test="username"]')
    username_input.send_keys(user.username)
    password_input = driver.find_element_by_css_selector('[data-test="password"]')
    password_input.send_keys('test')
    log_in = driver.find_element_by_css_selector('[data-test="log-in"]')
    log_in.click()
    assert user.username in driver.find_element_by_css_selector('[data-test="user"]').text
    assert 'followers' in driver.page_source
    assert 'following' in driver.page_source
    assert 'posts' in driver.page_source
    assert driver.find_element_by_css_selector('[data-test="make-post"]')
