import pytest


@pytest.mark.parametrize('user_is_admin', [True, False])
@pytest.mark.django_db
def test_unlock_levels(user_is_admin,
                       create_admin, create_user, api_client):
    if user_is_admin:
        test_user = create_admin()
    else:
        test_user = create_user()
    api_client.force_authenticate(test_user)
    user_levels_before = test_user.levels.count()
    body = {'related_levels': [18, 19, 20]}
    response = api_client.post(
        '/api/v1/levels/1/unlock_levels/',
        data=body,
        format='json'
    )
    assert response.status_code == 200
    assert test_user.levels.count() == \
           user_levels_before + len(body['related_levels'])
    assert response.json()[0] == {'id': 18, 'name': 'Уровень18'}


@pytest.mark.django_db
def test_unlock_levels_unauthenticated(api_client):
    body = {'related_levels': [18, 19, 20]}
    response = api_client.post('/api/v1/levels/1/unlock_levels/', data=body)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_open_levels_user(create_user, api_client):
    test_user = create_user()
    api_client.force_authenticate(test_user)
    body = {'user': test_user.id}
    response = api_client.delete(
        '/api/v1/levels/delete_open_levels/',
        data=body,
        format='json'
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_open_levels_admin(create_user, create_admin, api_client):
    test_user = create_user()
    user_levels = test_user.levels.count()
    test_admin = create_admin()
    api_client.force_authenticate(test_admin)
    body = {'user': test_user.id}
    response = api_client.delete(
        '/api/v1/levels/delete_open_levels/',
        data=body,
        format='json'
    )
    user_levels_after_del = test_user.levels.count()
    assert response.status_code == 200
    assert user_levels_after_del == 1
    assert response.data == f'{user_levels - 1} levels deleted'
