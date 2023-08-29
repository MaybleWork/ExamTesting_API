from rest_framework import serializers
from course.models import Test, Result, Question, Answer


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            "title",
            "max_mark",
            "number_of_attemps",
            "visibility",
            "automate_checking",
            "question_randomizer",
            "backstep",
            "penalty",
            "level",
            "test_duration",
            "start_date",
            "end_date",
            "count_of_question",
            "subject",
        )


class TestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ("title",)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "text", "test")


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "is_test",
            "is_multitest",
            "is_text",
            "text",
            "is_correct",
            "mark",
            "question",
        )


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = (
            "id",
            "text",
            "is_correct",
            "mark",
            "question",
        )


class ResultNumberAttempsSerializer(serializers.ModelSerializer):
    list_answers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Answer.objects.all()
    )

    class Meta:
        model = Result
        fields = ("list_answers",)


# class ResultUpdateSerializer():


class ResultUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            "list_answers",
            "name",
            "final_mark",
            "number_of_attemps",
            "student",
            "test",
        )


class ResultSerializer(serializers.ModelSerializer):
    list_answers = AnswerSerializer(many=True)

    class Meta:
        model = Result
        fields = (
            "list_answers",
            "name",
            "final_mark",
            "number_of_attemps",
            "student",
            "test",
        )

    def create(self, validated_data):
        list_answers_data = validated_data.pop("list_answers")
        result = Result.objects.create(**validated_data)
        for answer_data in list_answers_data:
            question_data = answer_data.pop("question")
            question = Question.objects.create(**question_data)
            answer = Answer.objects.create(question=question, **answer_data)
            result.list_answers.add(answer)
        return result

    def create(self, validated_data):
        list_answers_data = validated_data.pop("list_answers")
        result = Result.objects.create(**validated_data)
        for answer in list_answers_data:
            result.list_answers.add(answer)
        return result


class ResultCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            "name",
            "list_answers",
            "final_mark",
            "number_of_attemps",
            "student",
            "test",
        )


class ResultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("name", "final_mark", "student")
