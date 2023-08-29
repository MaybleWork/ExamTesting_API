from rest_framework import serializers
from human.models import Verification, Account, Student, Subject, Teacher, Group


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = [
            "code",
        ]


class AccountGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "user_type",
            "name",
            "last_name",
            "surname",
        ]


class AccountGetIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
        ]


class AccountAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "password",
        ]


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "name",
            "last_name",
            "surname",
        ]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "password",
            "user_type",
            "name",
            "last_name",
            "surname",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user


class TeacherSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        model = Teacher

    def create(self, validated_data):
        validated_data["user_type"] = "teacher"
        password = validated_data.pop("password")
        teacher = Teacher.objects.create(**validated_data)
        teacher.set_password(password)
        teacher.save()
        return teacher


class StudentSerializer(AccountSerializer):
    class Meta(AccountSerializer.Meta):
        model = Student

    def create(self, validated_data):
        validated_data["user_type"] = "student"
        password = validated_data.pop("password")
        student = Student.objects.create(**validated_data)
        student.set_password(password)
        student.save()
        return student


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("title", "teacher", "group")


class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("title",)


class TeacherEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "username",
            "email",
            "password",
        ]


class StudentGetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "group",
        ]


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("email", "name", "last_name", "surname", "group")


class AddStudentSerializer(AccountSerializer):
    class Meta:
        model = Student
        fields = ("group",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class AddTeacherToGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("teacher",)


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ("code",)
