from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
import boto3
import botocore.session

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    if request.user.choice_set.filter(question=question).exists():
        return render(request, 'polls/results.html', {
            'question': question,
            'error_message': "You have already voted.",
        })
    else:
        selected_choice.votes.add(request.user)
        selected_choice.num_votes += 1
        selected_choice.save()

        if question.notifications:
            session = boto3.session.Session()
            sns = session.client('sns')
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-1:716390431917:Polls',
                Message=request.user.username+' has voted for '+selected_choice.choice_text+\
                ' in '+question.question_text
            )

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
