from django.contrib.auth import get_user_model
from human.models import Teacher, Student
from human.serializers import AccountSerializer, StudentSerializer, TeacherSerializer
from django.contrib.auth.hashers import check_password

import pytest

User = get_user_model()


@pytest.mark.django_db
def test_account_serializer_create():
    serializer = AccountSerializer(
        data={
            "email": "test@example.com",
            "password": "testpassword",
            "user_type": "student",
            "name": "John",
            "last_name": "Doe",
            "surname": "Smith",
        }
    )
    assert serializer.is_valid()
    account = serializer.save()
    assert account.email == "test@example.com"
    assert account.user_type == "student"
    assert account.name == "John"
    assert account.last_name == "Doe"
    assert account.surname == "Smith"


@pytest.mark.django_db
def test_account_serializer_create_invalid():
    serializer = AccountSerializer(
        data={
            "email": "",
            "password": "testpassword",
            "user_type": "student",
            "name": "John",
            "last_name": "Doe",
            "surname": "Smith",
        }
    )
    assert not serializer.is_valid()
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_account_serializer_create_password_write_only():
    serializer = AccountSerializer(
        data={
            "email": "test@example.com",
            "password": "testpassword",
            "user_type": "student",
            "name": "John",
            "last_name": "Doe",
            "surname": "Smith",
        }
    )
    assert serializer.is_valid()
    assert "password" not in serializer.data


@pytest.mark.django_db
def test_teacher_serializer_create():
    serializer = TeacherSerializer()
    data = {
        "email": "teacher@example.com",
        "password": "password",
        "name": "John",
        "last_name": "Doe",
        "surname": "Smith",
    }
    teacher = serializer.create(validated_data=data)
    assert isinstance(teacher, Teacher)
    assert teacher.email == "teacher@example.com"
    assert teacher.name == "John"
    assert teacher.last_name == "Doe"
    assert teacher.surname == "Smith"
    assert teacher.user_type == "teacher"
    assert check_password("password", teacher.password)


@pytest.mark.django_db
def test_teacher_serializer_update():
    teacher = Teacher.objects.create(
        email="teacher@example.com",
        password="password",
        name="John",
        last_name="Doe",
        surname="Smith",
    )

    serializer = TeacherSerializer(instance=teacher)
    data = {
        "email": "updated_teacher@example.com",
        "name": "Updated",
        "last_name": "Teacher",
        "surname": "Test",
    }

    updated_teacher = serializer.update(instance=teacher, validated_data=data)
    assert updated_teacher.email == "updated_teacher@example.com"
    assert updated_teacher.name == "Updated"
    assert updated_teacher.last_name == "Teacher"
    assert updated_teacher.surname == "Test"


@pytest.mark.django_db
def test_student_serializer_create():
    serializer = StudentSerializer()
    data = {
        "email": "student@example.com",
        "password": "password",
        "name": "John",
        "last_name": "Doe",
        "surname": "Smith",
    }
    student = serializer.create(validated_data=data)
    assert isinstance(student, Student)
    assert student.email == "student@example.com"
    assert student.name == "John"
    assert student.last_name == "Doe"
    assert student.surname == "Smith"
    assert student.user_type == "student"
    assert check_password("password", student.password)


@pytest.mark.django_db
def test_student_serializer_update():
    student = Student.objects.create(
        email="student@example.com",
        password="password",
        name="John",
        last_name="Doe",
        surname="Smith",
    )

    serializer = StudentSerializer(instance=student)
    data = {
        "email": "updated_student@example.com",
        "name": "Updated",
        "last_name": "Student",
        "surname": "Test",
    }

    updated_student = serializer.update(instance=student, validated_data=data)
    assert updated_student.email == "updated_student@example.com"
    assert updated_student.name == "Updated"
    assert updated_student.last_name == "Student"
    assert updated_student.surname == "Test"
