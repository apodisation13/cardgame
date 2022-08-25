import pytest
from django.contrib.auth.hashers import make_password

from apps.core.management.commands.cards import Command as Cards
from apps.core.management.commands.core import Command as Core
from apps.core.management.commands.enemies import Command as Enemies
from django.core.management import call_command
from apps.accounts.models import CustomUser
from model_bakery import baker

import os


@pytest.fixture
def test_password():
    return 'VEry-1-strong-test-passWorD'


# Фикстура создания админа (вызывается КАЖДЫЙ раз, когда в тесте стоит в аргументах)
@pytest.fixture
def create_admin(db, django_user_model, test_password):
    def make_admin(**kwargs):
        print('ПАРОЛЬ', test_password, make_password(test_password))
        kwargs['password'] = make_password(test_password)
        if 'username' not in kwargs:
            kwargs['username'] = 'Some UserName'
            kwargs['email'] = 'some_test_email@mail.ru'
        admin_user = django_user_model.objects.create_superuser(is_staff=True, is_superuser=True, **kwargs)
        return admin_user
    return make_admin


# Вызов management команд: python manage.py core, python manage.py cards, python manage.py enemies
# благодаря тегу session выполняется только 1 раз перед началом тестов
# TODO: есть более красивый способ вызвать эти команды
@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    print(os.getcwd())
    with django_db_blocker.unblock():
        call_command('core')
        call_command('cards')
        call_command('enemies')


@pytest.fixture
def create_user():
    def user_factory(*args, **kwargs):
        return baker.make(CustomUser, *args, **kwargs)
    return user_factory
