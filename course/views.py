from rest_framework import generics
from course.models import Result, Question, Answer, Test
from course.serializers import (
    TestSerializer,
    TestListSerializer,
    QuestionSerializer,
    AnswerCreateSerializer,
    ResultCreationSerializer,
    ResultListSerializer,
    ResultUpdateSerializer,
    ResultNumberAttempsSerializer,
    ResultSerializer,
)
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
import random

# Create your views here.


class QuestionPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"


class TestCreateView(generics.CreateAPIView):
    """Test creation"""

    serializer_class = TestSerializer
    queryset = Test.objects.all()


class TestSubjectListView(generics.ListAPIView):
    """List test by subject title"""

    serializer_class = TestListSerializer
    queryset = Test.objects.all()
    lookup_field = "subject"

    def get_queryset(self):
        subject = self.kwargs["subject"]

        qs = Test.objects.filter(subject=subject)
        return qs


class TestGetView(generics.RetrieveAPIView):
    """Get test by title"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer

    lookup_field = "title"

    def get(self, request, *args, **kwargs):
        self.lookup_url_kwarg = self.lookup_field
        return self.retrieve(request, *args, **kwargs)


class TestUpdateView(generics.UpdateAPIView):
    """Test update"""

    serializer_class = TestSerializer
    queryset = Test.objects.all()

    lookup_field = "title"


class TestVisibilityCheckView(generics.ListAPIView):
    """List of visible test"""

    serializer_class = TestListSerializer

    def get_queryset(self):
        return Test.objects.get_visible_list(self.kwargs["subject"])


class QuestionCreateView(generics.CreateAPIView):
    """Question creation"""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionListView(generics.ListAPIView):
    """List of all question for defined test"""

    serializer_class = QuestionSerializer
    pagination_class = QuestionPagination

    def get_queryset(self):
        title = self.kwargs["title"]
        try:
            test = Test.objects.get(title=title)
        except ObjectDoesNotExist:
            return Question.objects.none()

        qs = Question.objects.filter(test=title)

        if test.question_randomizer:
            count = min(test.count_of_question, qs.count())
            qs = random.sample(list(qs), count)
        else:
            qs = qs[: test.count_of_question]

        return qs


class AnswerCreateView(generics.CreateAPIView):
    """Answer creation"""

    serializer_class = AnswerCreateSerializer
    queryset = Answer.objects.all()


class AnswerGeteView(generics.RetrieveAPIView):
    """Get answer"""

    serializer_class = AnswerCreateSerializer
    queryset = Answer.objects.all()
    lookup_field = "text"


class AnswerQuestionGeteView(generics.ListAPIView):
    """Get answer by question"""

    serializer_class = AnswerCreateSerializer
    queryset = Answer.objects.all()
    lookup_field = "question"

    def get_queryset(self):
        question = self.kwargs["question"]

        qs = Answer.objects.filter(question=question)
        return qs


class AnswerListView(generics.ListAPIView):
    """Answer creation"""

    serializer_class = AnswerCreateSerializer

    def get_queryset(self):
        text = self.kwargs["text"]

        qs = Answer.objects.filter(question=text)
        return qs


class ResultCreateView(generics.CreateAPIView):
    """Result creation"""

    serializer_class = ResultCreationSerializer
    queryset = Result.objects.all()


class ResultListView(generics.ListAPIView):
    """List of results for defined test"""

    serializer_class = ResultListSerializer
    lookup_field = "title"

    def get_queryset(self):
        title = self.kwargs["title"]

        qs = Result.objects.filter(test=title)
        return qs


class ResultStudentListView(generics.ListAPIView):
    """List of results for defined student"""

    serializer_class = ResultListSerializer

    def get_queryset(self):
        fk = self.kwargs["fk"]

        qs = Result.objects.filter(student=fk)
        return qs


class ResultUpdateView(generics.UpdateAPIView):
    """Update resut"""

    serializer_class = ResultUpdateSerializer
    lookup_field = "name"

    def get_queryset(self):
        return Result.objects.filter(name=self.kwargs["name"])


class ResultGetView(generics.RetrieveAPIView):
    """Get result"""

    serializer_class = ResultSerializer
    queryset = Result.objects.all()

    lookup_field = "name"

    def get(self, request, *args, **kwargs):
        self.lookup_url_kwarg = self.lookup_field
        return self.retrieve(request, *args, **kwargs)


class ResultNumberOfAttempsView(generics.UpdateAPIView):
    """Decrise numbers of attemps"""

    serializer_class = ResultNumberAttempsSerializer
    lookup_field = "name"

    def get_queryset(self):
        return (
            Result.objects.filter(name=self.kwargs["name"])
            .filter(test=self.kwargs["title"])
            .filter(number_of_attemps__gt=0)
        )

    def patch(self, request, *args, **kwargs):
        result = self.get_object()
        result.number_of_attemps -= 1
        result.save()

        serializer = self.get_serializer(result, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
