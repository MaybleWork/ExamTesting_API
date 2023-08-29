from django.db import models
from human.models import Student, Subject
from django.utils import timezone


# Create your models here.


class TestManager(models.Manager):
    def get_visible_list(self, subject):
        now = timezone.now()
        return (
            self.get_queryset()
            .filter(subject=subject)
            .filter(visibility=True)
            .filter(start_date__lte=now)
            .filter(end_date__gte=now)
            .filter(number_of_attemps__gt=0)
        )


class Test(models.Model):
    title = models.CharField(verbose_name="Title", max_length=100, unique=True)

    max_mark = models.PositiveSmallIntegerField(verbose_name="Maximum mark")

    number_of_attemps = models.PositiveSmallIntegerField(
        verbose_name="Number of attemps", max_length=10, default=0
    )

    visibility = models.BooleanField(verbose_name="Visibility", default=True)

    automate_checking = models.BooleanField(
        verbose_name="Automate checking", default=False
    )

    question_randomizer = models.BooleanField(
        verbose_name="Question randomizer", default=True
    )

    backstep = models.BooleanField(verbose_name="Backstep", default=False)

    penalty = models.PositiveSmallIntegerField(
        verbose_name="Penalty for rearrangements", max_length=100, default=0
    )

    level = models.PositiveSmallIntegerField(
        verbose_name="Completion level", max_length=100, default=0
    )

    test_duration = models.DurationField(
        verbose_name="Test duration",
    )

    start_date = models.DateTimeField(
        verbose_name="Start date",
    )

    end_date = models.DateTimeField(
        verbose_name="End date",
    )

    count_of_question = models.PositiveSmallIntegerField(
        verbose_name="Count of question"
    )

    subject = models.ForeignKey(
        Subject, to_field="title", verbose_name="Subject", on_delete=models.CASCADE
    )

    objects = TestManager()


class Question(models.Model):
    text = models.CharField(
        verbose_name="Text", null=True, blank=True, unique=True, max_length=256
    )

    test = models.ForeignKey(
        Test, verbose_name="Test", to_field="title", on_delete=models.CASCADE
    )


class Answer(models.Model):
    text = models.CharField(
        verbose_name="Text", null=True, blank=True, max_length=265, unique=True
    )

    is_test = models.BooleanField(
        verbose_name="Test answer", null=True, blank=True, default=False
    )
    is_multitest = models.BooleanField(
        verbose_name="Multitest answer", null=True, blank=True, default=False
    )
    is_text = models.BooleanField(
        verbose_name="Text answer", null=True, blank=True, default=False
    )

    is_correct = models.BooleanField(
        verbose_name="Correct answer", null=True, blank=True, default=False
    )

    mark = models.PositiveSmallIntegerField(
        verbose_name="Mark", null=True, blank=True, default=0
    )

    question = models.ForeignKey(
        Question,
        verbose_name="Question",
        to_field="text",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class Result(models.Model):
    name = models.CharField(verbose_name="Result name", unique=True, max_length=256)

    list_answers = models.ManyToManyField(Answer)

    final_mark = models.PositiveSmallIntegerField(verbose_name="Final mark", default=0)

    number_of_attemps = models.PositiveSmallIntegerField(
        verbose_name="Number of attemps", default=1
    )

    student = models.ForeignKey(
        Student, verbose_name="Student", on_delete=models.CASCADE
    )

    test = models.ForeignKey(
        Test, to_field="title", verbose_name="Test", on_delete=models.CASCADE
    )
