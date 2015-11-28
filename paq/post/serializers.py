from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Tag, Question, Answer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer


class QustionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    answers = AnswerSerializer(many=True, required=False, allow_null=True)
    user = UserSerializer()

    class Meta:
        model = Question
