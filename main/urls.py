"""Defines URL patterns for learning_logs."""

from django.urls import path
from django.urls import path, include

from . import views

app_name = 'main'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('contact/ticket-created/', views.ticket_created, name='ticket-created/'),
    path('support-price/', views.support_price, name='support-price'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('faq/', views.faq, name='faq'),
    path('services/', views.services, name='services'),

    #path('helpdesk/', include('helpdesk.urls')),
    #path('blog/', include('blog.urls')),

    path('newsletter/', include('newsletter.urls')),
    # 2FA

    #path('slider/', views.slider, name='slider'),
    #path('testim/', views.testim, name='testim'),
]