from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Tag, Question, Answer, UserScore, Vote, Comment


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


class CommentSerializer(serializers.ModelSerializer):
    comment_user = UserSerializer(allow_null=True)
    question = QustionSerializer()
    answer = AnswerSerializer(allow_null=True)

    class Meta:
        model = Comment


class VoteSerializer(serializers.ModelSerializer):
    voter_user = UserSerializer()

    class Meta:
        model = Vote


class UserScoreSerializer(serializers.ModelSerializer):
    voter_user = UserSerializer()

    class Meta:
        model = UserScore
