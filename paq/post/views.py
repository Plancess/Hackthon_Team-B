from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import F
from .serializers import TagSerializer, QustionSerializer, AnswerSerializer, \
    CommentSerializer, VoteSerializer
from .models import Tag, Question, Answer, Comment, Vote


# Create your views here.
class TagCreateView(ListCreateAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = TagSerializer(queryset, many=True)

        return Response(serializer.data)


class QuestionCreateView(ListCreateAPIView):
    serializer_class = QustionSerializer

    def list(self, request, *args, **kargs):
        # Note the use of `get_queryset()` instead of `self.queryset`\
        queryset = Question.objects.all()
        question_id = kargs.get('question_id')
        if question_id:
            Question.objects.filter(id=question_id).update(view_count=F('view_count') + 1)
            queryset = queryset.filter(id=question_id)

        serializer = QustionSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        tags = request.POST.getlist('tags[]')
        answers = request.POST.getlist('answers[]')
        if request.POST.get('type'):
            if int(request.POST.get('type')) == 0:
                post_type = Question.PRIVATE
            else:
                post_type = Question.PUBLIC

        post = Question(
            user=request.user, title=request.POST.get('title'),
            description=request.POST.get('description'), type=post_type)
        post.save()
        for tag in tags:
            try:
                tag = Tag.objects.get(id=tag)
                post.tags.add(tag)
            except Tag.DoesNotExist as e:
                pass

        for ans in answers:
            try:
                ans = Answer.objects.get(id=ans)
                post.tags.add(ans)
            except Answer.DoesNotExist as e:
                pass
        post.save()

        return Response(QustionSerializer(post).data)


class AnswerCreateView(ListCreateAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AnswerSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        try:
            ans = Answer(
                reply_user=request.user, description=request.POST.get('description'))

            ans.save()
            que_obj = Question.objects.get(id=request.POST.get('q_id'))
            que_obj.answers.add(ans)
            que_obj.save()
        except Exception as e:
            raise NotFound(str(e))

        return Response(AnswerSerializer(ans).data)


class CommentCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        comment_obj = Comment(
            text=request.POST['text'], comment_user=request.user)
        comment_obj.save()
        if request.POST.get('question'):
            que_obj = Question.objects.get(id=request.POST['question'])
            que_obj.comment.add(comment_obj)
            que_obj.save()
        if request.POST.get('answer'):
            ans_obj = Answer.objects.get(id=request.POST['answer'])
            ans_obj.comment.add(comment_obj)
            ans_obj.save()

        return Response(CommentSerializer(comment_obj).data)


class VoteCreateView(ListCreateAPIView):
    serializer_class = VoteSerializer

    def get_queryset(self):
        return Vote.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = VoteSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        try:
            vote = Vote(
                voter_user=request.user)
            vote.save()

            if request.POST.get('question'):
                que_obj = Question.objects.get(id=request.POST.get('question'))
                que_obj.question_voter.add(vote)
                que_obj.vote_count += int(request.POST.get('vote'))
                que_obj.save()
            else:
                que_obj = Answer.objects.get(id=request.POST.get('answer'))
                que_obj.answer_voter.add(vote)
                que_obj.vote_count += int(request.POST.get('vote'))
                que_obj.save()

        except Exception as e:
            raise NotFound(str(e))

        return Response(VoteSerializer(vote).data)
