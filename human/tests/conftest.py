import pytest
from django.test import Client
from human.tests.factory import AccountFactory
from rest_framework.test import APIClient
from human.tests.factory import TeacherFactory, GroupFactory


@pytest.fixture
def teacher_factory():
    return TeacherFactory()


@pytest.fixture
def group_factory():
    return GroupFactory()


@pytest.fixture()
def sample_account(db):
    return AccountFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def client():
    # Створення клієнта для виконання HTTP-запитів
    return Client()
