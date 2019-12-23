from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db import transaction
from .models import Choice, Question
from .forms import *
import os
import boto3
import botocore.session

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

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


class QuestionCreate(generic.CreateView):
    model = Question
    template_name = 'polls/create.html'
    form_class = QuestionForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(QuestionCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['choices'] = ChoiceFormSet(self.request.POST)
        else:
            data['choices'] = ChoiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context['choices']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if choices.is_valid():
                choices.instance = self.object
                choices.save()
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('polls:detail', kwargs={'pk': self.object.pk})

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
            session = boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
                aws_session_token=os.environ['AWS_SESSION_TOKEN'],
                region_name=os.environ['AWS_REGION']
            )
            sns = session.client('sns')
            response = sns.publish(
                TopicArn='arn:aws:sns:us-east-1:716390431917:Polls',
                Message=request.user.username+' has voted for '+selected_choice.choice_text+\
                ' in '+question.question_text
            )

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]