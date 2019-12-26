from ..models import Post
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer

class QuestionCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.QuestionSerializer

    def create(self, request, *args, **kwargs):
        super(QuestionCreateView, self).create(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully created",
                    "result": request.data}
        return Response(response)
