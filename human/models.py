from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    Group,
    Permission,
    BaseUserManager,
    AbstractBaseUser,
)


# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    email = models.EmailField(verbose_name="Email", max_length=100, unique=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default="student"
    )
    name = models.CharField(verbose_name="Person first name", max_length=60)
    last_name = models.CharField(verbose_name="Person last name", max_length=60)
    surname = models.CharField(verbose_name="Person surname name", max_length=60)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    groups = models.ManyToManyField(Group, related_name="custom_groups_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True
    )


class Teacher(Account):
    pass


class Group(models.Model):
    name = models.CharField(verbose_name="Group name", max_length=10, unique=True)

    teacher = models.ManyToManyField(Teacher, through="Subject")


class Student(Account):
    group = models.ForeignKey(
        Group,
        verbose_name="Group",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        to_field="name",
    )


class Subject(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100, unique=True)

    group = models.ForeignKey(Group, to_field="name", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Verification(models.Model):
    code = models.CharField(
        verbose_name="Verification code", max_length=30, unique=True
    )
