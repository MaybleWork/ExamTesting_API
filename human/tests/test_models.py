import pytest
from human.models import Account
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_account(sample_account):
    assert sample_account.email is not None
    assert sample_account.user_type == "student"
    # Перевірте інші поля


@pytest.mark.django_db
def test_get_account_by_email(sample_account):
    fetched_account = Account.objects.get(email=sample_account.email)
    assert fetched_account == sample_account


@pytest.mark.django_db
def test_create_user():
    # Arrange
    manager = get_user_model().objects
    email = "test@example.com"
    password = "password"
    user_type = "student"

    # Act
    user = manager.create_user(email=email, password=password, user_type=user_type)

    # Assert
    assert user.email == email
    assert user.check_password(password)
    assert user.user_type == user_type
    assert user.is_active
    assert user.is_staff


@pytest.mark.django_db
def test_create_superuser():
    # Arrange
    manager = get_user_model().objects
    email = "admin@example.com"
    password = "password"

    # Act
    superuser = manager.create_superuser(
        email=email, password=password, user_type="teacher"
    )

    # Assert
    assert superuser.email == email
    assert superuser.check_password(password)
    assert superuser.is_superuser
    assert superuser.is_staff


@pytest.mark.django_db
def test_create_user_with_no_email():
    # Arrange
    manager = get_user_model().objects
    password = "password"

    # Act & Assert
    with pytest.raises(ValueError) as e:
        manager.create_user(email="", password=password)
    assert str(e.value) == "The Email field must be set"


@pytest.mark.django_db
def test_create_superuser_with_no_staff():
    # Arrange
    manager = get_user_model().objects
    email = "admin@example.com"
    password = "password"

    # Act & Assert
    with pytest.raises(ValueError) as e:
        manager.create_superuser(email=email, password=password, is_staff=False)
    assert str(e.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_create_superuser_with_no_superuser():
    # Arrange
    manager = get_user_model().objects
    email = "admin@example.com"
    password = "password"

    # Act & Assert
    with pytest.raises(ValueError) as e:
        manager.create_superuser(email=email, password=password, is_superuser=False)
    assert str(e.value) == "Superuser must have is_superuser=True."
