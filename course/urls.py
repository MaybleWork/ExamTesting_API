from django.urls import path
from course.views import (
    TestCreateView,
    TestUpdateView,
    TestGetView,
    TestSubjectListView,
    TestVisibilityCheckView,
    QuestionCreateView,
    QuestionListView,
    AnswerCreateView,
    AnswerGeteView,
    AnswerQuestionGeteView,
    AnswerListView,
    ResultCreateView,
    ResultGetView,
    ResultListView,
    ResultStudentListView,
    ResultUpdateView,
    ResultNumberOfAttempsView,
)

app_name = "course"

urlpatterns = [
    path("test/create/", TestCreateView.as_view()),
    path("test/update/<str:title>", TestUpdateView.as_view()),
    path("test/get/<str:title>/", TestGetView.as_view()),
    path("test/subject/list/<str:subject>", TestSubjectListView.as_view()),
    path("test/visiblelist/<str:subject>", TestVisibilityCheckView.as_view()),
    path("question/create/", QuestionCreateView.as_view()),
    path("question/list/<str:title>", QuestionListView.as_view()),
    path("answer/create/", AnswerCreateView.as_view()),
    path("answer/get/<str:text>", AnswerGeteView.as_view()),
    path("answer/question/get/<str:question>", AnswerQuestionGeteView.as_view()),
    path("answer/list/<str:text>", AnswerListView.as_view()),
    path("result/create/", ResultCreateView.as_view()),
    path("result/get/<str:name>", ResultGetView.as_view()),
    path("result/teacherlist/<str:title>", ResultListView.as_view()),
    path("result/studentlist/<int:fk>", ResultStudentListView.as_view()),
    path("result/update/<str:name>", ResultUpdateView.as_view()),
    path(
        "result/decriseattemptnumber/<str:name>/<str:title>",
        ResultNumberOfAttempsView.as_view(),
    ),
]
