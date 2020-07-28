from pytest_factoryboy import register
from make_posts.tests.factories import UserFactory, PostFactory, CommentFactory, FollowFactory, ImageFactory
from make_posts.models import Post, Comment, Follow, User

register(UserFactory)
register(PostFactory)
register(CommentFactory)
register(FollowFactory)
register(ImageFactory)


def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    assert "welcome" in driver.page_source.lower()
    assert driver.find_element_by_css_selector('[data-test="login-link"]')


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
    assert driver.find_element_by_css_selector('[data-test="follower-count"]')
    assert driver.find_element_by_css_selector('[data-test="following-count"]')
    assert driver.find_element_by_css_selector('[data-test="make-post"]')


def test_make_post(driver, login_user, live_server, user_factory):
    user = user_factory.create()
    login_user(user)
    driver.get(live_server.url + f'/users/{user.pk}')
    post_text = driver.find_element_by_css_selector('[data-test="post"]')
    post_text.send_keys('Sample Post')
    post_it = driver.find_element_by_css_selector('[data-test="make-post"]')
    post_it.click()
    assert 'Sample Post' in driver.find_element_by_css_selector('[data-test="created-post"]').text
    last_post = Post.objects.all().last()
    assert last_post.user == user


def test_make_comment(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(10):
        post_factory.create(user=user)
    post = Post.objects.all().last()
    driver.get(live_server + f'/posts/{post.pk}')
    comment_field = driver.find_element_by_css_selector('[data-test="comment-text"]')
    comment_field.send_keys('Sample1')
    submit_comment = driver.find_element_by_css_selector('[data-test="create-comment"]')
    submit_comment.click()
    assert 'Sample1' in driver.find_element_by_css_selector('[data-test="user-comment"]').text
    recent_comment = Comment.objects.all().last()
    assert recent_comment.user == user
    assert recent_comment.post == post


def test_follow_change(driver, live_server, login_user, user_factory, post_factory):
    user = user_factory.create()
    user2 = user_factory.create()
    login_user(user2)
    driver.get(live_server.url + f'/users/{user.pk}')
    follow_button = driver.find_element_by_css_selector('[data-test="follow"]')
    follow_button.click()
    follower_count = driver.find_element_by_css_selector('[data-test="follower-count"]').text
    assert '1' in follower_count
    following_count = driver.find_element_by_css_selector('[data-test="following-count"]').text
    assert '0' in following_count
    follow = Follow.objects.all().last()
    assert follow.follower == user2
    assert follow.following == user


def test_see_followers(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(following=user)
    driver.get(live_server.url + f'/users/{user.pk}/followers')
    followers_list = driver.find_elements_by_css_selector('[data-test="followers"]')
    followers_count = 20
    assert len(followers_list) == followers_count
    assert 'Followers' in driver.find_element_by_css_selector('[data-test="follower-page-heading"]').text
    last_follower = Follow.objects.all().last()
    assert last_follower.following == user


def test_go_to_follower_homepage(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(following=user)
    driver.get(live_server.url + f'/users/{user.pk}/followers')
    follower_homepage = driver.find_elements_by_css_selector('[data-test="follower-homepage"]')[-1]
    follower_homepage.click()
    last_follower = Follow.objects.all().last()
    assert last_follower.follower.username in driver.find_element_by_css_selector('[data-test="user"]').text
    assert driver.find_element_by_css_selector('[data-test="follower-count"]')
    assert driver.find_element_by_css_selector('[data-test="following-count"]')


def test_see_following(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(follower=user)
    driver.get(live_server.url + f'/users/{user.pk}/following')
    following_list = driver.find_elements_by_css_selector('[data-test="following"]')
    following_count = 20
    assert len(following_list) == following_count
    assert 'Following' in driver.find_element_by_css_selector('[data-test="following-page-heading"]').text
    last_user_followed = Follow.objects.all().last()
    assert last_user_followed.follower == user


def test_go_to_following_homepage(driver, live_server, login_user, user_factory, follow_factory):
    user = user_factory.create()
    login_user(user)
    for _ in range(20):
        follow_factory.create(follower=user)
    driver.get(live_server.url + f'/users/{user.pk}/following')
    following_homepage = driver.find_elements_by_css_selector('[data-test="following-homepage"]')[-1]
    following_homepage.click()
    last_user_followed = Follow.objects.all().last()
    assert last_user_followed.following.username in driver.find_element_by_css_selector('[data-test="user"]').text
    assert driver.find_element_by_css_selector('[data-test="follower-count"]')
    assert driver.find_element_by_css_selector('[data-test="following-count"]')


def test_follow_user_one_time(driver, live_server, login_user, user_factory, follow_factory):
    user1 = user_factory.create()
    user2 = user_factory.create()
    follow_factory.create(follower=user2, following=user1)
    login_user(user2)
    driver.get(live_server.url + f'/users/{user1.pk}')
    follow_button = driver.find_element_by_css_selector('[data-test="follow"]')
    follow_button.click()
    follower_count = driver.find_element_by_css_selector('[data-test="follower-count"]').text
    assert '1' in follower_count
    following_count = driver.find_element_by_css_selector('[data-test="following-count"]').text
    assert '0' in following_count


def test_followed_user_posts_on_homepage(driver, live_server, login_user, user_factory, follow_factory, post_factory):
    user1 = user_factory.create()
    POSTS_COUNT = 20
    for _ in range(POSTS_COUNT):
        followed_user = user_factory.create()
        follow_factory.create(follower=user1, following=followed_user)
        post_factory.create(user=followed_user)
    login_user(user1)
    driver.get(live_server.url + '/home')
    followed_user_posts = driver.find_elements_by_css_selector('[data-test="followed_user_posts"]')
    assert len(followed_user_posts) == POSTS_COUNT
    last_post = followed_user_posts[-1]
    last_user = User.objects.all().last()
    last_post_text = Post.objects.all().last().content
    assert last_user.username in last_post.find_element_by_css_selector('[data-test="post_author"]').text
    assert last_post_text in last_post.find_element_by_css_selector('[data-test="post_text"]').text


def test_date_time_on_posts(driver, live_server, login_user, user_factory, post_factory, convert_datetime):
    user = user_factory.create()
    post_factory.create(user=user)
    login_user(user)
    driver.get(live_server.url + f'/users/{user.pk}')
    post_creation_date = driver.find_element_by_css_selector('[data-test="created_date"]')
    post_updated_date = driver.find_element_by_css_selector('[data-test="updated_date"]')
    post = Post.objects.all().last()
    assert convert_datetime(post.created_at) in post_creation_date.text
    assert convert_datetime(post.updated_at) in post_updated_date.text


def test_date_time_on_comments(
     driver,
     live_server,
     login_user,
     user_factory,
     post_factory,
     comment_factory,
     convert_datetime
):
    user = user_factory.create()
    post = post_factory.create(user=user)
    comment = comment_factory.create(user=user, post=post)
    login_user(user)
    driver.get(live_server.url + f'/posts/{post.pk}')
    comment_creation_date = driver.find_element_by_css_selector('[data-test="comment_creation_date"]')
    comment_updated_date = driver.find_element_by_css_selector('[data-test="comment_updated_date"]')
    comment = Comment.objects.all().last()
    assert convert_datetime(comment.created_at) in comment_creation_date.text
    assert convert_datetime(comment.updated_at) in comment_updated_date.text


def test_image_display_on_post(driver, live_server, post_factory, login_user, image_factory):
    post = post_factory.create()
    for _ in range(3):
        image_factory.create(post=post)
    IMAGE_COUNT = 3
    driver.get(live_server.url + f'/posts/{post.pk}')
    images_on_post = driver.find_elements_by_css_selector('[data-test="post_img_preview"]')
    assert len(images_on_post) == IMAGE_COUNT
