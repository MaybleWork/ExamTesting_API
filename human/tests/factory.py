import factory
from human.models import Group, Account, Teacher, Subject
from django.contrib.auth.hashers import make_password
from factory.faker import Faker
from factory.django import DjangoModelFactory


# Фабрика для моделі Group
class GroupFactory(DjangoModelFactory):
    name = Faker("word")

    class Meta:
        model = Group


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = make_password("password")
    user_type = "student"
    name = "John"
    last_name = "Doe"
    surname = "Smith"
    is_active = True
    is_staff = False


class TeacherFactory(AccountFactory):
    class Meta:
        model = Teacher

    user_type = "teacher"


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    title = factory.Sequence(lambda n: f"Subject {n}")
    group = factory.SubFactory(GroupFactory)
    teacher = factory.SubFactory(TeacherFactory)
