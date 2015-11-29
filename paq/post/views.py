from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import TagSerializer, QustionSerializer, AnswerSerializer, \
    CommentSerializer
from .models import Tag, Question, Answer, Comment


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

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Question.objects.all()
        question_id = request.GET.get('question_id')
        if question_id:
            queryset = queryset.filter(id=question_id)
        serializer = QustionSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        tags = request.POST.getlist('tags')
        answers = request.POST.getlist('answers')
        if request.POST.get('type'):
            if int(request.POST.get('type')) == 0:
                post_type = Question.PRIVATE
            else:
                post_type = Question.PUBLIC

        post = Question(
            user_id=request.user, title=request.POST.get('title'),
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
            user = request.user
            ans = Answer(
                reply_user=user, description=request.POST.get('description'))

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
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)
