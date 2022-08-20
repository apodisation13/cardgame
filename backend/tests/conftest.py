import pytest
from django.contrib.auth.hashers import make_password

from apps.core.management.commands.core import Command


@pytest.fixture
def test_password():
    return 'VEry-1-strong-test-passWorD'


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


@pytest.fixture
def load_database():
    core = Command()
    core.handle()
