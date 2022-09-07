import pytest
from django.conf import settings
from django.core.management import call_command
from model_bakery import baker
from rest_framework.test import APIClient

from apps.accounts.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return 'VEry-1-strong-test-passWorD'


# Фикстура создания админа (вызывается КАЖДЫЙ раз, когда в тесте стоит в аргументах)
@pytest.fixture
def create_admin(db, django_user_model, test_password):
    def make_admin(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = 'Some UserName'
            kwargs['email'] = 'some_test_email@mail.ru'
        admin_user = django_user_model.objects.create_superuser(is_staff=True, is_superuser=True, **kwargs)
        return admin_user
    return make_admin


# Вызов management команд: python manage.py core, python manage.py cards, python manage.py enemies
# благодаря тегу session выполняется только 1 раз перед началом тестов
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('core', path=f'{settings.BASE_DIR}')
        call_command('cards', path=f'{settings.BASE_DIR}')
        call_command('enemies', path=f'{settings.BASE_DIR}')


@pytest.fixture
def create_user():
    def user_factory(*args, **kwargs):
        return baker.make(CustomUser, *args, **kwargs)
    return user_factory
