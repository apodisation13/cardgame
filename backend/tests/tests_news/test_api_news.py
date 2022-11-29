import pytest
from model_bakery import baker
from rest_framework import status

from apps.news.models import News


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


@pytest.mark.django_db
def test_other_news_methods(create_admin, api_client, create_news):
    data = {'title': 'test', 'description': 'test'}
    test_user = create_admin()
    api_client.force_authenticate(test_user)

    response = api_client.post('/api/v1/news/', data)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, 'создание новости'

    test_news = create_news()
    url = f"/api/v1/news/{test_news.id}/"

    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, 'редактирование новости'

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, 'удаление новости'
