from django.test import RequestFactory
import pytest
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

from human.models import Account, Student, Verification
from human.serializers import VerificationSerializer
from human.tests.factory import (
    AccountFactory,
    GroupFactory,
    TeacherFactory,
    SubjectFactory,
)
from human.views import LoginView, StudentGetView, VerifCodeCreationView


@pytest.mark.django_db
def test_create_verification_code():
    factory = APIRequestFactory()
    view = VerifCodeCreationView.as_view()
    url = "/api/verification/"  # Опціонально, замість цього використовуйте reverse()

    # Передайте дані для створення коду верифікації
    data = {"code": "123456"}

    # Створіть POST-запит до представлення
    request = factory.post(url, data, format="json")
    response = view(request)

    # Перевірте, що код верифікації був створений
    assert response.status_code == status.HTTP_201_CREATED
    assert Verification.objects.exists()

    # Перевірте, що серіалізатор повертає правильні дані
    serializer = VerificationSerializer(instance=Verification.objects.first())
    assert response.data == serializer.data


@pytest.mark.django_db
def test_login_view_successful_authentication():
    # Arrange
    factory = RequestFactory()
    request = factory.post(
        "/login/",
        {
            "email": "test@example.com",
            "password": "password123",
        },
    )
    view = LoginView.as_view()
    account = Account.objects.create_user(
        email="test@example.com",
        password="password123",
        user_type="student",  # Provide the user_type value
    )
    token = Token.objects.create(user=account)

    # Act
    response = view(request)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["email"] == "test@example.com"
    assert response.data["token"] == token.key


@pytest.mark.django_db
def test_login_view_invalid_credentials():
    # Arrange
    factory = RequestFactory()
    request = factory.post(
        "/login/",
        {
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    view = LoginView.as_view()
    Account.objects.create_user(
        email="test@example.com",
        password="password123",
        user_type="student",  # Provide the user_type value
    )

    # Act
    response = view(request)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid Credentials"


@pytest.mark.django_db
def test_student_get_view():
    # Arrange
    factory = RequestFactory()
    request = factory.get("/students/test@example.com/")
    view = StudentGetView.as_view()
    student = Student.objects.create(
        email="test@example.com",
        user_type="student",
        name="John",
        last_name="Doe",
        surname="Smith",
    )

    # Act
    response = view(request, email="test@example.com")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "test@example.com"
    assert response.data["user_type"] == "student"
    assert response.data["name"] == "John"
    assert response.data["last_name"] == "Doe"
    assert response.data["surname"] == "Smith"


@pytest.mark.django_db
def test_student_get_view_invalid_email():
    # Arrange
    factory = RequestFactory()
    request = factory.get("/students/invalid@example.com/")
    view = StudentGetView.as_view()

    # Act
    response = view(request, email="invalid@example.com")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.data


@pytest.mark.django_db
def test_subject_list_view(api_client):
    # Створення вчителя
    teacher = TeacherFactory()
    teacher_id = teacher.id

    # Створення групи
    group = GroupFactory()

    # Створення предметів та призначення їм вчителя та групу
    subject1 = SubjectFactory(title="math", teacher=teacher, group=group)
    subject2 = SubjectFactory(title="math1", teacher=teacher, group=group)

    # Отримання списку предметів за ідентифікатором вчителя
    url = reverse("human:subject-teacher-list", args=[teacher_id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    # Перевірка даних предметів
    expected_data = [
        {"title": subject1.title},
        {"title": subject2.title},
    ]
    assert response.data == expected_data


@pytest.mark.django_db
def test_subject_student_list_view(api_client):
    # Створення вчителя
    teacher = TeacherFactory()

    # Створення групи
    group = GroupFactory()

    # Створення предметів та призначення їм вчителя та групу
    subject1 = SubjectFactory(title="math", group=group, teacher=teacher)
    subject2 = SubjectFactory(title="math1", group=group, teacher=teacher)

    name = group.name
    # Отримання списку предметів за ідентифікатором групи
    url = reverse("human:subject-student-list", args=[name])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    # Перевірка даних предметів
    expected_data = [
        {"title": subject1.title},
        {"title": subject2.title},
    ]
    assert response.data == expected_data


@pytest.mark.django_db
def test_subject_get_view(api_client):
    # Створення предмету
    subject = SubjectFactory()

    # Отримання предмету за назвою
    url = reverse("human:subject-get", args=[subject.title])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    # Перевірка даних предмету
    assert response.data["title"] == subject.title


# @pytest.mark.django_db
# def test_logout_view():
#     factory = APIRequestFactory()
#     view = LogoutView.as_view()
#     url = "/api/logout/"

#     user = AccountFactory()
#     token = Token.objects.create(user=user)

#     request = factory.post(url)
#     request.user = user
#     request.auth = token

#     response = view(request)

#     assert response.status_code == status.HTTP_200_OK
#     assert not Token.objects.filter(user=user).exists()
