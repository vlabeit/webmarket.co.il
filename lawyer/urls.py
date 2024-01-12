"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'lawyer'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('won/', views.won, name='won'),
    path('practice/', views.practice, name='practice'),
]