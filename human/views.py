from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status, serializers

from human.models import Subject, Verification, Account, Student, Teacher, Group
from human.serializers import (
    VerificationSerializer,
    AccountGetSerializer,
    AccountUpdateSerializer,
    TeacherSerializer,
    AccountGetIdSerializer,
    StudentSerializer,
    StudentGetGroupSerializer,
    StudentListSerializer,
    GroupSerializer,
    AddStudentSerializer,
    SubjectListSerializer,
    SubjectSerializer,
)


# Create your views here.


class VerifCodeCreationView(generics.CreateAPIView):
    """Creation verification code"""

    serializer_class = VerificationSerializer
    queryset = Verification.objects.all()


class VerifCodeGetView(generics.RetrieveAPIView):
    """Creation verification code"""

    serializer_class = VerificationSerializer
    queryset = Verification.objects.all()
    lookup_field = "code"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response_serializer = AccountGetSerializer(user)
            return Response(
                {"user": response_serializer.data, "token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class AccountUpdateView(generics.UpdateAPIView):
    """Updating account data"""

    serializer_class = AccountUpdateSerializer
    queryset = Account.objects.all()
    lookup_field = "email"


class TeacherCreateView(generics.CreateAPIView):
    serializer_class = TeacherSerializer


class TeacherGetIdView(generics.RetrieveAPIView):
    """Get teacher pk"""

    serializer_class = AccountGetIdSerializer
    queryset = Teacher.objects.all()
    lookup_field = "email"


class TeacherUpdateDeleteAView(generics.RetrieveUpdateDestroyAPIView):
    """Editing teacher account"""

    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    lookup_field = "email"


class StudentCreateView(generics.CreateAPIView):
    """Student creation"""

    serializer_class = StudentSerializer


class StudentGetView(generics.RetrieveAPIView):
    """Student get"""

    serializer_class = StudentSerializer
    lookup_field = "email"

    def get_queryset(self):
        email = self.kwargs["email"]

        query_set = Student.objects.filter(email=email)
        return query_set


class StudentUpdataeDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Update student account"""

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    lookup_field = "email"


class StudentListView(generics.ListAPIView):
    """All student list"""

    serializer_class = StudentListSerializer
    queryset = Student.objects.all()


class StudentGetGroupView(generics.RetrieveAPIView):
    """get student group"""

    serializer_class = StudentGetGroupSerializer
    queryset = Student.objects.all()
    lookup_field = "email"


class AddStudentView(generics.RetrieveUpdateDestroyAPIView):
    """Add student to group"""

    serializer_class = AddStudentSerializer
    queryset = Student.objects.all()
    lookup_field = "email"


class GroupCreateView(generics.CreateAPIView):
    """Group creation"""

    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupListView(generics.ListAPIView):
    """Display list of group"""

    serializer_class = GroupSerializer
    queryset = Group.objects.all()


class GroupUpdateView(generics.UpdateAPIView):
    """Update group name"""

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = "name"


class SubjectCreateView(generics.CreateAPIView):
    """Subject creation"""

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class SubjectListView(generics.ListAPIView):
    """Subject list for teacher"""

    serializer_class = SubjectListSerializer

    def get_queryset(self):
        foreign_key = self.kwargs["fk"]

        query_set = Subject.objects.filter(teacher=foreign_key)
        return query_set


class SubjecStudentListView(generics.ListAPIView):
    """Subject list for group"""

    serializer_class = SubjectListSerializer

    def get_queryset(self):
        name = self.kwargs["name"]

        query_set = Subject.objects.filter(group=name)
        return query_set


class SubjecGetView(generics.RetrieveAPIView):
    """Get Subject"""

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    lookup_field = "title"

    def get(self, request, *args, **kwargs):
        self.lookup_url_kwarg = self.lookup_field
        return self.retrieve(request, *args, **kwargs)
