from ..models import Question, Choice
from . import serializers
from rest_framework import generics, status, permissions
from rest_framework.response import Response

class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.QuestionSerializer(queryset, many=True)
        data = [[q['question_text'], q['pub_date']] for q in serializer.data]
        return Response(data)

class QuestionResultView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        super(QuestionResultView, self).retrieve(request, args, kwargs)
        question = self.get_object()
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Successfully retrieved",
                    "result": {"question_text": question.question_text,
                                "choices": {choice.choice_text : choice.num_votes \
                                for choice in question.choice_set.all()}}}
        return Response(response)
