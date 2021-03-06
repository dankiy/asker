from django.urls import path
from . import views
from .api import views as api_views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.QuestionCreate.as_view(), name='create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('api/', api_views.QuestionListView.as_view(), name=None),
    path('api/<int:pk>', api_views.QuestionResultView.as_view(), name=None),
]
