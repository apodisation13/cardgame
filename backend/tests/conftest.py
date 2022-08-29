import pytest
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management import call_command


@pytest.fixture
def test_password():
    return 'VEry-1-strong-test-passWorD'


# Фикстура создания админа (вызывается КАЖДЫЙ раз, когда в тесте стоит в аргументах)
@pytest.fixture
def create_admin(db, django_user_model, test_password):
    def make_admin(**kwargs):
        kwargs['password'] = make_password(test_password)
        if 'username' not in kwargs:
            kwargs['username'] = 'Some UserName'
            kwargs['email'] = 'some_test_email@mail.ru'
        admin_user = django_user_model.objects.create_superuser(is_staff=True, is_superuser=True, **kwargs)
        return admin_user
    return make_admin


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = make_password(test_password)
        if 'username' not in kwargs:
            kwargs['username'] = 'Some UserName_1'
            kwargs['email'] = 'some_test_email_1@mail.ru'
        user = django_user_model.objects.create_user(is_staff=True, **kwargs)
        return user
    return make_user


# Вызов management команд: python manage.py core, python manage.py cards, python manage.py enemies
# благодаря тегу session выполняется только 1 раз перед началом тестов
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('core', path=f'{settings.BASE_DIR}')
        call_command('cards', path=f'{settings.BASE_DIR}')
        call_command('enemies', path=f'{settings.BASE_DIR}')
