# Generated by Django 4.2.2 on 2023-06-24 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=100, unique=True, verbose_name="Email"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("student", "Student"), ("teacher", "Teacher")],
                        default="student",
                        max_length=20,
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=60, verbose_name="Person first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=60, verbose_name="Person last name"),
                ),
                (
                    "surname",
                    models.CharField(max_length=60, verbose_name="Person surname name"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="custom_groups_set", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_user_permissions_set",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=10, unique=True, verbose_name="Group name"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Verification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=30, unique=True, verbose_name="Verification code"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "account_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("human.account",),
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=100, unique=True, verbose_name="Title"),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="human.group",
                        to_field="name",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="human.teacher"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "account_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="human.group",
                        to_field="name",
                        verbose_name="Group",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("human.account",),
        ),
        migrations.AddField(
            model_name="group",
            name="teacher",
            field=models.ManyToManyField(through="human.Subject", to="human.teacher"),
        ),
    ]
