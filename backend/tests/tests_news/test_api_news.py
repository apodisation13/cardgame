import pytest
from apps.news.models import News
from model_bakery import baker


@pytest.fixture
def create_news():
    def news_factory(*args, **kwargs):
        return baker.make(News, *args, **kwargs)
    return news_factory


@pytest.mark.parametrize(
    'user', [(None), (True)]
)
@pytest.mark.django_db
def test_get_news(user, create_user, create_news, api_client):
    news = create_news(_quantity=10)
    if user:
        test_user = create_user()
        api_client.force_authenticate(test_user)
    response = api_client.get('/api/v1/news/')
    assert response.status_code == 200
    assert len(response.data) == len(news)


@pytest.mark.parametrize(
    'is_admin, resp_status_code', [(True, 201), (False, 403)]
)
@pytest.mark.django_db
def test_post_news(
        create_admin, create_user, is_admin, resp_status_code, api_client):
    news = {'title': 'test', 'description': 'test'}
    if is_admin:
        test_user = create_admin()
    else:
        test_user = create_user()
    api_client.force_authenticate(test_user)
    response = api_client.post('/api/v1/news/', data=news, format='json')
    data_news_title = response.data.get('title')
    assert response.status_code == resp_status_code
    if data_news_title:
        assert data_news_title == news['title']
