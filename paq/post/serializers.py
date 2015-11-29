from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Tag, Question, Answer, UserScore, Vote, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title',)


class CommentSerializer(serializers.ModelSerializer):
    comment_user = UserSerializer(allow_null=True)

    class Meta:
        model = Comment


class AnswerSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    reply_user = UserSerializer()

    class Meta:
        model = Answer


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote


class QustionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    answers = AnswerSerializer(many=True, required=False, allow_null=True)
    user = UserSerializer()
    comment = CommentSerializer(many=True)

    class Meta:
        model = Question


class UserScoreSerializer(serializers.ModelSerializer):
    voter_user = UserSerializer()

    class Meta:
        model = UserScore
