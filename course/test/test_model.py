import datetime
import pytest
from django.utils import timezone
from course.models import Test
from human.models import Subject


from human.tests.factory import GroupFactory, TeacherFactory


@pytest.mark.django_db
def test_test_manager_get_visible_list():
    teacher = TeacherFactory()

    group = GroupFactory()

    subject = Subject.objects.create(
        title="Math",
        group=group,
        teacher=teacher,
    )
    now = timezone.now()

    # Creating visible tests
    visible_test1 = Test.objects.create(
        title="Test 1",
        max_mark=100,
        visibility=True,
        test_duration=datetime.timedelta(minutes=60),
        start_date=now,
        end_date=now + timezone.timedelta(hours=1),
        number_of_attemps=1,
        count_of_question=10,
        subject=subject,
    )
    visible_test2 = Test.objects.create(
        title="Test 2",
        max_mark=100,
        visibility=True,
        test_duration=datetime.timedelta(minutes=60),
        start_date=now,
        end_date=now + timezone.timedelta(hours=1),
        number_of_attemps=2,
        count_of_question=10,
        subject=subject,
    )

    # Creating invisible tests
    invisible_test1 = Test.objects.create(
        title="Test 3",
        max_mark=100,
        visibility=False,
        test_duration=datetime.timedelta(minutes=60),
        start_date=now,
        end_date=now + timezone.timedelta(hours=1),
        number_of_attemps=1,
        count_of_question=10,
        subject=subject,
    )
    invisible_test2 = Test.objects.create(
        title="Test 4",
        max_mark=100,
        visibility=True,
        test_duration=datetime.timedelta(minutes=60),
        start_date=now + timezone.timedelta(hours=2),
        end_date=now + timezone.timedelta(hours=3),
        number_of_attemps=1,
        count_of_question=10,
        subject=subject,
    )
    invisible_test3 = Test.objects.create(
        title="Test 5",
        max_mark=100,
        visibility=True,
        test_duration=datetime.timedelta(minutes=60),
        start_date=now - timezone.timedelta(hours=2),
        end_date=now - timezone.timedelta(hours=1),
        number_of_attemps=1,
        count_of_question=10,
        subject=subject,
    )
    invisible_test4 = Test.objects.create(
        title="Test 6",
        max_mark=100,
        visibility=True,
        test_duration=datetime.timedelta(minutes=60),
        start_date=now,
        end_date=now + timezone.timedelta(hours=1),
        number_of_attemps=0,
        count_of_question=10,
        subject=subject,
    )

    visible_tests = Test.objects.get_visible_list(subject)
    assert visible_tests.count() == 2
    assert visible_test1 in visible_tests
    assert visible_test2 in visible_tests
    assert invisible_test1 not in visible_tests
    assert invisible_test2 not in visible_tests
    assert invisible_test3 not in visible_tests
    assert invisible_test4 not in visible_tests
