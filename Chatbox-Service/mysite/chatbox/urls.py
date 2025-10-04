from django.urls import path
from . import views

urlpatterns = [
  path('create-session/', views.create_session, name='create_session'),
  path('create-question/', views.create_question, name='create-question'),
  path('create-answer/', views.create_answer, name='create-answer')
]