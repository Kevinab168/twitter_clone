from pytest_factoryboy import register
from make_posts.tests.factories import UserFactory, PostFactory
from make_posts.models import Post, Comment


register(UserFactory)
register(PostFactory)


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert "welcome" in driver.page_source.lower()
    assert driver.find_element_by_css_selector('[data-test="log_in"]')


def test_login_page(driver, live_server, user_factory):
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


def test_make_post(driver, login_user, live_server, user_factory):
    user = user_factory.create()
    login_user(user)
    driver.get(live_server.url + f'/users/{user.pk}')
    post_text = driver.find_element_by_css_selector('[data-test="post"]')
    post_text.send_keys('Sample Post')
    post_it = driver.find_element_by_css_selector('[data-test="make-post"]')
    post_it.click()
    assert 'Sample Post' in driver.page_source
    assert driver.current_url == live_server.url + f'/users/{user.pk}'
    last_post = Post.objects.all().last()
    assert last_post.user == user


def test_make_comment(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(10):
        post_factory.create(user=user)
    driver.get(live_server + f'/users/{user.pk}')
    post_1 = driver.find_element_by_css_selector('[data-test="post-info"]')
    post_1.click()
    text_field = driver.find_element_by_css_selector('[data-test="text-input"]')
    text_field.send_keys('Sample1')
    submit_comment = driver.find_element_by_css_selector('[data-test="create-comment"]')
    submit_comment.click()
    assert 'Sample1' in driver.page_source
    recent_comment = Comment.objects.all().last()
    post_of_comment = Post.objects.get(pk=1)
    assert recent_comment.user == user
    assert recent_comment.post == post_of_comment
